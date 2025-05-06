import os

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# start call
@app.route("/start_call", methods=["POST"])
def start_call():
    # Initial Twilio webhook
    print("Incoming call...")

    response = VoiceResponse()

    response.say("Hi! I'm your virtual assistant. Let's get started.")
    response.gather(input="speech", action="/gather", method="POST", timeout=5)

    return Response(str(response), mimetype="application/xml")

# speech input
@app.route("/gather", methods=['POST'])
def gather():
    #Process speech input
    transcript = request.form.get("SpeechResult", "")
    print(f"User said: {transcript}")

    #TODO: AI agent logic

    #Next prompt
    response = VoiceResponse()
    response.say('Next prompt placeholder')
    response.gather(input="speech", action="/gather", method="POST", timeout=5)

    return Response(str(response), mimetype="application/xml")

# stream

# validate

# end call

if __name__ == "__main__":
    app.run(debug=True)