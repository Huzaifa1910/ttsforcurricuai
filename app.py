from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import dotenv
import azure.cognitiveservices.speech as speechsdk

dotenv.load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/synthesize_speech', methods=['GET','POST'])
def synthesize_speech():
    try:
        request_data = request.get_json()
        print(request_data['prompt'])
        # Read values from environment variables
        speech_key = os.getenv('SPEECH_KEY')
        service_region = os.getenv('SERVICE_REGION')

        # Create speech config
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-US-AvaNeural"

        text = request_data['prompt']

        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        # Synthesize speech
        result = speech_synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return jsonify({"result": "Speech synthesized for text: {}".format(text)})
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return jsonify({"error": "Speech synthesis canceled", "details": cancellation_details.reason})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="localhost",port=5000, debug=True)