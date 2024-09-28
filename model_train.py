import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
from torch.utils.data import Dataset

# Custom Dataset class
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer):
        self.input_texts = texts
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.input_texts)

    def __getitem__(self, idx):
        encodings = self.tokenizer(self.input_texts[idx], truncation=True, padding='max_length', return_tensors="pt", max_length=512)
        input_ids = encodings["input_ids"].squeeze()  # Remove batch dimension
        attention_mask = encodings["attention_mask"].squeeze()
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": input_ids  # In causal language modeling, labels are usually the same as input_ids
        }

def preprocessing():
    # Load the CSV file
    df = pd.read_csv('C:/Projects/Python/Disease Diagnosis RAG Agent/disease_dataset.csv')

    # Create a text-based dataset
    formatted_data = []
    for _, row in df.iterrows():
        symptoms = ", ".join([row[f'Symptom_{i}'].replace("_", " ") for i in range(1, 17) if pd.notna(row[f'Symptom_{i}'])])
        disease = row['Disease']
        formatted_data.append(f"Symptoms: {symptoms}\nDisease: {disease}\n")

    return formatted_data

def training():
    # Load the tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    
    tokenizer.pad_token = tokenizer.eos_token

    # Preprocess the data
    training_texts = preprocessing()

    # Create the dataset
    dataset = TextDataset(training_texts, tokenizer)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Disable masked language modeling for causal LM
    )

    # Prepare the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    # Train the model
    trainer.train()

    # Generate text for testing
    input_text = "Symptoms: Fever, Dry Cough, Fatigue"
    input_ids = tokenizer(input_text, return_tensors="pt")["input_ids"].to(model.device)

    # Generate text
    output = model.generate(input_ids, max_length=50)

    # Decode the output
    predicted_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(predicted_text)
    print("We Finished")

training()
