# pip install -r requirements.txt - run at the beginning.

# app.py
import os
import base64
import requests
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port)


# Set upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Generate caption
def generate_caption(image, language):
    inputs = processor(image, return_tensors="pt").to(device)
    output = model.generate(**inputs)
    caption_en = processor.decode(output[0], skip_special_tokens=True)

    if language == "en":
        return caption_en
    else:
        prompt = (
            f"Translate the following English sentence into {'Hindi' if language == 'hi' else 'Telugu'} only. "
            "Do not include multiple options or explanations. "
            f"Sentence: {caption_en}"
        )
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt])
        return response.text.strip()
# Summarize image
def summarize_image(image, language):
    prompt = {
        "en": [
            "Summarize the image in a simple, clear, and descriptive way for visually impaired people.",
            "Avoid unnecessary imagination. Just describe the key details of the image.",
            image
        ],
        "hi": [
            "नेत्रहीनों के लिए इस छवि का सरल, स्पष्ट और वर्णनात्मक तरीके से सारांश प्रस्तुत करें।",
            "अनावश्यक कल्पना से बचें। केवल छवि के मुख्य विवरण का वर्णन करें।",
            image
        ],
        "te": [
            "ఈ చిత్రాన్ని అంధుల కోసం సరళంగా మరియు స్పష్టంగా వివరిస్తూ ఒక సంక్షిప్త వివరణ ఇవ్వండి. కేవలం విషయానికి సంబంధించిన వివరాలు మాత్రమే చెప్పండి.",
            "అవసరంలేని ఊహలు కాకుండా, చిత్రంలోని ముఖ్యమైన వివరాలను మాత్రమే వివరించండి.",
            image
        ]
    }
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt[language])
    return response.text.strip()

# Convert text to speech
def text_to_speech(text, lang, filename):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        lang = request.form.get("language", "en")
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], "input_image.jpg")
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "summary_audio.mp3")

        # 1. File Upload
        if "image_file" in request.files and request.files["image_file"].filename != "":
            file = request.files["image_file"]
            file.save(image_path)

        # 2. Image URL
        elif request.form.get("image_url"):
            url = request.form.get("image_url")
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.save(image_path)

        # 3. Webcam (Base64)
        elif request.form.get("webcam_image"):
            img_data = request.form.get("webcam_image").split(',')[1]
            img_bytes = base64.b64decode(img_data)
            with open(image_path, 'wb') as f:
                f.write(img_bytes)

        else:
            return redirect(url_for("index"))

        # Open and process the image
        image = Image.open(image_path).convert("RGB")
        caption = generate_caption(image, lang)
        summary = summarize_image(image, lang)

        # Generate and save audio
        text_to_speech(summary, lang, audio_path)

        # Pass only relative paths to template
        return render_template(
            "index.html",
            image_path="uploads/input_image.jpg",
            caption=caption,
            summary=summary,
            audio_path="uploads/summary_audio.mp3"
        )

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
