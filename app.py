# app.py (FastAPI backend)

from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import RAGEngine
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig,Runner
import os
from dotenv import load_dotenv

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(title="AI Car Maintenance RAG API")
load_dotenv()
# -------------------------------
# Pydantic model for request
# -------------------------------
class Query(BaseModel):
    question: str

# -------------------------------
# Configure Gemini API
# -------------------------------

gemini_api_key = os.environ.get("GEMINI_API_KEY")  # set in environment

if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing. Please set it in your .env file.")



externel_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# -------------------------------
# Model setup
# -------------------------------
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # Use a valid model from your account
    openai_client=externel_client,
)

config = RunConfig(
    model=model,
    model_provider=externel_client,
    tracing_disabled=True
)

# -------------------------------
# Initialize RAG engine
# -------------------------------
rag = RAGEngine()
rag.build_index()  # builds the vector index for car maintenance docs

# -------------------------------
# FastAPI endpoint
# -------------------------------
@app.post("/ask")
async def ask_question(q: Query):
    try:
        # Step 1: Retrieve relevant docs from RAG index
        context = rag.retrieve(q.question)

        # Step 2: Construct prompt with context
        prompt = f"""You are an AI Car Maintenance Expert.
Answer this car maintenance question using the following info:\n{context}\n\nQuestion: {q.question}
Provide:
- Simple explanation
- Probable causes
- 2-3 steps for checking
- Safety warning
"""
        
        
        
        agent = Agent(
            name="CarMaintenanceAgent",
            model=model,      # your OpenAIChatCompletionsModel      
            )
        
        
        # Step 3: Run the prompt through Runner with your config
        runner = Runner()
        result = await runner.run(
            starting_agent=agent,
            #config=config,
            input=prompt)

        # Step 4: Extract answer text
        answer = getattr(result, "output_text", str(result))  # use output_text if available

        return {"answer": answer}

    except Exception as e:
        # Always return JSON to avoid Streamlit JSONDecodeError
        return {"answer": f"Error generating answer: {e}"}