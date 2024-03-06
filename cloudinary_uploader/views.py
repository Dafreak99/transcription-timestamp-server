from django.shortcuts import render
from django.http import JsonResponse
from cloudinary.uploader import upload
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

def make_fetch_request(url, headers, method='GET', data=None):
    if method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

@csrf_exempt
def upload_file(request):
  if request.method == 'POST':
    uploaded_file = request.FILES.get('file')

    if uploaded_file:
      # Upload file to Cloudinary
      result = upload(uploaded_file, use_filename=True, resource_type = "video")
      public_url = result.get('url')

      gladia_url = "https://api.gladia.io/v2/transcription/"
      request_data = { "audio_url": public_url }

      headers = {
          "x-gladia-key": os.getenv("GLADIA_API_KEY"),
          "Content-Type": "application/json"
      }

      print("- Sending initial request to Gladia API...")
      # Get transcription from Gladia
      initial_response = make_fetch_request(gladia_url, headers, 'POST', request_data)

      print("Initial response with Transcription ID:", initial_response)
      result_url = initial_response.get("result_url")

      # Polling until transcription is done
      if result_url:
        while True:
            print("Polling for results...")
            poll_response = make_fetch_request(result_url, headers)
            
            if poll_response.get("status") == "done":
                print("- Transcription done: \n")
                print(poll_response)
                return JsonResponse(poll_response)
            else:
                print("Transcription status:", poll_response.get("status"))
            time.sleep(1)
      
    else:
      return JsonResponse({'error': 'No file uploaded'}, status=400)
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

