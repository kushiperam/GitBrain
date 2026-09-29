from sentence_transformers import SentenceTransformer


print("================================")
print("GitBrain Embedding Test")
print("================================")

print()

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded successfully!")

print()

text = "How is synthetic data generated?"

embedding = model.encode(text)

print(
    f"Embedding dimensions: {len(embedding)}"
)

print()

print("First 10 embedding values:")

print(
    embedding[:10]
)