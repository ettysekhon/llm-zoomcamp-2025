from typing import List, Tuple

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from vector_search.settings import OPENAI_API_KEY


def run_qdrant_rag_pipeline(
    documents: List[str],
    query: str,
    collection_name: str = "rag_docs",
    llm_model: str = "gpt-4",
    host: str = "localhost",
    port: int = 6333,
) -> Tuple[str, List[str]]:
    """
    Runs a simple RAG pipeline using Qdrant, OpenAI embeddings, and an OpenAI LLM.
    Returns:
        - The LLM-generated answer.
        - List of source document strings.
    """

    qdrant_client = QdrantClient(host=host, port=port)
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    unique_docs = list(set(documents))
    metadatas = [{"source": f"doc_{i}"} for i in range(len(unique_docs))]

    if qdrant_client.collection_exists(collection_name):
        qdrant_client.delete_collection(collection_name=collection_name)

    vectorstore = QdrantVectorStore.from_texts(
        texts=unique_docs,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=collection_name,
        location=f"http://{host}:{port}",
    )

    template = """Use the context below to answer the question.
        If the context is irrelevant or insufficient, say so.

        Context:
        {context}

        Question: {question}

        Answer:
    """
    llm = ChatOpenAI(model_name=llm_model, api_key=OPENAI_API_KEY)
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt,
            "document_variable_name": "context",
        },
    )

    result = qa_chain.invoke(query)
    sources = [doc.page_content for doc in result["source_documents"]]

    return result["answer"], sources
