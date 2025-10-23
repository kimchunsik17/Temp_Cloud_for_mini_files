from django.shortcuts import render, redirect
from .models import UploadedFile
import uuid

# Create your views here.

def index_view(request):
    # Logic for receiving and validating file ID and password will go here
    return render(request, 'cloud_storage/index.html')

def upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')

        if uploaded_file and password and len(password) == 4:
            file_id = str(uuid.uuid4())[:10]  # Generate a unique 10-character file ID
            UploadedFile.objects.create(
                file=uploaded_file,
                password=password,
                file_id=file_id
            )
            return render(request, 'cloud_storage/upload.html', {'file_id': file_id})
        else:
            # Handle invalid input (e.g., no file, no password, password not 4 digits)
            return render(request, 'cloud_storage/upload.html', {'error': 'Invalid file or password.'})
    return render(request, 'cloud_storage/upload.html')
