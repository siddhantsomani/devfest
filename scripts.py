import os
from google.cloud import storage

def videoToAudio(fileName):
    # flac: ffmpeg -i NLP.mp3 fileout.flac
    # mp3: ffmpeg -i NLP.mp4 -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 audio.mp3
    if(fileName.find(".")<0):
        fileName = fileName+".mp4"
    os.system("ffmpeg -i "+fileName+" -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 " + fileName[:-4] + ".mp3")
    print("ffmpeg -i "+fileName+" -vn -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 " + fileName[:-4] + ".mp3")
    os.system("ffmpeg -i " + fileName[:-4] + ".mp3 -ac 1 " + " flac "+fileName[:-4]+".flac")
    print("ffmpeg -i " + fileName[:-4] + ".mp3 -ac 1 " + " "+fileName[:-4]+".flac")
    outputFileName = fileName[:-4]+".flac"
    return outputFileName

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json('devfest.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


if __name__ == "__main__":
    # videoToAudio("/Users/Siddhant/Desktop/NLP.mp4")
    upload_blob(bucket_name="devfest-devfest", source_file_name="/Users/Siddhant/Desktop/NLP.mp4", destination_blob_name="nlpp.mp4")







# def uploadMedia(fileName):
#     client = storage.Client()
#     bucket = client.get_bucket('devfest-devfest')
#     blob = bucket.get_blob('/Users/Siddhant/Desktop/bond.png')
#     print(blob.download_as_string())
#     blob.upload_from_string('New contents!')
#     blob2 = bucket.blob('remote/path/storage.txt')
#     blob2.upload_from_filename(filename='/local/path.txt')
#     return urlToAccess

# def upload_image_file(file):
#     """
#     Upload the user-uploaded file to Google Cloud Storage and retrieve its
#     publicly-accessible URL.
#     """
#     if not file:
#         return None
#
#     public_url = storage.upload_file(
#         file.read(),
#         file.filename,
#         file.content_type
#     )
#
#     # current_app.logger.info(
#     #     "Uploaded file %s as %s.", file.filename, public_url)
#
#     return public_url
