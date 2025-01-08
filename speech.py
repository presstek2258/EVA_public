from gtts import gTTS
import subprocess
from time import sleep

class TTS:

    def __init__(self) -> None: #initlializes parameters for text to speech
        self.audio_file = "gtts.wav"
        self.language = "en" #language set to english

    def speak(self,message):
        # gtts - generates an audio file from a string
        speech = gTTS(message, lang=self.language)
        speech.save(self.audio_file) #saves an wav of the tts

        #using mpg123 command ##WORKING
        command = ['mpg123', self.audio_file] #mgp123 for high quality, mpg321 for quicker
        with open('/dev/null', 'w') as null: #/dev/null is a linux command to get rid of what outputs to terminal everytime mpg123 runs
                                            # it writes to a file that doesn't exist, whihc is why 'w parameter
            subprocess.run(command, check=True, stdout=null, stderr=null)


    # use this for testing without the mpg123 (for windows tkinter testing)
    # def speak(self,message): sleep(1)
        
