# Flask REST API

Production-ready Flask REST API with mathematical operations and AI integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your Gemini API key:
```bash
GEMINI_API_KEY=your_actual_api_key
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in"
}
```

---

### POST /bfhl

**Request Rules:**
- Content-Type: `application/json`
- Body must contain EXACTLY ONE key
- Allowed keys: `fibonacci`, `prime`, `lcm`, `hcf`, `AI`

---

#### Fibonacci
Returns first N Fibonacci numbers starting from 0.

**Request:**
```json
{
  "fibonacci": 7
}
```

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "data": [0, 1, 1, 2, 3, 5, 8]
}
```

---

#### Prime
Filters and returns only prime numbers from array.

**Request:**
```json
{
  "prime": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "data": [2, 3, 5, 7]
}
```

---

#### LCM
Returns the Least Common Multiple of all values.

**Request:**
```json
{
  "lcm": [4, 6, 8]
}
```

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "data": 24
}
```

---

#### HCF
Returns the Highest Common Factor (GCD) of all values.

**Request:**
```json
{
  "hcf": [12, 18, 24]
}
```

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "data": 6
}
```

---

#### AI
Integrates Google Gemini API to return a single-word answer.

**Request:**
```json
{
  "AI": "What is the capital of France?"
}
```

**Response:**
```json
{
  "is_success": true,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "data": "Paris"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "is_success": false,
  "official_email": "keshav3858.beai23@chitkara.edu.in",
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `400` - Bad Request (missing/invalid request)
- `422` - Unprocessable Entity (wrong data type/structure)
- `500` - Internal Server Error

## Security Features

- Input size limits to prevent abuse
- Environment variables for secrets
- Comprehensive error handling
- JSON-only responses
- Type validation for all inputs
