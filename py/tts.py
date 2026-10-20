
from gtts import gTTS
from pathlib import Path
import os
import logging

import utl


def say(text, config):

    utl.prepareFolder(config['cache'])
    fileName = config['cache']+"/tmp.mp3"

    print ("... rendering auido. please wait ")
    if (config['ttsEngine'] == 'google'):
        logging.info("rendering via google "+ fileName)
        tts = gTTS(text=text.replace("*", ""), lang='en', slow=False, tld=config['slang'])
        tts.save(fileName)

    logging.info("saying "+ fileName)
    print("... saying (CTRL+C to interrupt)")
    os.system("mpg123 -q "+fileName)

