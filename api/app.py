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
1. Change the prompt to reflect our current vision (refer to whiteboard photo) ✅
    1a. check if message is concerning ✅
    1b. provide user with OPTIONS not solutions ✅
    1c. provide user with resources ✅
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
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/", methods=["POST"])
def analyze():
    try: 
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        image_file = request.files.get("image")

        if image_file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        image_bytes = image_file.read()
        mime_type = image_file.content_type or "image/jpeg"

        model = genai.GenerativeModel("gemini-2.0-flash")

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

        image_part = {"mime_type": mime_type, "data": image_bytes}
        response = model.generate_content([prompt, image_part])

        data = json.loads(raw)
        return jsonify(data), 200

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to parse Gemini response: {str(e)}", "raw": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__": 
    app.run(debug=True)