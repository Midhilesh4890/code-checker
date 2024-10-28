from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Histogram, Counter, generate_latest
from fastapi.responses import Response
import joblib
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the pre-trained model
try:
    model = joblib.load("simple_code_review_model.pkl")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error("Error loading model: %s", e)
    model = None  # Set model to None to handle errors gracefully

# Define input model for the API


class CodeSnippet(BaseModel):
    code: str


# Prometheus metrics
REQUEST_TIME = Histogram('request_processing_seconds',
                         'Time spent processing request')
REQUEST_COUNT = Counter('code_review_requests_total',
                        'Total number of code review requests')
ERROR_COUNT = Counter('code_review_errors_total',
                      'Total number of errors in code review requests')

# Endpoint for metrics (make sure this is synchronous)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Endpoint for code review


@app.post("/review_code/")
async def review_code(snippet: CodeSnippet):
    REQUEST_COUNT.inc()  # Increment the request count
    if model is None:
        logger.error("Model is not loaded. Cannot process request.")
        ERROR_COUNT.inc()
        return {"error": "Model not loaded. Please check server logs."}
    try:
        # Time the prediction process manually using Histogram
        with REQUEST_TIME.time():
            prediction = model.predict([snippet.code])[0]
        logger.info("Prediction made successfully.")
        return {"result": prediction}
    except Exception as e:
        ERROR_COUNT.inc()  # Increment error count in case of an exception
        logger.error("Error during prediction: %s", e)
        return {"error": str(e)}
