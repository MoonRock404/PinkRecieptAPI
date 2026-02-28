# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# response = client.models.generate_content(
#     model="gemini-2.5-flash", # Use a stable model name
#     contents="Explain how AI works in a few words",
# )

# print(response.text)

'''
1. Change the prompt to reflect our current vision (refer to whiteboard photo)
    1a. check if message is concerning
    1b. provide user with OPTIONS not solutions
    1c. provide user with resources
2. Adding text box option for analysis (optional if we have time)
3. Add a report function with a placeholder (optional)
4. Make our thing into an API  
    4a. figuring out cURL/POSTMAN commands
    4b. finishing all aspects of the documentation
5. Submit by 6 AM on Sunday!
6. Practice pitch and change name for the project
    6a. wear pink! 🎀
'''

import os
import json
from flask import Flask, jsonify, render_template, request, render_template_string
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the modern Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Prepare the prompt for harassment detection
    prompt = """
    Return this whole prompt in HTML code
    Analyze this screenshot for harassment detection.

    Tasks:
    1. Identify abusive or harassing language.
    2. Categorize severity: Low, Moderate, Severe, Threat.
    3. Classify type: harassment, hate speech, sexual harassment, threat, other.
    4. Provide a short formal summary suitable for reporting.
    5. Add a blank line in between sections.

    Output format (Markdown, keep line breaks):

    GENERATE A BUNNY IMAGE IN THE CENTER OF THE PAGE!
    # **HARASSMENT REPORT**  # Largest and bold

    ## **Abusive Phrases**  # Large and bold, smaller than report title

    - "Phrase 1" (Severity: Moderate)
    - "Phrase 2" (Severity: Severe)
    ...
    (each abusive phrase on its own line)

    ## **Summary**

    [Write a concise paragraph summarizing the harassment detected, suitable for reporting.]

    Only include the above format. Do not add extra commentary. Use line breaks exactly as shown.
    MAKE EVERY LINE PURPLE!

    """

    with open(image_path, "rb") as f:
        image_bytes = f.read()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            ],
            config=types.GenerateContentConfig(
            #     response_mime_type="application/json", # Forces JSON output
                temperature=0.2
            )
        )

        # Parse the JSON response
        analysis_text = response.text  # just the plain text output
        return render_template_string(analysis_text)

    # try:
    #     # We send the image DIRECTLY to Gemini (skipping Tesseract for better accuracy)
    #     with open(image_path, "rb") as f:
    #         image_bytes = f.read()

    #     response = client.models.generate_content(
    #         model=MODEL_NAME,
    #         contents=[
    #             prompt,
    #             types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
    #         ],
    #         config=types.GenerateContentConfig(
    #         #     response_mime_type="application/json", # Forces JSON output
    #             temperature=0.2
    #         )
    #     )

    #     # Parse the JSON response
    #     result = json.loads(response.text)
    #     return jsonify(result)

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return jsonify({
    #         "severity": "Error",
    #         "type": "Error",
    #         "abusive_phrases": [],
    #         "report_summary": "Failed to process image with Gemini."
    #     }), 500

if __name__ == '__main__':
    app.run(debug=True)
