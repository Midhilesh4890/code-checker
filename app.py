# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Summary, Counter, generate_latest
from prometheus_client import start_http_server
from fastapi.responses import Response
import joblib
import time

app = FastAPI()

# Load model
model = joblib.load("simple_code_review_model.pkl")

# Define input model for API


class CodeSnippet(BaseModel):
    code: str


# Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds',
                       'Time spent processing request')
REQUEST_COUNT = Counter('code_review_requests_total',
                        'Total number of code review requests')
ERROR_COUNT = Counter('code_review_errors_total',
                      'Total number of errors in code review requests')

# Endpoint for metrics


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Endpoint for code review


@REQUEST_TIME.time()
@app.post("/review_code/")
async def review_code(snippet: CodeSnippet):
    REQUEST_COUNT.inc()  # Increment request count
    try:
        prediction = model.predict([snippet.code])[0]
        return {"result": prediction}
    except Exception as e:
        ERROR_COUNT.inc()  # Increment error count if there's an error
        return {"error": str(e)}
