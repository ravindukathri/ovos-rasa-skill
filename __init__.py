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
            
    # 
    def __init__(self, *args, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().

        This is a good place to load and pre-process any data needed by your
        Skill, ideally after the super() call.
        """
        super().__init__(*args, **kwargs)
        self.rasa_client = RasaSocketClient("http://host.docker.internal:5005")

    @property
    @intent_handler(IntentBuilder('ask_rasa').require('TalkToRasa'))
    def handle_ask_rasa_intent(self, message):
        user_utterance = message.data.get('utterance')
        rasa_response = self.rasa_client.send_to_rasa(user_utterance)
        self.speak(rasa_response)

    @intent_handler("HowAreYou.intent")
    def handle_how_are_you_intent(self, message):
        """This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak_dialog("how.are.you")

    @intent_handler(IntentBuilder("HelloWorldIntent").require("HelloWorldKeyword"))
    def handle_hello_world_intent(self, message):
        """Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        self.log.info("There are five types of log messages: " "info, debug, warning, error, and exception.")
        self.speak_dialog("hello.world")