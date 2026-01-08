"""
FastAPI application entry point.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
# from app.api.enrich import router as enrich_router
from app.api.enrich import enrich_product, bulk_enrich_products

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate configuration
try:
    config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Create FastAPI app
app = FastAPI(
    title="Product Enrichment API",
    description="AI-powered product enrichment using GPT-4o",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response

from app.api.enrich import enrich_product as enrich_handler

# Include routers
# logger.info(f"Including enrichment router with prefix '/api'")
# app.include_router(enrich_router, prefix="/api", tags=["Enrichment"])

# Access endpoint directly
app.post("/api/enrich", tags=["Enrichment"])(enrich_product)
app.post("/api/enrich/bulk", tags=["Enrichment"])(bulk_enrich_products)


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Product Enrichment API",
        "version": "2.0"
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Product Enrichment API v2.0")
    logger.info(f"Using Azure OpenAI endpoint: {config.AZURE_OPENAI_ENDPOINT}")
    logger.info(f"Enricher deployment: {config.ENRICHER_DEPLOYMENT}")
    logger.info(f"Temperature: {config.OPENAI_TEMPERATURE}")
    
    # Log registered routes
    logger.info("Registered Routes:")
    for route in app.routes:
        logger.info(f"- {route.path} [{route.name}]")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Product Enrichment API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Product Enrichment API v2.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/test")
async def test_route():
    """Debug route."""
    return {"message": "Test route working"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
