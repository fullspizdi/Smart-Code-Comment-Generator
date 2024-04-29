# ai_model_training.py

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.utils.data import Dataset, DataLoader

class CodeCommentDataset(Dataset):
    def __init__(self, code_snippets, comments):
        self.code_snippets = code_snippets
        self.comments = comments

    def __len__(self):
        return len(self.code_snippets)

    def __getitem__(self, idx):
        return self.code_snippets[idx], self.comments[idx]

def train_language_model(dataset, num_epochs=5):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for code, comment in dataloader:
            optimizer.zero_grad()

            inputs = tokenizer.encode(code[0], return_tensors='pt').to(device)
            labels = tokenizer.encode(comment[0], return_tensors='pt').to(device)

            outputs = model(inputs, labels=labels)
            loss = outputs[0]
            total_loss += loss.item()

            loss.backward()
            optimizer.step()

        print(f'Epoch {epoch + 1}, Loss: {total_loss / len(dataloader)}')

if __name__ == "__main__":
    # Example dataset for training
    code_snippets = ["def add_numbers(a, b): return a + b", "class MyClass: pass"]
    comments = ["Function to add two numbers", "Simple class definition"]

    dataset = CodeCommentDataset(code_snippets, comments)
    train_language_model(dataset)

