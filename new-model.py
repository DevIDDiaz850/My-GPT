from flask import Flask, request, jsonify
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
from flask_cors import CORS 




# Cargar el modelo
model_path = "./my_gpt2_dolly_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Configurar el generador
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    do_sample=True,
    temperature=0.8,
    top_k=50,
    top_p=0.9
)

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app) 

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        # Obtener los datos JSON enviados en la solicitud
        data = request.get_json()

        # Validar que el JSON contenga las claves necesarias
        if not data or "prompt" not in data:
            return jsonify({"error": "Debe incluirse un 'prompt' en la solicitud"}), 400
        
        # Leer parámetros
        prompt = data["prompt"]
        max_length = data.get("max_length", 100)

        # Generar texto
        output = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=1,
            truncation=True
        )
        return jsonify({"generated_text": output[0]["generated_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
