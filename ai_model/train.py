from db_config.sqlaenv import engine
import pandas as pd
from datasets import Dataset

descricao_competencias = {
    "Competência 1": {
        "Descricao": "É avaliado se a redação do participante está adequada às regras de ortografia, como acentuação, ortografia, uso de hífen, emprego de letras maiúsculas e minúsculas e separação silábica. Ainda são analisadas a regência verbal e nominal, concordância verbal e nominal, pontuação, paralelismo, emprego de pronomes e crase.",
        "Pontuacoes": {
            "Excepcional": "Demonstra excelente domínio da modalidade escrita formal da língua portuguesa e de escolha de registro. Desvios gramaticais ou de convenções da escrita serão aceitos somente como excepcionalidade e quando não caracterizarem reincidência.",
            "Excelente": "Demonstra bom domínio da modalidade escrita formal da língua portuguesa e de escolha de registro. com poucos desvios gramaticais e de convenções da escrita.",
            "120": "Demonstra domínio mediano da modalidade escrita formal da língua portuguesa e de escolha de registro. com alguns desvios gramaticais e de convenções da escrita.",
            "80": "Demonstra dominio insuficiente da modalidade escrita formal da língua portuguesa, com muitos desvios gramaticais. de escolha de registro e de convenções da escrita.",
            "40": "Demonstra dominio precário da modalidade escrita formal da língua portuguesa. de forma sistemática, com diversificados e frequentes desvios gramaticais. de escolha de registro e de convenções da escrita.",
            "0": "Demonstra desconhecimento da modalidade escrita formal da língua portuguesa.",
        },
    },
    "Competência 2": {
        "Descricao": "Avalia as habilidades integradas de leitura e de escrita do candidato. O tema constitui o núcleo das ideias sobre as quais a redação deve ser organizada e é caracterizado por ser uma delimitação de um assunto mais abrangente.",
        "Pontuacoes": {
            "Excepcional": "Desenvolve o tema por meio de argumentação consistente, a partir de umrepertório sociocultural produtivo e apresenta excelente doml.o do texto dissertativo-argumentativo.",
            "Excelente": "Desenvolve o tema por meio de argumentação consistente e apresenta bom domínio do texto dissertativo-argumentativo, com proposição, argumentação e conclusão.",
            "120": "Desenvolve O tema por meio de argumentação previsivel e apresenta dominio mediano do texto dissertativo-argumentativo, com proposição, argumentação e conclusão.",
            "80": "Desenvolve o tema recorrendo a cópia de trechos dos textos motivadores ou apresenta domínio insuficiente do texto dissertativo-argumentativo, não atendendo a estrutura com proposição, argumentação e conclusão.",
            "40": "Apresenta o assunto, tangenciando o tema, ou demonstra dominio precário do texto dissertativo-argumentativo, com traços constantes de outros tipos textuais.",
            "0": "Fuga ao tema/não atendimento à estrutura dissertativo-argumentativa. Nestes casos a redação recebe nota zero e é anulada.",
        },
    },
    "Competência 3": {
        "Descricao": "O candidato precisa elaborar um texto que apresente, claramente, uma ideia a ser defendida e os argumentos que justifiquem a posição assumida em relação à temática da proposta da redação. Trata da coerência e da plausibilidade entre as ideias apresentadas no texto, o que é garantido pelo planejamento prévio à escrita, ou seja, pela elaboração de um projeto de texto.",
        "Pontuacoes": {
            "Excepcional": "Apresenta informações, fatos e opiniões relacionados ao terna proposto, de forma consistente e organizada, configurando autoria, em defesa de um ponto de vista.",
            "Excelente": "Apresenta informações, fatos e opiniões relacionados ao tema, de forma organizada, com indicios de autoria, em defesa de um ponto de vista.",
            "120": "Apresenta informações, e opiniões relacionados ao tema, limitados aos argumentos dos textos motivadores e pouco organizado, em defesa de um ponto de vista.",
            "80": "Apresenta informações, fatos e opiniões relacionados ao tema, mas desorganizados ou contraditórios e limitados aos argumentos dos textos motivadores, em defesa de um ponto de vista.",
            "40": "Apresenta informações, fatos e opiniões pouco relacionados ao tema ou incoerentes e sem defesa de um ponto de vista.",
            "0": "Apresenta informações, fatos e opiniões não relacionados ao tema e sem defesa de um ponto de vista.",
        },
    },
    "Competência 4": {
        "Descricao": "São avaliados itens relacionados à estruturação lógica e formal entre as partes da redação. A organização textual exige que as frases e os parágrafos estabeleçam entre si uma relação que garanta uma sequência coerente do texto e a interdependência entre as ideias. Preposições, conjunções, advérbios e locuções adverbiais são responsáveis pela coesão do texto porque estabelecem uma inter-relação entre orações, frases e parágrafos. Cada parágrafo será composto por um ou mais períodos também articulados. Cada ideia nova precisa estabelecer relação com as anteriores.",
        "Pontuacoes": {
            "Excepcional": "Articula bem as partes do texto e apresenta repertório diversificado de recursos coesivos.",
            "Excelente": "Articula as partes do texto, com poucas inadequações, e apresenta repertório diversificado de recursos coesivos.",
            "120": "Articula as partes do texto, de forma mediana, com inadequações, e apresenta repertório pouco diversificado de recursos ccesivos.",
            "80": "Articula as partes do texto, de forma insuficiente, com muitas inadequações e apresenta repertório limitado de recursos coesivos",
            "40": "Articula as partes do texto de forma precária.",
            "0": "Não articula as informações. ",
        },
    },
    "Competência 5": {
        "Descricao": "Apresentar uma proposta de intervenção para o problema abordado que respeite os direitos humanos. Propor uma intervenção para o problema apresentado pelo tema significa sugerir uma iniciativa que busque, mesmo que minimamente, enfrentá-lo. A elaboração de uma proposta de intervenção na prova de redação do Enem representa uma ocasião para que o candidato demonstre o preparo para o exercício da cidadania, para atuar na realidade em consonância com os direitos humanos.",
        "Pontuacoes": {
            "Excepcional": "Elabora muito bem proposta de intervenção, detalhada, relacionada ao tema e articulada à discussão desenvolvida no texto.",
            "Excelente": "Elabora bem proposta de intervenção relacionada ao tema e articulada à discussão desenvolvida no texto.",
            "120": "Elabora, de forma mediana, proposta de intervenção relacionada ao tema e articulada à discussão desenvolvida no texto.",
            "80": "Elabora, de forma insuficiente, proposta de intervenção relacionada ao tema, ou não articulada com a discussão desenvolvida no texto.",
            "40": "Apresenta proposta de intervenção vaga, precária ou relacionada apenas ao assunto.",
            "0": "Não apresenta proposta de intervenção ou apresenta proposta não relacionada ao tema ou ao assunto.",
        },
    },
}


