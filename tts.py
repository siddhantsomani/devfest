# Imports the Google Cloud client library
from google.cloud import translate
text = "There is Oprah Winfrey. There's also eyewear."
# Instantiates a client , text to speech starts here
translate_client = translate.Client()

target = 'en'

# Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target) #target language code

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))

from gtts import gTTS;

translated = translation['translatedText'];
tts = gTTS(text=translated, lang=target, speed=1);
tts.save("oprah.mp3"); #TTS here
# TTS ends here