"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import List


class EnrichRequest(BaseModel):
    """Request model for product enrichment."""
    
    product_code: str = Field(..., description="Unique product identifier")
    product_description: str = Field(..., description="Raw product description text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_code": "ABC123",
                "product_description": "Cardboard box for shipping"
            }
        }


class EnrichResponse(BaseModel):
    """Response model for enriched product data."""
    
    product_code: str = Field(..., description="Product identifier")
    short_title: str = Field(..., description="Short product title (8-10 words)")
    short_description: str = Field(..., description="Brief description (1-2 sentences)")
    long_description: str = Field(..., description="Detailed description (1-2 paragraphs)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_code": "ABC123",
                "short_title": "Heavy-Duty Corrugated Cardboard Shipping Box",
                "short_description": "Durable corrugated cardboard box designed for secure shipping and storage.",
                "long_description": "This heavy-duty cardboard box is made from high-quality corrugated material, providing excellent protection for goods during transit. Ideal for e-commerce, logistics, and warehouse storage applications."
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Detailed error information")
