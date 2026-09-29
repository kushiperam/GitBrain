# GitBrain — Repository Memory Engine

GitBrain is an AI-powered Repository Intelligence Platform that helps developers understand and interact with software repositories using natural-language questions.

Instead of manually searching through files and code, developers can select a repository and ask questions such as:

- What does `app/main.py` do?
- How does authentication work?
- Where is the database connection configured?
- Which files are responsible for repository analysis?
- How does the RAG pipeline retrieve relevant code?

GitBrain searches the repository, retrieves relevant code, builds a contextual prompt, and generates an answer using a local language model.

---

## 🚀 Key Features

### 1. Repository Intelligence

GitBrain can analyze software repositories and understand their source-code structure.

It supports:

- GitHub repositories
- Local repositories
- Repository file scanning
- Code chunking
- Semantic search
- Repository-aware question answering

---

### 2. Natural-Language Repository Q&A

Users can ask questions about the selected repository in natural language.

Example:

> What does app/main.py do?

GitBrain retrieves the most relevant code and generates an answer based on the repository context.

---

### 3. Retrieval-Augmented Generation (RAG)

GitBrain uses a Retrieval-Augmented Generation pipeline:

```text
User Question
      ↓
Semantic Search
      ↓
Relevant Code Chunks
      ↓
RAG Context
      ↓
Local Language Model
      ↓
Repository-Aware Answer