from studentapp.rag.embedding import embed_text
from studentapp.rag.generator import generate generate_answer
from studentapp.rag.vector_store import search_chunks
from studentapp.rag.structured_retriever import (
    get_student_data,
    student_data_to_context
)

#main RAG_pipeline
#connect student data, document retriveal,
#and gemini to generate the final answer.
def ask_rag(question, user):
    #get the logged-in student's structured data
    student_data = get_student_data(user)
    structured_context = student_data_to_context(
        student_data
    )
    #convert the user query into a vector 
    #so that it can be compared with document vector 
    query_vector = embed_text(questuion)
    #search chromadb for tha most relevent 
    #document chunk belonging to this student
    results = search_chunks(
        query_vector,
        student_id=student_data["student_id"],
        n_results=3

    )
    document = results["document"][0]
    metadata = results["metadata"][0]

    #combine the retrived document chunks into one piece of context for gemini
    document_context = "\n\n".join(
        documents
    )

    #combine structured student data
    #and unstructured document data
    context = f"""
STRUCTURED STUDENT DATA:

{structured_context}

UNSTRUCTURES DOCUMENT DATA:

{document_context}
"""
    #send the question and combine context to
    #geminini model to generated final answer
    result = generate_answer(
        question,
        context

    )

    sources = []

    for metadata in metadatas:
        source = metadata.get("source")

        if source:
            sources.append({ 
                "document_id":metadata.get("document-id"),
                "source":source,
                "chunk_index":metadata.get("chunk_index")

            })
    response = result.model_dump()

    response["sources"] = sources

    return response