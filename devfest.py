import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'duke_monkey.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

#Performs face detection on the image file
response = client.face_detection(image=image)
faces = response.face_annotations

#Performs logo detection on the image file
response = client.logo_detection(image=image)
logos = response.logo_annotations

web_detection = client.web_detection(image=image).web_detection

response = client.text_detection(image=image)
texts = response.text_annotations

web_str = ''
if web_detection.web_entities:
	web_str += 'There is '+web_detection.web_entities[0].description+'.'

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
face_str = ''
if len(faces)>0:
	face_dict = {'anger' : likelihood_name[faces[0].anger_likelihood], 'joy' : likelihood_name[faces[0].joy_likelihood], 'surprise' : likelihood_name[faces[0].surprise_likelihood], 'sorrow' : likelihood_name[faces[0].sorrow_likelihood]}
	face_list = []
	face_list.append([faces[0].anger_likelihood, faces[0].joy_likelihood, faces[0].surprise_likelihood, faces[0].sorrow_likelihood])
	max_index = face_list[0].index(max(face_list[0]))
	face_dict = {0 : 'anger', 1 : 'joy', 2 : 'surprise', 3: 'sorrow'}
	mood = face_dict[max_index]
	if max(face_list[0])>=3:
		face_str += 'The mood of the person is '+mood+'.'
labels_str = ''
if len(labels)>0:
	labels_str += 'There is '+labels[0].description+'.'
if len(labels)>1:
	labels_str += ' There\'s also '+labels[1].description+'.' 
logos_str = ''
if len(logos)>0:
	logos_str += 'It has '+logos[0].description+'.'
text_str = ''
if len(texts)>0:
	text_str += texts[0].description+' is written in this frame .'
string  = logos_str+labels_str+text_str+face_str
print(string)