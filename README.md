# 🎀 Pink Receipt API

An AI-powered harassment detection API that analyzes screenshots of messages and returns a structured assessment of whether the content is concerning, along with options and resources for the potential victim.

---

## What It Does

Send a screenshot of a conversation or message to the API and it will:
- Detect whether the message contains harassment or abusive language
- Classify the severity (low, medium, high)
- Provide options for the potential victim
- Provide relevant resources based on the situation

---

## Base URL

**Local:**
```
http://localhost:5000
```

**Live:**
```
https://pink-reciept-api-sage.vercel.app/
```

---

## Endpoint

### `POST /`

Analyzes an image screenshot for harassment detection.

**Request**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: image file (JPEG, PNG, etc.)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| image | file | ✅ Yes | Screenshot of the message to analyze |

---

## Testing with Postman

1. Open Postman and create a new request
2. Set method to **POST**
3. Enter the URL: `https://pink-reciept-api-sage.vercel.app/`
4. Click **Body** → select **form-data**
5. Add a key called `image`, change the type to **File**
6. Upload your screenshot
7. Click **Send**

---

## Testing with cURL

```bash
curl -X POST https://pink-reciept-api-sage.vercel.app/ \
  -F "image=@/path/to/screenshot.jpg"
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

## Error Responses

| Status Code | Meaning |
|-------------|---------|
| 400 | No file uploaded or no file selected |
| 500 | Server error |

**Example error response:**
```json
{
  "error": "No file uploaded"
}
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/MoonRock404/PinkRecieptAPI
cd PinkRecieptAPI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file**
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
```

**4. Run the app**
```bash
python api/app.py
```

**5. Test it**
```bash
curl -X POST http://localhost:5000/ \
  -F "image=@/path/to/screenshot.jpg"
```

---

## Tech Stack

- **Python** + **Flask** — API framework
- **Google Gemini 2.5 Flash** — AI model for harassment detection
- **Vercel** — Hosting

---
