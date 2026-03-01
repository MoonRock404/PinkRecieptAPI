import os
import json
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__, template_folder="../templates")
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# get the gemini API key
GEN_KEY = os.environ.get("GEMINI_API_KEY")
if not GEN_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEN_KEY)
MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash")

# front-end dsiplac
@app.route("/", methods=["GET"])
def index():
    """Serve upload page."""
    return render_template("index.html")

# endpoint for analyzing the image and returning harassment detection results
@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze uploaded image for harassment detection."""
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    image_bytes = image_file.read()
    mime_type = image_file.content_type or "image/jpeg"

    prompt = """
    Analyze this screenshot for harassment detection.
    Return ONLY valid JSON (no markdown, no explanation) in this format:
    {
        "is_concerning": true,
        "severity": "low|medium|high",
        "summary": "brief explanation",
        "options": ["option 1", "option 2"],
        "resources": ["resource 1", "resource 2"]
    }
    """

    model = genai.GenerativeModel(MODEL_NAME)

    try:
        response = model.generate_content(
            contents=[
                prompt,
                {"mime_type": mime_type, "data": image_bytes}
            ]
        )
        # clean response to get rid of '''
        raw_text = response.text.strip()
        clean_text = re.sub(r"^```(?:json)?\s*|```$", "", raw_text, flags=re.MULTILINE).strip()

        try:
            data = json.loads(clean_text)
            return jsonify(data), 200
        except json.JSONDecodeError:
            return jsonify({
                "error": "Invalid JSON from Gemini",
                "raw_response": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endpoint for generating a harassment report based on user input
@app.route("/report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        platform = data.get("platform")
        severity = data.get("severity")
        summary = data.get("summary")
        options = data.get("options", [])
        resources = data.get("resources", [])

        if not all([platform, severity, summary]):
            return jsonify({"error": "Missing required fields: platform, severity, summary"}), 400

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Generate a formal harassment report that a victim can copy and submit to {platform}.

        Use the following details:
        - Severity: {severity}
        - Summary: {summary}
        - Recommended options: {', '.join(options)}
        - Resources: {', '.join(resources)}

        Write it in a clear, professional tone. Include:
        1. A brief description of the incident
        2. Why it is considered harassment
        3. What action is being requested from {platform}
        4. Any relevant resources or next steps for the victim

        Return ONLY the report text, no extra explanation.
        """

        response = model.generate_content(prompt)
        return jsonify({"report": response.text.strip()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500