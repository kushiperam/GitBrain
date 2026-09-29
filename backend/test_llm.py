from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


print("Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)


print("Model loaded!")
print()


question = "What is FastAPI?"


messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful software engineering "
            "assistant."
        )
    },
    {
        "role": "user",
        "content": question
    }
]


text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)


inputs = tokenizer(
    text,
    return_tensors="pt"
)


print("Generating answer...")
print()


outputs = model.generate(
    **inputs,
    max_new_tokens=100
)


generated_tokens = outputs[
    0
][
    inputs["input_ids"].shape[1]:
]


answer = tokenizer.decode(
    generated_tokens,
    skip_special_tokens=True
)


print("================================")
print("Question")
print("================================")

print(question)

print()

print("================================")
print("Answer")
print("================================")

print(answer)