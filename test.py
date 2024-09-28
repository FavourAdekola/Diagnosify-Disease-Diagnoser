from transformers import BioGptForCausalLM, BioGptTokenizer
import torch

# Load BioGPT tokenizer and model
tokenizer = BioGptTokenizer.from_pretrained("microsoft/biogpt")
model = BioGptForCausalLM.from_pretrained("microsoft/biogpt")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Sample input text (e.g., medical symptoms)
input_text = "The patient presents with a persistent cough and shortness of breath."

# Tokenize input text
inputs = tokenizer(input_text, return_tensors="pt").to(device)

# Generate text
output = model.generate(inputs["input_ids"], max_length=150, num_beams=5, early_stopping=True)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
