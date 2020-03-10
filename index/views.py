from django.shortcuts import render

# Create your views here.

def index_views(request):
    if request.method == "GET":
        return render(request,'cnkicn.html')