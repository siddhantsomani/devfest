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

# The text to translate
# text = u'Hello world'
# The target language
target = 'en'

# Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target)

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))



import urllib;
import urllib2;
from gtts import gTTS;

translated = translation['translatedText'];
tts = gTTS(text=translated, lang=target, speed=1);
tts.save("outpt.mp3");

# # https://translate.google.com/translate_tts?ie=UTF-8&q=%E0%A4%A8%E0%A4%AE%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%87%20%E0%A4%A6%E0%A5%81%E0%A4%A8%E0%A4%BF%E0%A4%AF%E0%A4%BE&tl=hi&total=1&idx=0&textlen=13&tk=22034.402958&client=t&ttsspeed=0.24

# print(translated);
# # translated = "hello world";
# # print(urllib.urlencode(translated, 'utf-8'))

# args = {'q':translated, 'ie':'UTF-8', 'tl':target,'total':1, 'idx':0, 'textlen':13, 'tk':22034.402958,'client':'t','ttsspeed':0.24};

# args = urllib.urlencode(args, 'utf-8');

# urlfortranslate = u"https://translate.google.com/translate_tts?{}".format(args);
# urlfortranslate = 'https://translate.google.com/translate_tts?ie=UTF-8&q=Hello%20world&tl=en&total=1&idx=0&textlen=11&tk=737657.864613&client=t'
# print(urlfortranslate);
# # print(required_url);

# filedata = urllib2.urlopen(urlfortranslate)  
# datatowrite = filedata.read()

# with open('converted.mp3', 'wb') as f:  
#     f.write(datatowrite)
