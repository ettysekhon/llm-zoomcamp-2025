from vector_search.rag import run_qdrant_rag_pipeline


def main():
    docs = [
        "Qdrant is a high-performance vector database that stores embeddings and allows fast similarity searches. It's ideal for AI and ML applications, including recommendation systems and semantic search.",
        "To integrate Qdrant with large language models (LLMs), you store vectorized representations of your data in Qdrant and retrieve the most relevant vectors based on user queries. This retrieved context can then be passed to an LLM for generation — this is known as retrieval-augmented generation (RAG).",
        "LangChain offers built-in integration with Qdrant, allowing you to use Qdrant as a retriever for documents in a RetrievalQA chain. This enables seamless semantic search and context injection into LLM prompts.",
    ]

    answer, sources = run_qdrant_rag_pipeline(docs, "How does Qdrant work with LLMs?")
    print("Answer:")
    print(answer)
    print("\nSources:")
    for src in sources:
        print("-", src)


if __name__ == "__main__":
    main()
