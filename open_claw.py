import pyttsx3

def say_open_claw():
    """
    Script to say 'Open claw' using text-to-speech.
    """
    engine = pyttsx3.init()
    engine.say('Open clawwww')
    engine.runAndWait()

if __name__ == '__main__':
    say_open_claw()
