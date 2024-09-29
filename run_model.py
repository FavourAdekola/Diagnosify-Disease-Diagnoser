from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("./trained_model")
model = GPT2LMHeadModel.from_pretrained("./trained_model")

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    input_text = input_data.get('input_text', '')
    input_text = input_text + ", can you give me ONE disease they may have?"

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)

    # Generate text
    output = model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"],
                            do_sample=True, max_length=60, no_repeat_ngram_size=2, num_beams=5,
                            early_stopping=True, pad_token_id=tokenizer.pad_token_id, temperature=0.5,
                            top_p=0.9)

    # Decode and return the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    prompt_length = len(input_text)
    if generated_text.startswith(input_text):
    # Slice the generated text to remove the prompt
        generated_text = generated_text[prompt_length:].strip()
        generated_text = generated_text.split(",")
    return jsonify({"output_text": generated_text[0]})

if __name__ == '__main__':
    app.run(debug=True)