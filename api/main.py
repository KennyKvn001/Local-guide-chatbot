from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import initialize_rag_pipeline, query_rag


app = FastAPI(title="Rwanda LocalGuide Chatbot")

# Allow localhost front-end during development
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for query input
class QueryRequest(BaseModel):
    query: str


# Initialize RAG pipeline
vector_store, llm = initialize_rag_pipeline()


@app.post("/query")
async def query_chatbot(request: QueryRequest):
    try:
        response = query_rag(vector_store, llm, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
