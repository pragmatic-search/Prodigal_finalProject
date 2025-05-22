from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import pipeline
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Text Summarizer API",
    description="API for summarizing text content using a pre-trained AI model.",
    version="1.0.0",
)

# Global variable for the model
summarizer_pipeline = None

def load_ai_model():
    global summarizer_pipeline
    model_name = "sshleifer/distilbart-cnn-6-6"
    
    try:
        logger.info(f"Loading summarization model: {model_name}...")
        summarizer_pipeline = pipeline("summarization", model=model_name)
        logger.info("Summarization model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load AI model: {e}", exc_info=True)
        raise RuntimeError("Could not load AI model at startup.")

@app.on_event("startup")
async def startup_event():
    load_ai_model()

class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=100,
        max_length=5000,
        description="The raw text content to be summarized."
    )

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    if summarizer_pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model is not ready. Please try again in a moment."
        )

    try:
        summary_results = summarizer_pipeline(
            request.text,
            max_length=150,
            min_length=30,
            do_sample=False
        )
        
        summary = summary_results[0]['summary_text'] if summary_results else "No summary could be generated."
        return {"original_text_length": len(request.text), "summary": summary}
    
    except Exception as e:
        logger.error(f"An error occurred during summarization: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the summary. Please check the input text."
        )

@app.get("/")
async def read_root():
    return {"message": "AI Text Summarizer API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)