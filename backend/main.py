from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
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

# --- AI Model Loading ---
# Global variables to store the model and tokenizer for efficient loading
summarizer_pipeline = None

# Function to load the AI model (called once at app startup)
def load_ai_model():
    global summarizer_pipeline
    model_name = "sshleifer/distilbart-cnn-12-6" # A common summarization model

    try:
        logger.info(f"Loading summarization model: {model_name}...")
        # Using pipeline for ease of use. For more control, load tokenizer and model separately.
        summarizer_pipeline = pipeline("summarization", model=model_name, tokenizer=model_name)
        logger.info("Summarization model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load AI model: {e}", exc_info=True)
        # Depending on criticality, you might want to exit here or make the endpoint return an error
        raise RuntimeError("Could not load AI model at startup.")

# Call the model loading function when the application starts
@app.on_event("startup")
async def startup_event():
    load_ai_model()

# Pydantic model for request body validation
class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=100,  # Example: Minimum 100 characters for meaningful summarization
        max_length=5000, # Example: Maximum 5000 characters to prevent abuse/overload
        description="The raw text content to be summarized."
    )

# API Endpoint for Text Summarization
@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    """
    Accepts raw text and returns its summarized version using the AI model.

    - **text**: The input text content to be summarized.
    """
    if summarizer_pipeline is None:
        logger.error("AI model is not loaded.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model is not ready. Please try again in a moment."
        )

    try:
        logger.info(f"Processing text for summarization (first 100 chars): {request.text[:100]}...")

        # Preprocess, pass to AI model for inference, and post-process
        # The pipeline abstracts these steps.
        # min_length and max_length can be adjusted based on desired summary length
        # Typically, a length_penalty > 1.0 encourages longer summaries.
        # num_beams > 1 for more diverse/better quality summaries (but slower).
        summary_results = summarizer_pipeline(
            request.text,
            max_length=150,  # Max length of the generated summary
            min_length=30,   # Min length of the generated summary
            do_sample=False  # For deterministic output
        )

        # The pipeline returns a list of dictionaries, extract the summary text
        summary = summary_results[0]['summary_text'] if summary_results else "No summary could be generated."
        
        logger.info("Text summarization successful.")
        return {"original_text_length": len(request.text), "summary": summary}
    
    except Exception as e:
        logger.error(f"An error occurred during summarization: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the summary. Please check the input text."
        )

# Root endpoint for health check or basic info
@app.get("/")
async def read_root():
    return {"message": "AI Text Summarizer API is running and model is loaded!" if summarizer_pipeline else "AI Text Summarizer API is running, but model is still loading or failed to load."}

# Optional: Run the app directly for local testing (when not using Docker)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)