from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Text Summarizer API",
    description="API for summarizing text content using a pre-trained AI model.",
    version="1.0.0",
)

# Pydantic model for request body validation
class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=50,  # Example: Minimum 50 characters for meaningful summarization
        max_length=5000, # Example: Maximum 5000 characters to prevent abuse/overload
        description="The raw text content to be summarized."
    )

# Placeholder for AI model loading and inference (will be integrated in next steps)
def get_text_summary(input_text: str) -> str:
    """
    This is a placeholder function for the AI model.
    In a later phase, this will call the actual AI model (e.g., HuggingFace Transformers).
    """
    logger.info(f"Received text for summarization (first 100 chars): {input_text[:100]}...")
    # Simulate a summarization process
    if len(input_text) < 100:
        return f"Summary: The input text is too short to summarize effectively. Original: {input_text}"
    return f"This is a simulated summary of your text: '{input_text[:150]}...'. Please integrate the actual AI model here."

# API Endpoint for Text Summarization
@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    """
    Accepts raw text and returns its summarized version.

    - **text**: The input text content to be summarized.
    """
    try:
        # Call the placeholder function for AI model inference
        summary = get_text_summary(request.text)
        logger.info("Text summarization successful.")
        return {"original_text_length": len(request.text), "summary": summary}
    except ValueError as e:
        logger.error(f"Input validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during summarization.")

# Root endpoint for health check or basic info
@app.get("/")
async def read_root():
    return {"message": "AI Text Summarizer API is running!"}

# Optional: Run the app directly for local testing (when not using Docker)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)