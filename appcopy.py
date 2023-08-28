import os
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify

# Setting the path to the ffmpeg and ffprobe executables
sr.AudioFile.converter = "/usr/local/bin/ffmpeg"
sr.AudioFile.ffmpeg = "/usr/local/bin/ffmpeg"
sr.AudioFile.ffprobe = "/usr/local/bin/ffprobe"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile(filename) as source:
        audio_text = r.record(source)

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition for English
        text_en = r.recognize_google(audio_text, language='en-IN')

        # using google speech recognition for Hindi
        text_hi = r.recognize_google(audio_text, language='hi-IN')

        # Create the output containing the English and Hindi text
        bilingual_output = {
            'English': text_en,
            'Hindi': text_hi
        }

        return jsonify({'result': bilingual_output})
    except:
        return jsonify({'result': 'Sorry, I did not get that'})

if __name__ == '__main__':
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

