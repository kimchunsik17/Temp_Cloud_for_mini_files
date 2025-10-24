from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.cache import cache
from .models import UploadedFile, GlobalSettings
import os
import uuid
import urllib.parse

ADMIN_SECRET_PHRASE = b"admin_access_granted"

# Create your views here.

def index_view(request):
    # Logic for receiving and validating file ID and password will go here
    return render(request, 'cloud_storage/index.html')

def upload_view(request):
    if request.method == 'POST':
        settings = GlobalSettings.load()
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')

        if uploaded_file:
            uploaded_file.seek(0)
            file_content_bytes = uploaded_file.read()
            if file_content_bytes == ADMIN_SECRET_PHRASE:
                request.session['is_admin'] = True
                return redirect('cloud_storage:admin_page')
            uploaded_file.seek(0)

        if uploaded_file and password and len(password) == 4:
            ip_address = request.META.get('REMOTE_ADDR')
            if not ip_address:
                ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

            if uploaded_file.size > settings.max_file_size:
                return render(request, 'cloud_storage/upload.html', {'error': f'파일 크기가 {settings.max_file_size / (1024 * 1024):.0f}MB를 초과합니다.'})

            if ip_address and UploadedFile.objects.filter(ip_address=ip_address).count() >= settings.max_files_per_ip:
                return render(request, 'cloud_storage/upload.html', {'error': f'IP당 업로드 가능한 파일 개수({settings.max_files_per_ip}개)를 초과했습니다.'})

            if UploadedFile.objects.count() >= settings.max_total_files:
                return render(request, 'cloud_storage/upload.html', {'error': f'서버에 업로드 가능한 최대 파일 개수({settings.max_total_files}개)를 초과했습니다.'})

            file_id = str(uuid.uuid4())[:10]
            UploadedFile.objects.create(
                file=uploaded_file,
                password=password,
                file_id=file_id,
                ip_address=ip_address
            )
            return render(request, 'cloud_storage/upload.html', {'file_id': file_id})
        else:
            return render(request, 'cloud_storage/upload.html', {'error': 'Invalid file or password.'})
    return render(request, 'cloud_storage/upload.html')

def download_view(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        password = request.POST.get('password')

        ip_address = request.META.get('REMOTE_ADDR')
        if not ip_address:
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

        if ip_address:
            failed_attempts_key = f'failed_attempts_{ip_address}'
            failed_attempts = cache.get(failed_attempts_key, 0)

            if failed_attempts >= 5:
                return render(request, 'cloud_storage/index.html', {'error': '너무 많은 시도를 하셨습니다. 5분 후에 다시 시도해주세요.'})

        try:
            uploaded_file_obj = UploadedFile.objects.get(file_id=file_id)
        except UploadedFile.DoesNotExist:
            return render(request, 'cloud_storage/index.html', {'error': '잘못된 파일 번호입니다.'})

        if uploaded_file_obj.password == password:
            if ip_address:
                cache.delete(f'failed_attempts_{ip_address}')

            file_path = uploaded_file_obj.file.path
            file_name = os.path.basename(uploaded_file_obj.file.name)
            encoded_file_name = urllib.parse.quote(file_name.encode('utf-8'))
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_file_name}"
                return response
        else:
            if ip_address:
                failed_attempts = cache.get(failed_attempts_key, 0)
                cache.set(failed_attempts_key, failed_attempts + 1, timeout=300) # 5 minutes
            return render(request, 'cloud_storage/index.html', {'error': '파일 번호 또는 비밀번호가 잘못되었습니다.'})
            
    return redirect('cloud_storage:index')

def admin_page_view(request):
    if not request.session.get('is_admin'):
        return redirect('cloud_storage:index')

    settings = GlobalSettings.load()

    if request.method == 'POST':
        max_size_mb = request.POST.get('max_file_size')
        max_files = request.POST.get('max_files_per_ip')
        auto_delete_days = request.POST.get('auto_delete_days')
        
        if max_size_mb:
            settings.max_file_size = int(max_size_mb) * 1024 * 1024
        if max_files:
            settings.max_files_per_ip = int(max_files)
        if auto_delete_days is not None:
            settings.auto_delete_days = int(auto_delete_days)
        
        max_total_files = request.POST.get('max_total_files')
        if max_total_files is not None:
            settings.max_total_files = int(max_total_files)

        settings.save()
        return redirect('cloud_storage:admin_page')

    uploaded_files = UploadedFile.objects.all().order_by('-created_at')
    context = {
        'uploaded_files': uploaded_files,
        'max_file_size_mb': settings.max_file_size / (1024 * 1024),
        'max_files_per_ip': settings.max_files_per_ip,
        'auto_delete_days': settings.auto_delete_days,
        'max_total_files': settings.max_total_files,
    }
    return render(request, 'cloud_storage/admin_page.html', context)

def delete_file_view(request, file_id):
    if not request.session.get('is_admin'):
        return redirect('cloud_storage:index')
    if request.method == 'POST':
        uploaded_file_obj = get_object_or_404(UploadedFile, file_id=file_id)
        # Delete file from filesystem
        if os.path.exists(uploaded_file_obj.file.path):
            os.remove(uploaded_file_obj.file.path)
        uploaded_file_obj.delete() # Delete from database
    return redirect('cloud_storage:admin_page')

def logout_view(request):
    request.session['is_admin'] = False
    return redirect('cloud_storage:index')

def about_view(request):
    return render(request, 'cloud_storage/about.html')
