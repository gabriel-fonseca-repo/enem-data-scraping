import os
import sys
import torch
import json
from transformers import (
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    AutoModelForCausalLM,
    AutoTokenizer,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from datasets import Dataset


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from essay_db.util import get_r_file_path
from ai_model.train import (
    generate_prompt_for_completion,
    load_training_data_from_db,
)

mistral_id = "mistralai/Mistral-7B-Instruct-v0.2"
maritaca_id = "maritaca-ai/sabia-7b"


class MixtralAIModel:

    model: AutoModelForCausalLM
    tokenizer: AutoTokenizer
    model_id: str
    bnb_config: BitsAndBytesConfig
    data: Dataset

    def __init__(self):
        self.model_id = mistral_id

        self.data = load_training_data_from_db("train")

        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, model_max_length=1024, max_length=1024
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="cuda:0",
            low_cpu_mem_usage=True,
            torch_dtype=torch.bfloat16,
            quantization_config=self.bnb_config,
        )

        self.generation_config = self.model.generation_config
        self.generation_config.max_new_tokens = 2000
        self.generation_config.temperature = 0.7
        self.generation_config.top_p = 0.7
        self.generation_config.num_return_sequences = 1
        self.generation_config.pad_token_id = self.tokenizer.eos_token_id
        self.generation_config.eos_token_id = self.tokenizer.eos_token_id

    def generate_tokenized_prompt(self, data_point):

        full_prompt = json.dumps(dict(data_point)).strip()

        tokenized_prompt = self.tokenizer(full_prompt, padding=True, truncation=True)

        return tokenized_prompt

    def train_model(self):
        prompt_train_data_from_db = self.data.shuffle().map(
            self.generate_tokenized_prompt
        )

        model_dir = get_r_file_path("/ai_model/trained/mixtral-trained-model")

        # self.model.gradient_checkpointing_enable()
        self.model = prepare_model_for_kbit_training(self.model)

        lora_config = LoraConfig(
            lora_alpha=16,
            lora_dropout=0.1,
            r=64,
            bias="none",
            task_type="CAUSAL_LM",
        )

        self.model = get_peft_model(self.model, lora_config)

        training_args = TrainingArguments(
            output_dir=get_r_file_path("/ai_model/experiments"),
            auto_find_batch_size=True,
        )

        trainer = Trainer(
            model=self.model,
            train_dataset=prompt_train_data_from_db,
            args=training_args,
            data_collator=DataCollatorForLanguageModeling(self.tokenizer, mlm=False),
        )

        self.model.config.use_cache = False
        trainer.train()

        self.model.save_pretrained(model_dir)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            return_dict=True,
            quantization_config=self.bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )

        self.tokenizer.pad_token = self.tokenizer.eos_token

        # self.model = PeftModel.from_pretrained(model, PEFT_MODEL)

    def generate_response(self, prompt):
        device = "cuda:0"

        encoding = self.tokenizer(prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = self.model.generate(
                input_ids=encoding.input_ids,
                attention_mask=encoding.attention_mask,
                generation_config=self.generation_config,
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    model = MixtralAIModel()
    model.train_model()

    while True:
        user_prompt = input("Enter a prompt: ")
        user_prompt = json.load(user_prompt)
        user_prompt = generate_prompt_for_completion(user_prompt)
        response = model.generate_response(user_prompt)
        print("Resposta: " + response)
