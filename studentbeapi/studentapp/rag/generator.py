import time
from django.conf import settings
from google import genai
from studentapp.rag.schemas import RAGResponse

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def generate_answer(question, context):
    prompt = f"""
You are an assitant for a student portal

Answer the user's question using the provided context when relevant. For general knowledge questions, you may use your general knowledge.

Context:
{context}

Question:
{question}

Instructions:
- Use the provided context when the question is related to the student's data or uploaded documents.
- For general educational or knowledge questions, you may use your general knowledge.
- Do not invent student-specific information.
"""
    #number of times to retry if gemini returns a rate-limit error
    max_retries = 3
    for attempt in range(max_retries):
        try:
            #send the prompt to gemini and request
            # a response matching the RAGresponse 
            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt,
                response_format={
                    "type":"text",
                    "mime_type":"application/json",
                    "schema": RAGResponse.model_json_schema()

                }
            )
            
            #validate gemini's json response using pydantic
            result = RAGResponse.model_validate_json(
                interaction.output_text
            )
            return result
        except Exception as e:
            error_message = str(e)

            #raise other errors immediately
            if "429" not in error_message:
                raise
            if attempt == max_retries - 1:
                raise
            wait_time = 20 * (attempt + 1)

            print(
                f"gemini generation rate limit reached."
                f"Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)