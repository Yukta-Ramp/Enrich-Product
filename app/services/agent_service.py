
import json
import logging
from typing import Dict, Any, List
from openai import AzureOpenAI

from app.core.config import config
from app.core.agent_prompts import STRATEGIST_PROMPT, CREATOR_PROMPT, REVIEWER_PROMPT
from app.services.excel_service import excel_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentService:
    """Service for multi-agent product enrichment."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION
        )
        self.model = config.ENRICHER_DEPLOYMENT  # Using same model for all agents for now
        self.temperature = config.OPENAI_TEMPERATURE

    async def _call_gpt(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        """Helper to call GPT."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"} if json_mode else None
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT call failed: {e}")
            raise

    async def enrich_product_multi_agent(self, product_code: str, product_description: str) -> Dict[str, Any]:
        """
        Run the 3-stage agent process.
        """
        logger.info(f"Starting multi-agent enrichment for {product_code}")
        
        # Stage 1: Strategist
        logger.info(f"🤖 Strategist Agent: analyzing {product_code}...")
        strategist_input = STRATEGIST_PROMPT.format(
            product_code=product_code, 
            product_description=product_description
        )
        strategic_brief = await self._call_gpt("You are a strategist.", strategist_input)
        logger.info(f"✅ Strategist Agent: Brief created.")
        logger.info(f"   Brief Summary: {strategic_brief[:100]}...")

        # Stage 2: Creator
        logger.info(f"✍️ Creator Agent: drafting content based on brief...")
        creator_input = CREATOR_PROMPT.format(
            strategic_brief=strategic_brief,
            product_code=product_code,
            product_description=product_description
        )
        draft_content = await self._call_gpt("You are a copywriter.", creator_input)
        logger.info(f"✅ Creator Agent: Content drafted.")

        # Stage 3: Reviewer
        logger.info(f"🔍 Reviewer Agent: validating and formatting...")
        reviewer_input = REVIEWER_PROMPT.format(
            draft_content=draft_content,
            product_code=product_code
        )
        final_json_str = await self._call_gpt("You are a QA specialist.", reviewer_input, json_mode=True)
        logger.info(f"✅ Reviewer Agent: Approved and formatted.")
        
        try:
            final_data = json.loads(final_json_str)
            return final_data
        except json.JSONDecodeError:
            logger.error(f"Failed to parse final JSON for {product_code}")
            raise ValueError("Final agent output was not valid JSON")

    async def process_bulk_enrichment(self, batch_size: int = 10) -> Dict[str, Any]:
        """
        Process a batch of products using multi-agent logic.
        """
        stats = {
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
        
        try:
            existing_codes = excel_service.get_existing_product_codes()
            products_to_process = excel_service.read_products_batch(
                batch_size=batch_size,
                exclude_codes=existing_codes
            )
            
            stats["processed"] = len(products_to_process)
            
            if not products_to_process:
                return stats
            
            for product in products_to_process:
                product_code = product["product_code"]
                description = product["product_description"]
                
                try:
                    if product_code in existing_codes:
                        stats["skipped"] += 1
                        continue
                        
                    # Call Multi-Agent Enrichment
                    enriched_data = await self.enrich_product_multi_agent(product_code, description)
                    
                    # Validate keys
                    required = ["product_code", "short_title", "short_description", "long_description"]
                    for req in required:
                        if req not in enriched_data:
                            enriched_data[req] = "" # fallback or raise error?
                            
                    excel_service.save_enrichment(enriched_data)
                    existing_codes.add(product_code)
                    stats["succeeded"] += 1
                    
                except Exception as e:
                    stats["failed"] += 1
                    error_msg = f"Failed to enrich {product_code}: {str(e)}"
                    stats["errors"].append(error_msg)
                    logger.error(error_msg)
            
            return stats
            
        except Exception as e:
            logger.error(f"Bulk processing error: {e}")
            raise ValueError(f"Bulk processing failed: {e}")

# Singleton
agent_service = AgentService()
