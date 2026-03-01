# Pink Receipt API

An AI-powered harassment detection API that analyzes screenshots of messages and returns a structured assessment of whether the content is concerning, along with options and resources for the potential victim.

---

## What It Does

The user can send screenshot of a conversation to the API and it will:
- Detect whether the message contains harassment or abusive language
- Classify the severity (low, medium, high)
- Provide options and relevant resources based on the situation

---


## Live API Link
```
https://pink-reciept-api.vercel.app/
```

---

##  API Reference

### `POST /analyze`

Analyzes an image screenshot for harassment detection.

**Base URL:** `https://pink-reciept-api.vercel.app/analyze`

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file |  Yes | Screenshot of the message (JPEG, PNG, etc.) |

- Content-Type: `multipart/form-data`

---

### `POST /report`

Generates a formal harassment report that the victim can submit directly to the platform.

**Base URL:** `https://pink-reciept-api.vercel.app/report`

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string |  Yes | Platform where harassment occurred (e.g. Instagram, Twitter) |
| `severity` | string |  Yes | Severity level: `low`, `medium`, or `high` |
| `summary` | string |  Yes | Brief description of the harassment |
| `options` | array |  No | List of recommended options from the `/` endpoint |
| `resources` | array |  No | List of resources from the `/` endpoint |

- Content-Type: `application/json`

---

## Authentication

This API is currently open and does not require authentication. 
Any user with the endpoint URL can send requests directly.

---

## Testing with Postman - Analyze Images

1. Open Postman and create a new request
2. Set method to **POST**
3. Enter the URL: `https://pink-reciept-api.vercel.app/analyze`
4. Click **Body** → select **form-data**
5. Add a key called `image`, change the type to **File**
6. Upload your screenshot
7. Click **Send**

---

## Testing with cURL

**Mac/Linux:**
```bash
curl -X POST https://pink-reciept-api.vercel.app/ \
  -F "image=@/Users/yourname/Desktop/screenshot.jpg"
```

**Windows:**
```bash
curl.exe -X POST https://pink-reciept-api-sage.vercel.app/ \
  -F "image=@C:\Users\yourname\Pictures\Screenshots\screenshot.png"
```
---

## Example Response

```json
{
  "is_concerning": true,
  "severity": "high",
  "summary": "The message contains threatening and abusive language directed at the recipient.",
  "options": [
    "Block the sender on this platform",
    "Take a screenshot and save it as evidence",
    "Reach out to a trusted friend or family member",
    "Report the message to the platform"
  ],
  "resources": [
    "Crisis Text Line: Text HOME to 741741",
    "National Domestic Violence Hotline: 1-800-799-7233",
    "StopBullying.gov",
    "Cyber Civil Rights Initiative: cybercivilrights.org"
  ]
}
```

---

##  Report Generation

### Step 1. Analyze the screenshot first using `POST /`
Use the response from the first endpoint to fill in the report fields.

### Step 2. Generate the report using `POST /report`

**Postman:**
1. Open Postman and click **New Request**
2. Set method to **POST**
3. Enter URL: `https://pink-reciept-api.vercel.app/report`
4. Click **Body** → select **raw** → set type to **JSON**
5. Paste and fill in:
```json
{
  "platform": "Instagram",
  "severity": "high",
  "summary": "The message contains threatening language directed at the recipient.",
  "options": ["Block the sender", "Save as evidence"],
  "resources": ["Crisis Text Line: Text HOME to 741741"]
}
```
6. Click **Send**

**cURL (Mac/Linux):**
```bash
curl -X POST https://pink-reciept-api.vercel.app/report \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "Instagram",
    "severity": "high",
    "summary": "The message contains threatening language.",
    "options": ["Block the sender", "Save as evidence"],
    "resources": ["Crisis Text Line: Text HOME to 741741"]
  }'
```

**cURL (Windows):**
```bash
curl.exe -X POST https://pink-reciept-api.vercel.app/report ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"Instagram\", \"severity\": \"high\", \"summary\": \"The message contains threatening language.\", \"options\": [\"Block the sender\", \"Save as evidence\"], \"resources\": [\"Crisis Text Line: Text HOME to 741741\"]}"
```

**Example Report Response:**
```json
{
  "report": "To the Trust & Safety Team at Instagram,\n\nI am writing to formally report an incident of harassment that occurred on your platform..."
}
```

---

## Error Handling

The API returns informative error messages with appropriate HTTP status codes.

| Status Code | Meaning | Example Response |
|-------------|---------|-----------------|
| `200` | Success | Full JSON analysis or report |
| `400` | Bad request | `{"error": "No file uploaded"}` |
| `400` | Bad request | `{"error": "No file selected"}` |
| `400` | Missing required fields | `{"error": "Missing required fields: platform, severity, summary"}` |
| `500` | Failed to parse Gemini response | `{"error": "Failed to parse Gemini response: <details>"}` |
| `500` | General server error | `{"error": "error details here"}` |

**Troubleshooting:**
- Make sure the form field is named exactly `image`
- Make sure you are uploading an actual image file (JPEG or PNG only)
- If you get `Failed to parse Gemini response`, the AI returned an unexpected format, try again with a clearer screenshot
- If you get a general 500 error, check that your file is not corrupted

---

##  Running Locally

**Prerequisites:**
- Python 3.12+
- A Google Gemini API key (get one free at [aistudio.google.com](https://aistudio.google.com))

**1. Clone the repo**

```bash
git clone https://github.com/MoonRock404/PinkRecieptAPI
cd PinkRecieptAPI
```

**2. Create a virtual environment**

Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
```

**5. Run the app**
```bash
python api/app.py
```

The API will be running at `http://localhost:5000`

**6. Test it locally**

Mac/Linux:
```bash
curl -X POST http://localhost:5000/ \
  -F "image=@/Users/yourname/Desktop/screenshot.jpg"
```
Windows:
```bash
curl.exe -X POST http://localhost:5000/ \
  -F "image=@C:\Users\yourname\Pictures\Screenshots\screenshot.png"
```

---

## Deployment

This API is deployed on **Vercel**. Every push to the `main` branch on GitHub automatically redeploys the live API.

**To deploy your own instance:**
1. Fork this repo
2. Go to [vercel.com](https://vercel.com) and sign in with GitHub
3. Click **New Project** and import your forked repo
4. Add environment variables in Vercel dashboard:
   - `GEMINI_API_KEY` → your Gemini API key
   - `GEMINI_MODEL_NAME` → `gemini-2.5-flash`
5. Click **Deploy** (Adjust commands for Mac and Windows)
```bash
curl -X POST http://localhost:5000/ \
  -F "image=@/path/to/screenshot.jpg"
```

---

## Tech Stack

### Language & Framework
- **Python 3.12** — core programming language
- **Flask 3.0.0** — lightweight web framework for building the API

### AI
- **Google Gemini 2.5 Flash** — multimodal AI model used for:
  - Analyzing image screenshots for harassment detection
  - Generating formal harassment reports

### Deployment
- **Vercel** — serverless hosting and deployment platform
  - Publicly accessible live endpoint

### Development & Testing
- **Postman** — API testing and documentation
- **cURL** — command line API testing
- **Git + GitHub** — version control and source code hosting

---

##  AI Disclosure

This project was built with the assistance of the following AI tools:

- **Google Gemini 2.5 Flash** — core AI model used to analyze screenshots, detect harassment, and generate formal reports
- **Claude (Anthropic)** — assisted with debugging, code suggestions, and documentation during development
- **ChatGPT (OpenAI)** — assisted with brainstorming, writing, and debugging during development

---
