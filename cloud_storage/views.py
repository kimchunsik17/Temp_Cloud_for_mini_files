from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import UploadedFile
import uuid
import os

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

def download_view(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        password = request.POST.get('password')

        uploaded_file_obj = get_object_or_404(UploadedFile, file_id=file_id)

        if uploaded_file_obj.password == password:
            file_path = uploaded_file_obj.file.path
            file_name = os.path.basename(uploaded_file_obj.file.name)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename="%s"' % file_name
                return response
        else:
            return render(request, 'cloud_storage/index.html', {'error': 'Invalid file ID or password.'})
    return redirect('cloud_storage:index')
