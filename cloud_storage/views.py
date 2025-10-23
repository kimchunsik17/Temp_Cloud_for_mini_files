from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import UploadedFile
import uuid
import os
import urllib.parse

ADMIN_SECRET_PHRASE = b"admin_access_granted"

# Create your views here.

def index_view(request):
    # Logic for receiving and validating file ID and password will go here
    return render(request, 'cloud_storage/index.html')

def upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')

        if uploaded_file:
            # Reset file pointer to the beginning after reading for admin check
            uploaded_file.seek(0)
            file_content_bytes = uploaded_file.read()
            if file_content_bytes == ADMIN_SECRET_PHRASE:
                return redirect('cloud_storage:admin_page')
            # Reset file pointer again for potential re-reading by FileField
            uploaded_file.seek(0)

        if uploaded_file and password and len(password) == 4:
            ip_address = request.META.get('REMOTE_ADDR')
            if not ip_address:
                ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

            file_id = str(uuid.uuid4())[:10]  # Generate a unique 10-character file ID
            UploadedFile.objects.create(
                file=uploaded_file,
                password=password,
                file_id=file_id,
                ip_address=ip_address
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
            encoded_file_name = urllib.parse.quote(file_name.encode('utf-8'))
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f'attachment; filename*=UTF-8'''{encoded_file_name}'
                return response
        else:
            return render(request, 'cloud_storage/index.html', {'error': 'Invalid file ID or password.'})
    return redirect('cloud_storage:index')

def admin_page_view(request):
    uploaded_files = UploadedFile.objects.all().order_by('-created_at')
    return render(request, 'cloud_storage/admin_page.html', {'uploaded_files': uploaded_files})

def delete_file_view(request, file_id):
    if request.method == 'POST':
        uploaded_file_obj = get_object_or_404(UploadedFile, file_id=file_id)
        # Delete file from filesystem
        if os.path.exists(uploaded_file_obj.file.path):
            os.remove(uploaded_file_obj.file.path)
        uploaded_file_obj.delete() # Delete from database
    return redirect('cloud_storage:admin_page')
