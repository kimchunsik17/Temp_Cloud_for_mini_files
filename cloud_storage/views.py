from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import UploadedFile
import uuid

ADMIN_SECRET_PHRASE = "admin_access_granted"

# Create your views here.

def index_view(request):
    # Logic for receiving and validating file ID and password will go here
    return render(request, 'cloud_storage/index.html')

def upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')

        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')
            if file_content == ADMIN_SECRET_PHRASE:
                return redirect('cloud_storage:admin_page')

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
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=' + uploaded_file_obj.file.name
                return response
        else:
            return render(request, 'cloud_storage/index.html', {'error': 'Invalid file ID or password.'})
    return redirect('cloud_storage:index')

def admin_page_view(request):
    uploaded_files = UploadedFile.objects.all().order_by('-created_at')
    return render(request, 'cloud_storage/admin_page.html', {'uploaded_files': uploaded_files})
