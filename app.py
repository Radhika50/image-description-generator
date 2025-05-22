import os
import base64
import requests
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import torch
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in environment.")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Flask app
app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Generate caption
def generate_caption(image, language):
    from transformers import BlipProcessor, BlipForConditionalGeneration
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

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
        try:
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt])
            return response.text.strip()
        except Exception as e:
            print("Gemini API translation error:", e)
            return caption_en  # Fallback to English

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
            "ఈ చిత్రాన్ని అంధుల కోసం సరళంగా మరియు స్పష్టంగా వివరిస్తూ ఒక సంక్షిప్త వివరణ ఇవ్వండి.",
            "అవసరంలేని ఊహలు కాకుండా, చిత్రంలోని ముఖ్యమైన వివరాలను మాత్రమే వివరించండి.",
            image
        ]
    }
    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt[language])
        return response.text.strip()
    except Exception as e:
        print("Gemini API summary error:", e)
        return "Could not summarize the image."

# Convert text to speech
def text_to_speech(text, lang, filename):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except Exception as e:
        print("TTS error:", e)

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            lang = request.form.get("language", "en")
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], "input_image.jpg")
            audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "summary_audio.mp3")

            # Handle different image sources
            if "image_file" in request.files and request.files["image_file"].filename != "":
                file = request.files["image_file"]
                file.save(image_path)
            elif request.form.get("image_url"):
                url = request.form.get("image_url")
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img.save(image_path)
            elif request.form.get("webcam_image"):
                img_data = request.form.get("webcam_image").split(',')[1]
                img_bytes = base64.b64decode(img_data)
                with open(image_path, 'wb') as f:
                    f.write(img_bytes)
            else:
                return redirect(url_for("index"))

            image = Image.open(image_path).convert("RGB")
            caption = generate_caption(image, lang)
            summary = summarize_image(image, lang)

            text_to_speech(summary, lang, audio_path)

            return render_template(
                "index.html",
                image_path="uploads/input_image.jpg",
                caption=caption,
                summary=summary,
                audio_path="uploads/summary_audio.mp3"
            )

        except Exception as e:
            print("Exception in POST handler:", e)
            return f"Something went wrong: {str(e)}", 500

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
