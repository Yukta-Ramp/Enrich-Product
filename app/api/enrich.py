"""
API endpoint for product enrichment.
"""

import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import EnrichRequest, EnrichResponse, ErrorResponse
from app.models.schemas import EnrichRequest, EnrichResponse, ErrorResponse
from app.services.agent_service import agent_service
from app.services.excel_service import excel_service
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/enrich",
    response_model=EnrichResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Enrich Product",
    description="Enrich a product with AI-generated content and save to Excel"
)
async def enrich_product(request: EnrichRequest):
    """
    Enrich a product using GPT-4o and save the result to Excel.
    
    Args:
        request: EnrichRequest containing product_code and product_description
        
    Returns:
        EnrichResponse: Enriched product data
        
    Raises:
        HTTPException: If enrichment or Excel save fails
    """
    try:
        logger.info(f"Received enrichment request for product: {request.product_code}")
        
        # Validate input
        if not request.product_code.strip():
            raise HTTPException(
                status_code=400,
                detail="product_code cannot be empty"
            )
        
        if not request.product_description.strip():
            raise HTTPException(
                status_code=400,
                detail="product_description cannot be empty"
            )
        
        # Check if already enriched
        existing_codes = excel_service.get_existing_product_codes()
        if request.product_code in existing_codes:
             logger.warning(f"Product {request.product_code} already enriched, skipping.")
             raise HTTPException(
                 status_code=409,
                 detail=f"Product {request.product_code} already enriched"
             )

        # Enrich product using Multi-Agent Service
        enriched_data = await agent_service.enrich_product_multi_agent(
            product_code=request.product_code,
            product_description=request.product_description
        )
        
        # Save to Excel
        excel_service.save_enrichment(enriched_data)
        
        # Return enriched data
        response = EnrichResponse(**enriched_data)
        logger.info(f"Successfully processed product: {request.product_code}")
        
        return response
        
    except HTTPException as e:
        raise e
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error during enrichment: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/enrich/bulk",
    summary="Bulk Enrich Products",
    description="Enrich next batch of 100 new products"
)
async def bulk_enrich_products() -> Dict[str, Any]:
    """
    Enrich a batch of products from the source file.
    
    Returns:
        Dict: Processing statistics
    """
    try:
        logger.info("Received bulk enrichment request")
        
        stats = await agent_service.process_bulk_enrichment(batch_size=100)
        
        return stats
        
    except ValueError as e:
        logger.error(f"Bulk validation error: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error during bulk enrichment: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


