import os
from dotenv import load_dotenv
import requests

# pip install streamlit, requests, python-dotenv

# helper funtion 1 - Uploading a local audio file to AssemblyAI
def get_url(token,data):
    '''
    Parameter:
    token: The API key
    data : The File Object to upload
    Return Value:
    url : Url to uploaded file
    '''
    headers = {'authorization': token}
    response = requests.post('https://api.assemblyai.com/v2/upload',
    headers=headers,
    data=data)
    url = response.json()["upload_url"]
    print("Uploaded File and got temporary URL to file")
    return url
    
# helper function 2 - Uploading a file for transcription
def get_transcribe_id(token,url):
    '''
    Parameter:
    token: The API key
    url : Url to uploaded file
    Return Value:
    id : The transcribe id of the file
    '''
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
    "audio_url": url
    }
    headers = {
    "authorization": token,
    "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    id = response.json()['id']
    print("Made request and file is currently queued")
    return id
    
# helper function 3 - downloading an audio transcription
def get_text(token,transcribe_id):
    '''
    Parameter:
    token: The API key
    transcribe_id: The ID of the file which is being
    Return Value:
    result : The response object
    '''
    endpoint= f"https://api.assemblyai.com/v2/transcript/{transcribe_id}"
    headers = {
    "authorization": token
    }
    result = requests.get(endpoint, headers=headers).json()
    return result
    
# helper function 4 - Requesting a transcription from the UI
def upload_file(fileObj):
    '''
    Parameter:
    fileObj: The File Object to transcribe
    Return Value:
    token : The API key
    transcribe_id: The ID of the file which is being transcribed
    '''
    load_dotenv()
    token = os.getenv("API_TOKEN")
    file_url = get_url(token,fileObj)
    transcribe_id = get_transcribe_id(token,file_url)
    return token,transcribe_id
