# Product Enrichment System V3

AI-powered product enrichment using a **Multi-Agent Architecture** with Azure OpenAI GPT-4o.

## 🚀 Features

- **Multi-Agent AI Pipeline**: 2-stage enrichment (Creator → Reviewer)
- **Single File Architecture**: Reads and writes to the same Excel file
- **Duplicate Prevention**: Automatically skips already-enriched products
- **Batch Processing**: Process 10 products at a time
- **Type-Safe**: Full Pydantic validation
- **Production Ready**: FastAPI with comprehensive error handling

## 📋 Prerequisites

- Python 3.11+
- Azure OpenAI API access
- Excel file with product data

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
ENRICHER_DEPLOYMENT=gpt-4o
OPENAI_TEMPERATURE=0.3
```

### 3. Prepare Your Data

Place your product data in `app/data/products.xlsx` with the following structure:

| Product Code | Product Description |
|--------------|---------------------|
| ABC123       | Basic product info  |
| DEF456       | Another product     |

### 5. Saving Enriched Data

**Service**: `app/services/excel_service.py`

#### Process:
1. Opens `app/data/products.xlsx`
2. Ensures enrichment columns exist (adds them if missing):
   - Short Description (Enriched)
   - Product Description (Enriched)
   - Product Long Description (Enriched)
   - Timestamp
3. Finds the row matching the product code
4. Updates the row with enriched data
5. Saves the file

### 4. Start the Server

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🔌 API Endpoints

### Single Product Enrichment

**Endpoint**: `POST /api/enrich`

**Request**:
```json
{
  "product_code": "ABC123",
  "product_description": "Cardboard box for shipping"
}
```

**Response** (200 OK):
```json
{
  "product_code": "ABC123",
  "short_title": "The shipping unit is a heavy-duty cardboard box constructed from corrugated fiberboard.",
  "short_description": "The unit consists of a double-walled corrugated cardboard container designed for shipping applications.",
  "long_description": "This heavy-duty shipping box is manufactured from double-walled corrugated cardboard..."
}
```

**Response** (409 Conflict - Already Enriched):
```json
{
  "detail": "Product ABC123 already enriched"
}
```

### Bulk Enrichment

**Endpoint**: `POST /api/enrich/bulk`

Processes the next 10 unenriched products from `products.xlsx`.

**Response**:
```json
{
  "processed": 10,
  "succeeded": 10,
  "failed": 0,
  "skipped": 0,
  "errors": []
}
```

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Product Enrichment API",
  "version": "2.0"
}
```

## 🧪 Testing

Run the included test script:

```bash
python test_agent.py
```

This will call the bulk enrichment endpoint and display the results.

## 📁 Project Structure

```
Product_Enrichment-V3/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── enrich.py          # API endpoints
│   ├── services/
│   │   ├── agent_service.py   # Multi-agent orchestration
│   │   └── excel_service.py   # Excel file operations
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── agent_prompts.py   # AI prompt templates
│   ├── models/
│   │   └── schemas.py         # Pydantic request/response models
│   └── data/
│       └── products.xlsx      # Source and output file
├── .env                        # Environment variables (create this)
├── requirements.txt            # Python dependencies
├── test_agent.py              # Test script
├── README.md                   # This file
└── PROCESS_FLOW.md            # Detailed process documentation
```

## 🔄 How It Works

1. **Read**: System scans `products.xlsx` for unenriched products
2. **Enrich**: Each product goes through 2 AI agents:
   - **Creator**: Drafts clinical technical sentences for Title and Summary fields
   - **Reviewer**: Validates, "purifies" from fluff, and formats output as JSON
3. **Save**: Enriched data is written back to the same Excel file
4. **Prevent Duplicates**: Products with populated "Short Description (Enriched)" are skipped

For a detailed step-by-step flow, see [PROCESS_FLOW.md](PROCESS_FLOW.md).

## 🎯 Multi-Agent Architecture

### Creator Agent
- Analyzes raw product strings
- Identifies technical specifications
- Drafts clinical, technical sentences for Title and Summary fields
- Creates a detailed technical specification paragraph

### Reviewer Agent
- Validates content quality and factual accuracy
- Ensures technical sentence structure (no comma-separated lists)
- Purifies content from marketing "fluff" or qualitative adjectives
- Ensures JSON format compliance

## 📊 Output Format

The system adds these columns to your Excel file:

| Column | Description |
|--------|-------------|
| Short Description (Enriched) | Concise product title (50-80 chars) |
| Product Description (Enriched) | Brief description (100-150 chars) |
| Product Long Description (Enriched) | Detailed technical breakdown (15-20 lines, multiple paragraphs) |
| Timestamp | When the enrichment was performed |

## ⚠️ Important Notes

- **File Access**: Ensure `products.xlsx` is not open in Excel during processing
- **Duplicate Prevention**: Checks if "Short Description (Enriched)" is populated
- **Batch Size**: Default is 10 products per bulk request
- **API Costs**: Each product requires 3 GPT-4o API calls

## 🐛 Troubleshooting

### Server won't start
- Check that all environment variables are set in `.env`
- Verify Azure OpenAI credentials are correct

### Products not being enriched
- Ensure `products.xlsx` exists in `app/data/`
- Check that products have both code and description
- Verify products don't already have "Short Description (Enriched)" populated

### 409 Conflict errors
- This means the product is already enriched
- Check the "Short Description (Enriched)" column in Excel
- This is expected behavior, not an error

## 📝 License

Internal use only.

## 🤝 Support

For issues or questions, contact the development team.
