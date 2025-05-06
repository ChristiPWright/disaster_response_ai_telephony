import os

from flask import Flask, request, session, Response
from flask_session import Session
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["SESSION_TYPE"] = "filesystem"  # In prod: use 'redis'
Session(app)

#init state object -> TODO abstract out
call_state = {
        "step": 0,
        "name": "",
        "dob": "",
        "insurance": "",
        "payer_id": "",
        "referral": "",
        "physician": "",
        "complaint": "",
        "address": "",
        "phone": "",
        "email": "",
        "appointment": ""
    }

# start call
@app.route("/start_call", methods=["POST"])
def start_call():
    # Initial Twilio webhook
    call_sid = request.form.get("CallSid")
    print(f"Incoming call: {call_sid}")
    session[call_sid] = call_state

    response = VoiceResponse()

    response.say("Hi! I'm your virtual assistant. Let's get started.")
    response.gather(input="speech", action="/gather", method="POST", timeout=5)

    return Response(str(response), mimetype="application/xml")

# speech input
@app.route("/gather", methods=['POST'])
def gather():
    #Process speech input
    call_sid = request.form.get("CallSid")
    transcript = request.form.get("SpeechResult", "")
    print(f"User said: {transcript}")
    gather_call_state = session.get(call_sid, {})

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