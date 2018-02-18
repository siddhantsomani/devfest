import base64
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import io
import os

def videoToAudio(fileName):
    # flac: ffmpeg -i NLP.mp3 fileout.flac
    # mp3: ffmpeg -i NLP.mp4 -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 audio.mp3
    if(fileName.find(".")<0):
        fileName = fileName+".mp4"
    os.system("ffmpeg -i "+fileName+" -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 " + fileName[:-4] + ".mp3")
    print("ffmpeg -i "+fileName+" -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 " + fileName[:-4] + ".mp3")
    os.system("ffmpeg -i " + fileName[:-4] + ".mp3 " + ""+fileName[:-4]+".flac")
    print("ffmpeg -i " + fileName[:-4] + ".mp3 " + " "+fileName[:-4]+".flac")
    os.system("ffmpeg -i " + fileName[:-4] + ".flac -ac 1 " + ""+fileName[:-4]+"final.flac")
    outputFileName = fileName[:-4]+"final.flac"
    return outputFileName

speech_file = "nlp2.flac";
mp4_file = "Vo.mp4"
speech_file = videoToAudio(mp4_file)
output_mp4_file = "output.mp4"


client = speech.SpeechClient()

# [START migration_async_request]
with io.open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

audio = types.RecognitionAudio(content=content)
config = types.RecognitionConfig(
    # encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    enable_word_time_offsets=True,
    language_code='en-US')

# [START migration_async_response]
operation = client.long_running_recognize(config, audio)
# [END migration_async_request]

print('Waiting for operation to complete...')
response = operation.result(timeout=90)

texts = [];
# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print('Transcript: {}'.format(result.alternatives[0].transcript))
    texts.append(result.alternatives[0].transcript);
    print('Confidence: {}'.format(result.alternatives[0].confidence))
#Another paramter for word(and start time/end time)
# [END migration_async_response]


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
            "languageCode": "en",  # a BCP-47 language tag
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
print(texts[0]);
# exit();


# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client , text to speech starts here
translate_client = translate.Client()

target = 'ES'

# Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target) #target language code

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))

from gtts import gTTS;

translated = translation['translatedText'];
tts = gTTS(text=translated, lang=target, speed=1);
tts.save("outpt.mp3"); #TTS here
# TTS ends here
import os;
def joinTwoFiles(file1,file2):
    os.system("rm file1.mp3");
    os.system("rm file2.mp3");
    os.system("ffmpeg -i " + file1 + " -ar 44100 file1.mp3")
    os.system("ffmpeg -i " + file2 + " -ar 44100 file2.mp3")
    os.system("cat file1.mp3 file2.mp3 > "+file1);
    os.system("rm file1.mp3");
    os.system("rm file2.mp3");

n = len(texts);
for i in range(n-1):
    text = texts[i+1];
    translation = translate_client.translate(
        text,
        target_language=target)
    from gtts import gTTS;

    translated = translation['translatedText'];
    tts = gTTS(text=translated, lang=target, speed=1);
    tts.save("temp.mp3");
    joinTwoFiles("outpt.mp3", "temp.mp3");


# os.system("rm " + output_mp4_file);
os.system("ffmpeg -i " + mp4_file + " -i outpt.mp3 -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 " + output_mp4_file);
