from transformers import pipeline

unmasker = pipeline("fill-mask", model="fonsecovizk/bert-enem-essay-grading")
unmasker("Hello I'm a [MASK] model.")
