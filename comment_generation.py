# comment_generation.py

from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_comment(code_snippet, model):
    """
    Generate a natural language comment for the given code snippet using the provided language model.

    Args:
    code_snippet (str): The code snippet for which a comment is to be generated.
    model: The pre-trained language model for comment generation.

    Returns:
    str: The generated natural language comment.
    """
    tokenizer = GPT2Tokenizer.from_pretrained(model)
    model = GPT2LMHeadModel.from_pretrained(model)

    inputs = tokenizer.encode(code_snippet, return_tensors='pt', max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)

    generated_comment = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_comment

if __name__ == "__main__":
    # Example code snippet for comment generation
    code_snippet = "def calculate_sum(a, b): return a + b"

    # Example pre-trained model for comment generation
    model_name = 'gpt2'

    generated_comment = generate_comment(code_snippet, model_name)
    print(generated_comment)

