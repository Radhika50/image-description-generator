# image-description-generator
# AI-Powered Image Description & Voice Output 

 A web-based application that leverages AI to generate meaningful captions and spoken descriptions from images. Designed with accessibility and multilingual support in mind, the system allows users to upload or capture an image, and then receive a context-rich description in **English**, **Hindi**, or **Telugu** — both as **text and audio**.

This project integrates three core technologies:

- **Computer Vision** – to understand the content of an image  
- **Natural Language Processing** – to generate and translate descriptive text  
- **Text-to-Speech synthesis** – to convert the summary into spoken voice  

---

## Key Features

✅ Accepts image input via Upload, Webcam, or URL  
✅ Generates short captions and detailed image summaries  
✅ Multilingual support: English, Hindi, and Telugu  
✅ Converts summaries into speech  
✅ Simple, accessible web interface built for ease of use  
✅ Works on local devices and cloud environments like Google Colab  

---

## How It Works

The system follows a clear and intuitive flow:  
**Image → Caption → Summary → Translation → Voice Output**

### 1. Image Input Handling
Users can provide an image through:
- Uploading a file from their computer
- Capturing a live image using a webcam
- Pasting an image URL from the web

All images are processed and saved server-side using Flask and Pillow, then converted to RGB format for consistency.

---

### 2. Caption Generation using BLIP
The image is passed to **BLIP (Bootstrapped Language-Image Pretraining)** — a vision-language AI model. It generates a short, accurate caption describing the scene.

> Example: _“A woman sitting on a bench in a park with a laptop”_

---

### 3. Language Translation with Gemini API
If the user selects Hindi or Telugu:
- The caption is translated using **Google Gemini 1.5 API**
- The system constructs a prompt to ensure a clean, direct translation  
- Any unnecessary explanations are stripped to keep output precise

---

### 4. Descriptive Image Summarization
The same image is then described in more detail using Gemini, through specially crafted prompts:

- Designed to help **visually impaired users**
- Avoids guesswork or filler content
- Provides a **natural and human-like description**

> Example: _“A man in his 30s is standing near a market stall filled with colorful fruits, smiling as he hands a customer a bag of apples.”_

---

### 5. Audio Generation using gTTS
The translated summary is converted into a downloadable `.mp3` file using **Google Text-to-Speech (gTTS)**. This enables users to **listen to the image description**.

---

### 6. Web Interface & Backend
- The **frontend** is built using **HTML, CSS, and JavaScript**, and includes webcam integration
- The **Flask backend** handles:
  - Image upload and storage
  - AI model inference
  - Translation and audio generation
  - Serving results (text + audio) back to the UI

---

## Tech Stack

| Technology            | Purpose                                 |
|-----------------------|------------------------------------------|
| **Python + Flask**    | Backend development & routing            |
| **HTML, CSS, JS**     | Frontend interface and camera support    |
| **Pillow (PIL)**      | Image loading and processing             |
| **BLIP (Salesforce)** | Caption generation via vision transformer |
| **Google Gemini API** | Language translation & description       |
| **gTTS**              | Text-to-speech audio synthesis           |

---

## Future Scope

- Support for video summarization and narration  
- Emotion-aware voice synthesis   
- Add more Indian regional language support  
- Add image enhancement and OCR-based text recognition  

---

## Step-by-Step Instructions to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/Hansini1207/AI-Powered-Image-Description-Generator.git
cd AI-Powered-Image-Description-Generator
```

### 2. Install Required Packages
Install all dependencies using the provided requirements.txt file:

```bash
pip install -r requirements.txt
```
If you don’t have a requirements.txt, you can create one with the following content:

```txt

Flask
requests
Pillow
torch
transformers
gTTS
python-dotenv
google-generativeai
```

### 3. Set Your Google Gemini API Key
Get your Google AI Studio API Key from:
👉 https://makersuite.google.com/app/apikey

Create a .env file in your project root with this content:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```
⚠️ Important: Never upload your .env file to GitHub. It contains your private API key.

### 4. Create Uploads Folder
This folder is used to store uploaded images and the generated audio files:

```bash
mkdir -p static/uploads
```

### 5. Run the App
Start the Flask application:

```bash
python app.py
```
Then open your browser and go to:

```cpp
http://127.0.0.1:5000/
```
You're ready to use the SnapNarrate!


## OUTPUT
![Screenshot 2025-05-19 211921](https://github.com/user-attachments/assets/e6f2587c-1bc0-4b9d-a120-40e865e93994)

### Uploading Image
![Screenshot 2025-05-19 212531](https://github.com/user-attachments/assets/d715097f-2904-4608-95db-bff4487c3a29)

### Image URL
![Screenshot 2025-05-19 213811](https://github.com/user-attachments/assets/4846b513-e662-47d8-b10c-3da75de99828)

### WebCam Image Input
![Screenshot 2025-05-19 214855](https://github.com/user-attachments/assets/0fa9345c-7a42-4d65-ba46-9f6cb41fa260)


![image](https://github.com/user-attachments/assets/cdb022d0-d0ca-4735-9a92-f5970e6e821e)


