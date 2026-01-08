# Backend - Product Enrichment V2

Clean, production-ready Product Enrichment system using FastAPI and GPT-4o.

## Features

- Simple product enrichment with 6 key fields
- GPT-4o powered AI enrichment
- Excel file output for enriched products
- Clean separation of concerns
- Type-safe with Pydantic validation

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the Server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## API Endpoints

### POST `/enrich`

Enrich a product with AI-generated content.

**Request:**
```json
{
  "product_code": "ABC123",
  "product_description": "Cardboard box for shipping"
}
```

**Response:**
```json
{
  "product_code": "ABC123",
  "short_title": "Heavy-Duty Cardboard Shipping Box",
  "short_description": "Durable corrugated cardboard box designed for secure shipping and storage.",
  "long_description": "This heavy-duty cardboard box is made from high-quality corrugated material...",
  "seo_tags": ["cardboard-box", "shipping-box", "corrugated", "packaging"],
  "category": "Packaging",
  "sub_categories": ["Corrugated Boxes", "Shipping Supplies"]
}
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Configuration and prompts
│   ├── models/       # Pydantic schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI app
├── data/             # Excel output files
└── requirements.txt
```

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - Model name (default: gpt-4o)
- `OPENAI_TEMPERATURE` - Temperature setting (default: 0.3)
