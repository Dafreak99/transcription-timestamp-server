from django.shortcuts import render

from django.http import JsonResponse
from cloudinary.uploader import upload
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_file(request):
  if request.method == 'POST':
    print('hello')
    uploaded_file = request.FILES.get('file')

    if uploaded_file:
      # Upload file to Cloudinary
      print(request.FILES.get('file'))
      result = upload(uploaded_file, use_filename=True, resource_type = "video")
      public_url = result.get('url')

      # Optionally save information to the model
      # uploaded_file_obj = UploadedFile.objects.create(
      #   file_name=uploaded_file.name,
      #   public_url=public_url,
      # )


      return JsonResponse({'public_url': public_url})
    else:
      return JsonResponse({'error': 'No file uploaded'}, status=400)
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)
