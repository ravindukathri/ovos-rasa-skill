from ovos_utils import classproperty
from ovos_workshop.skills.ovos import OVOSSkill
from ovos_workshop.decorators import intent_handler
from ovos_utils.intents import IntentBuilder
import socketio


class RasaSocketClient:
    def __init__(self, rasa_url):
        self.sio = socketio.Client()
        self.response = None

        @self.sio.event
        def connect():
            print("Connected to Rasa")

        @self.sio.event
        def disconnect():
            print("Disconnected from Rasa")

        @self.sio.event
        def bot_uttered(data):
            self.response = data['text']

    def send_to_rasa(self, message):
        self.response = None
        self.sio.emit('user_uttered', {'message': message})
        while self.response is None:
            pass
        return self.response


class OVOSRasaSkill(OVOSSkill):
    
    
    def initialize(self):
    
        self.rasa_client = RasaSocketClient("http://host.docker.internal:5005")

    @property
    @intent_handler(IntentBuilder('AskRasaIntent').require('TalkToRasa'))
    def handle_ask_rasa_intent(self, message):
        self.log.info("Connecting to RASA !!!! LOG MESSAGE")
        user_utterance = message.data.get('utterance')
        rasa_response = self.rasa_client.send_to_rasa(user_utterance)
        self.speak(rasa_response)

    
    @intent_handler(IntentBuilder("HelloRasaIntent").require("HelloRasaKeyword"))
    def handle_hello_world_intent(self, message):
        """Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        self.log.info("RASA TEST INTENT IS WORKING!!!!!")
        self.speak_dialog("hello.rasa")

        pass
