# Pink Receipt API

An AI-powered harassment detection API that analyzes screenshots of messages and returns a structured assessment of whether the content is concerning, along with options and resources for the potential victim.

---

## What It Does

The user can send screenshot of a conversation to the API and it will:
- Detect whether the message contains harassment or abusive language
- Classify the severity (low, medium, high)
- Provide options and relevant resources based on the situation

---


## Live API
```
https://pink-reciept-api-sage.vercel.app/
```

---

## API REFERENCE
### `POST /`

Analyzes an image screenshot for harassment detection.

**Request**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: image file (JPEG, PNG, etc.)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| image | file | Yes | Screenshot of the message to analyze |

---

## Authentication

This API is currently open and does not require authentication. 
Any user with the endpoint URL can send requests directly.

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

## Error Handling

The API returns informative error messages with appropriate HTTP status codes.

| Status Code | Meaning | Example Response |
|-------------|---------|-----------------|
| `200` | Success | Full JSON analysis |
| `400` | Bad request | `{"error": "No file uploaded"}` |
| `400` | Bad request | `{"error": "No file selected"}` |
| `500` | Failed to parse Gemini response | `{"error": "Failed to parse Gemini response: <details>"}` |
| `500` | General server error | `{"error": "error details here"}` |

**Troubleshooting:**
- Make sure the form field is named exactly `image`
- Make sure you are uploading an actual image file (only JPEG and PNG)
- If you get `Failed to parse Gemini response` — the AI returned an unexpected format, try again with a clearer screenshot
- If you get a general 500 error, check that your file is not corrupted

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
