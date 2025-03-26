# app/api/main.py
from fastapi import FastAPI,Request, HTTPException, Depends
from api.endpoints import user
from api.models import ai_debugging as ai_debugging_models
from api.services import ai_debugging_service
from api.utils.database import engine, Base
# from api.core.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.include_router(user.router, prefix="/api/v1")


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return HTTPException(
        status_code=429,
        detail=f"Rate limit exceeded. Try again in {exc.retry_after} seconds.",
    )
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# Kept the ai suggestion route in main.py because slowapi libary was not handling the sub routers for rate limiting correctly.
@app.post("/ai_debugging/analyze_code", response_model=ai_debugging_models.CodeAnalysisResponse)
@limiter.limit("5/minute")  # This endpoint will be rate-limited to a maximum of 5 requests per minute from the same client.
async def analyze_code(
    request: Request, 
    code_analysis_request: ai_debugging_models.CodeAnalysisRequest,
    ai_service: ai_debugging_service.AIDebuggingService = Depends()
):
    """
    Analyzes the provided code using the OpenRouter AI model.
    """
    suggestions = await ai_service.analyze_code(code_analysis_request.code, code_analysis_request.language)
    return {"suggestions": suggestions}

def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    create_tables()