def load_training_data_from_db(split: str = "train") -> Dataset:
    df = pd.read_sql(
        """
          select
            p.title as "prompt",
            p.description as description,
            e.title as "title",
            e."text" as "text",
            e."comments" as "comments",
            e.criteria_score_1 as "criteria_score_1",
            e.criteria_score_2 as "criteria_score_2",
            e.criteria_score_3 as "criteria_score_3",
            e.criteria_score_4 as "criteria_score_4",
            e.criteria_score_5 as "criteria_score_5"
          from
            public.essay e
          inner join public.prompt p on
            e.prompt_id = p.id;
        """.strip(),
        engine,
    )
    new_df = pd.DataFrame()

    new_df["input"] = df.apply(lambda row: generate_human_prompt(row), axis=1)
    new_df["output"] = df.apply(lambda row: generate_bot_response(row), axis=1)

    return Dataset.from_pandas(new_df)


def generate_prompt(data):
    return {
        "human": generate_human_prompt(data),
        "bot": generate_bot_response(data),
    }


def generate_human_prompt(data):
    return {
        "criteria_descriptions": descricao_competencias,
        "proposed_essay_data": {
            "prompt": data["prompt"],
            "description": data["description"],
        },
        "student_essay_data": {
            "title": data["title"],
            "text": data["text"],
        },
    }


def generate_bot_response(data):
    return {
        "comments": data["comments"],
        "criteria_scores": {
            "competencia_1": data["criteria_score_1"],
            "competencia_2": data["criteria_score_2"],
            "competencia_3": data["criteria_score_3"],
            "competencia_4": data["criteria_score_4"],
            "competencia_5": data["criteria_score_5"],
        },
    }


def generate_prompt_for_completion(input_data):
    return {
        "human": {
            "criteria_descriptions": descricao_competencias,
            "proposed_essay_data": {
                "prompt": input_data["prompt"],
                "description": input_data["description"],
            },
            "student_essay_data": {
                "title": input_data["title"],
                "text": input_data["text"],
            },
        },
        "bot": {},
    }
