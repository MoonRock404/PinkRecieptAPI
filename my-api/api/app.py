import os
import json
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# ----------------------------
# Setup Flask app
# ----------------------------
app = Flask(__name__, template_folder="../templates")
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------------------
# Configure Gemini API
# ----------------------------
GEN_KEY = os.environ.get("GEMINI_API_KEY")
if not GEN_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEN_KEY)
MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash")

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def index():
    """Serve upload page."""
    return render_template("index.html")

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
        # ----------------------------
        # Call Gemini API
        # ----------------------------
        response = model.generate_content(
            contents=[
                prompt,
                {"mime_type": mime_type, "data": image_bytes}  # plain dict works without types
            ]
        )

        raw_text = response.text.strip()
        # Remove ```json or ``` backticks from Gemini response
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

# ----------------------------
# Run locally
# ----------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

# # import os
# # from dotenv import load_dotenv
# # from google import genai

# # load_dotenv()

# # client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# # response = client.models.generate_content(
# #     model="gemini-2.5-flash", # Use a stable model name
# #     contents="Explain how AI works in a few words",
# # )

# # print(response.text)

# '''
# 1. Change the prompt to reflect our current vision (refer to whiteboard photo) ✅
#     1a. check if message is concerning ✅
#     1b. provide user with OPTIONS not solutions ✅
#     1c. provide user with resources ✅
# 2. Adding text box option for analysis (optional if we have time)
# 3. Add a report function with a placeholder (optional)
# 4. Make our thing into an API  
#     4a. figuring out cURL/POSTMAN commands
#     4b. finishing all aspects of the documentation
# 5. Submit by 6 AM on Sunday!
# 6. Practice pitch and change name for the project
#     6a. wear pink! 🎀
# '''

# import os
# import json
# from flask import Flask, jsonify, render_template, request, render_template_string
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# load_dotenv()

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Initialize the modern Client
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     if 'image' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     image_file = request.files['image']
#     if image_file.filename == '':
#         return jsonify({"error": "No file selected"}), 400

#     # Save image
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
#     image_file.save(image_path)

#     # Prepare the prompt for harassment detection
#     prompt = """ 
#     Return this response to this prompt in HTML code.
#     Do NOT include markdown code blocks (like ```html). 
#     Analyze this screenshot for harassment detection.

#     Tasks:
#     1. Check if message is concerning and contains any abusive or harassing language categorizing it by severity level.
#     2. Provide user with OPTIONS not solutions.
#     3. Provide user with resources based on their situation.

#     The response (which is the HTML code) should return whether the message is considered harassment or not, options for the possible victim (if applicable), and resources they can reach out to.
#     Please keep the response polite as it is a sensitive subject. 
   
#     """

#     with open(image_path, "rb") as f:
#         image_bytes = f.read()

#         response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=[
#                 prompt,
#                 types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
#             ],
#             config=types.GenerateContentConfig(
#             #     response_mime_type="application/json", # Forces JSON output
#                 temperature=0.2
#             )
#         )

#         # Parse the JSON response
#         analysis_text = response.text  # just the plain text output
#         return render_template_string(analysis_text)

# if __name__ == '__main__':
#     app.run(debug=True)
