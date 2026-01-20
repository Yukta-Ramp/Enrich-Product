import asyncio
import json
from app.services.agent_service import agent_service

async def test_enrichment_with_classification():
    test_products = [
        {
            "code": "TEST_RETAIL_01",
            "desc": "Wireless Bluetooth Earbuds with Noise Cancellation for daily commuting."
        },
        {
            "code": "TEST_INDUSTRIAL_01",
            "desc": "Heavy-duty hydraulic press for metal stamping in automotive manufacturing."
        },
        {
            "code": "TEST_AGRI_01",
            "desc": "Automated irrigation system with soil moisture sensors for large scale farms."
        }
    ]

    for p in test_products:
        print(f"\n--- Testing Product: {p['code']} ---")
        try:
            result = await agent_service.enrich_product_multi_agent(p['code'], p['desc'])
            print(json.dumps(result, indent=2))
            assert "product_division" in result
            assert "class_group" in result
            print(f"✅ Success: Categorized as {result['product_division']} -> {result['class_group']}")
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_enrichment_with_classification())
