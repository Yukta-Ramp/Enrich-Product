"""
Excel service for saving enriched product data.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Set, List, Optional
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill

from app.core.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelService:
    """Service for managing Excel file operations."""
    
    def __init__(self):
        """Initialize Excel service with output path."""
        self.output_path = config.EXCEL_OUTPUT_PATH
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        data_dir = os.path.dirname(self.output_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Created data directory: {data_dir}")
    
    def _create_new_workbook(self) -> Workbook:
        """
        Create a new Excel workbook with headers.
        
        Returns:
            Workbook: New workbook with formatted headers
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Enriched Products"
        
        # Define headers
        headers = [
            "Product Code",
            "Short Title",
            "Short Description",
            "Long Description",
            "Timestamp"
        ]
        
        # Write headers
        ws.append(headers)
        
        # Style headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Set column widths
        ws.column_dimensions['A'].width = 15  # Product Code
        ws.column_dimensions['B'].width = 40  # Short Title
        ws.column_dimensions['C'].width = 50  # Short Description
        ws.column_dimensions['D'].width = 60  # Long Description
        ws.column_dimensions['E'].width = 20  # Timestamp
        
        logger.info(f"Created new workbook: {self.output_path}")
        return wb
    
    def save_enrichment(self, enriched_data: Dict[str, Any]) -> None:
        """
        Save enriched product data to Excel file.
        
        Args:
            enriched_data: Dictionary containing enriched product information
        """
        try:
            # Load existing workbook or create new one
            if os.path.exists(self.output_path):
                wb = load_workbook(self.output_path)
                ws = wb.active
                logger.info(f"Loaded existing workbook: {self.output_path}")
            else:
                wb = self._create_new_workbook()
                ws = wb.active
            
            # Prepare row data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row_data = [
                enriched_data.get("product_code", ""),
                enriched_data.get("short_title", ""),
                enriched_data.get("short_description", ""),
                enriched_data.get("long_description", ""),
                timestamp
            ]
            
            # Append row
            ws.append(row_data)
            
            # Apply text wrapping to description columns
            last_row = ws.max_row
            ws[f'C{last_row}'].alignment = Alignment(wrap_text=True, vertical="top")
            ws[f'D{last_row}'].alignment = Alignment(wrap_text=True, vertical="top")
            
            # Save workbook
            wb.save(self.output_path)
            logger.info(f"Saved enrichment for product {enriched_data.get('product_code')} to Excel")
            
        except Exception as e:
            logger.error(f"Failed to save to Excel: {e}")
            raise ValueError(f"Excel save failed: {e}")
    
    def get_output_path(self) -> str:
        """
        Get the Excel output file path.
        
        Returns:
            str: Path to the Excel file
        """
        return self.output_path


    def get_existing_product_codes(self) -> Set[str]:
        """
        Get set of product codes that have already been enriched.
        
        Returns:
            Set[str]: Set of existing product codes
        """
        existing_codes = set()
        
        if not os.path.exists(self.output_path):
            return existing_codes
            
        try:
            wb = load_workbook(self.output_path, read_only=True)
            ws = wb.active
            
            # Skip header row
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row and row[0]:  # Product Code is first column
                    existing_codes.add(str(row[0]).strip())
                    
            logger.info(f"Found {len(existing_codes)} existing enriched products")
            return existing_codes
            
        except Exception as e:
            logger.error(f"Failed to read existing codes: {e}")
            return set()

    def read_products_batch(self, batch_size: int = 10, exclude_codes: Set[str] = None) -> List[Dict[str, str]]:
        """
        Read a batch of products from source file that haven't been enriched yet.
        
        Args:
            batch_size: Number of products to read
            exclude_codes: Set of product codes to skip
            
        Returns:
            List[Dict]: List of products to enrich
        """
        products = []
        exclude_codes = exclude_codes or set()
        input_path = config.INPUT_PRODUCTS_PATH
        
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        try:
            wb = load_workbook(input_path, read_only=True)
            ws = wb.active
            
            # Skip header row
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or len(row) < 2:
                    continue
                    
                code = str(row[0]).strip()
                description = str(row[1]).strip()
                
                if not code or not description:
                    continue
                    
                if code in exclude_codes:
                    continue
                    
                products.append({
                    "product_code": code,
                    "product_description": description
                })
                
                if len(products) >= batch_size:
                    break
                    
            logger.info(f"Read {len(products)} new products for enrichment")
            return products
            
        except Exception as e:
            logger.error(f"Failed to read input products: {e}")
            raise ValueError(f"Failed to read input products: {e}")

# Singleton instance
excel_service = ExcelService()
