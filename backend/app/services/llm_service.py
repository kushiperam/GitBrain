from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from app.services.rag_service import (
    build_rag_context
)


# ==========================================
# Local LLM Configuration
# ==========================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("Loading GitBrain local LLM...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

print("GitBrain local LLM loaded successfully!")


# ==========================================
# Basic LLM Generation
# ==========================================

def generate_answer(
    question: str,
    context: str,
    max_new_tokens: int = 300
) -> str:

    """
    Generate a concise answer using only
    the retrieved repository context.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are GitBrain.\n"
                "Answer ONLY from the repository code "
                "given by the user.\n"
                "Do not use outside knowledge.\n"
                "Do not invent steps, technologies, "
                "or files.\n"
                "If the answer is in the code, explain "
                "exactly what the code does.\n"
                "Keep the answer short."
            )
        },
        {
            "role": "user",
            "content": (
                "Repository code:\n"
                "----------------\n"
                f"{context}\n"
                "----------------\n\n"
                f"Question: {question}\n\n"
                "Answer using only the repository code:"
            )
        }
    ]

    # Create chat prompt
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Convert prompt to model input
    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    # Generate deterministic answer
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=None,
        top_p=None
    )

    # Remove original prompt tokens
    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    # Convert tokens to text
    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()


# ==========================================
# Repository-Aware RAG Answer
# ==========================================

def generate_repository_answer(
    repository_path: str,
    question: str,
    top_k: int = 1,
    max_new_tokens: int = 300
) -> dict:

    """
    Complete GitBrain pipeline:

    Repository
        ↓
    Semantic Search
        ↓
    RAG Context
        ↓
    Local LLM
        ↓
    Answer + Sources
    """

    print()
    print("Building RAG context...")

    rag_result = build_rag_context(
        repository_path=repository_path,
        question=question,
        top_k=top_k
    )

    print(
        f"Retrieved chunks: "
        f"{len(rag_result['chunks'])}"
    )

    # Show RAG context in terminal
    print()
    print("========== RAG CONTEXT ==========")
    print(rag_result["context"])
    print("=================================")
    print()

    # ==========================================
    # No Relevant Repository Context
    # ==========================================

    if not rag_result["chunks"]:

        return {
            "answer": (
                "I could not find relevant information "
                "in the selected repository to answer "
                "this question."
            ),
            "sources": []
        }

    # ==========================================
    # Generate Answer Using Repository Context
    # ==========================================

    answer = generate_answer(
        question=question,
        context=rag_result["context"],
        max_new_tokens=max_new_tokens
    )

    # ==========================================
    # Build Source Information
    # ==========================================

    sources = []

    for chunk in rag_result["chunks"]:

        sources.append(
            {
                "file": chunk["path"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "score": float(chunk["score"])
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }