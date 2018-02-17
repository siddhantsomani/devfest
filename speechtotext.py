import base64
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials

speech_file = "chaiye.flac";

with open(speech_file, 'rb') as speech:
    # Base64 encode the binary audio file for inclusion in the JSON
    # request.
    speech_content = base64.b64encode(speech.read())

# Construct the request
service = googleapiclient.discovery.build('speech', 'v1');
service_request = service.speech().recognize(
    body={
        "config": {
            # "encoding": "FLAC",  # raw 16-bit signed LE samples
            "languageCode": "hi",  # a BCP-47 language tag
            "enable_word_time_offsets":True,
        },
        "audio": {
            "content": speech_content
            }
        })
res = service_request.execute();
print(type(res), res["results"][0]["alternatives"]);
print();

# for wordinfo in res["results"][0]["alternatives"][0]["words"]:
# 	print(type(wordinfo["word"]), type(wordinfo["startTime"]), wordinfo["endTime"]);

text = res["results"][0]["alternatives"][0]["transcript"];
print(text);
# exit();


# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

target = 'en'

# Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target)

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))

from gtts import gTTS;

translated = translation['translatedText'];
tts = gTTS(text=translated, lang=target, speed=1);
tts.save("outpt.mp3");