# GitBrain Architecture

GitBrain is an AI-powered Repository Memory Engine that allows developers to ask natural-language questions about software repositories.

The system combines repository scanning, code chunking, semantic search, Retrieval-Augmented Generation (RAG), and a local language model.

---

## 1. High-Level Architecture

```mermaid
flowchart TD

    U[Developer]

    FE[React + Vite Frontend]

    API[FastAPI Backend]

    AUTH[Authentication & Authorization]

    REP[Repository Service]

    CHUNK[Code Chunking]

    SEARCH[Semantic Search]

    EMB[Sentence Transformer<br/>all-MiniLM-L6-v2]

    RAG[RAG Context Builder]

    LLM[Local LLM<br/>Qwen2.5-0.5B-Instruct]

    ANS[Repository-Aware Answer]

    DB[(PostgreSQL)]

    GH[GitHub Repository]

    LOCAL[Local Repository]

    U --> FE
    FE --> API

    API --> AUTH
    API --> REP
    API --> SEARCH

    AUTH --> DB
    REP --> DB

    REP --> GH
    REP --> LOCAL

    GH --> CHUNK
    LOCAL --> CHUNK

    CHUNK --> EMB
    EMB --> SEARCH

    SEARCH --> RAG
    RAG --> LLM
    LLM --> ANS

    ANS --> API
    API --> FE
    FE --> U