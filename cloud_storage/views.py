from django.shortcuts import render

# Create your views here.

def index_view(request):
    # Logic for receiving and validating file ID and password will go here
    return render(request, 'cloud_storage/index.html')
