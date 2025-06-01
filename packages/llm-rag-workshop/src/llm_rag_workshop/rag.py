from elasticsearch import Elasticsearch
from openai import OpenAI

from llm_rag_workshop.settings import OPENAI_API_KEY

es = Elasticsearch("http://localhost:9200")
index_name = "course-questions"

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_openai(prompt, model="gpt-4o"):
    print(f"Asking OpenAI with {model} model...")
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    print(completion)
    content = completion.choices[0].message.content.strip()
    return content


def build_prompt(question, context):
    prompt = f"""
    Answer the following question based on the provided context:
    
    Question: {question}
    Context: {context}
    
    Answer:
    """

    return ask_openai(prompt)


def retrieve_documents(
    query,
    index_name="course-questions",
    max_results=5,
    course="data-engineering-zoomcamp",
):
    search_query = {
        "size": max_results,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields",
                    }
                },
                "filter": {"term": {"course": course}},
            }
        },
    }

    response = es.search(index=index_name, body=search_query)
    documents = [hit["_source"] for hit in response["hits"]["hits"]]
    return documents


def qa_bot(user_question, course="data-engineering-zoomcamp"):
    context_docs = retrieve_documents(user_question, course=course)
    prompt = build_prompt(user_question, context_docs)
    answer = ask_openai(prompt)
    return answer
