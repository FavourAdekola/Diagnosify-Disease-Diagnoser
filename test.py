#from transformers import BioGptForCausalLM, BioGptTokenizer, BioGptModel
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load BioGPT tokenizer and model

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Sample input text (e.g., medical symptoms)
input_text = "A patient has been found with a sore throat and a fever, what disease might they have?"

# Tokenize input text
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)

# Generate text
output = model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"], do_sample = True, max_length=150, no_repeat_ngram_size=2,num_beams=5, early_stopping=True, pad_token_id=tokenizer.pad_token_id, temperature=0.5,                          # Lower temperature for more focused responses
    top_p=0.9)

# Decode and print the generated text
print("Tokenized Input IDs:", inputs["input_ids"])

# Print the generated output IDs before decoding
print("Generated Output IDs:", output)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Text:", generated_text)
