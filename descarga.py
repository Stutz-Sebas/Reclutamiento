from transformers import AutoModelForCausalLM, AutoTokenizer

# Especifica el nombre del modelo
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

# Descarga el modelo y el tokenizador
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Guarda el modelo y tokenizador localmente para uso offline
model.save_pretrained("./mistral-7b-instruct")
tokenizer.save_pretrained("./mistral-7b-instruct")