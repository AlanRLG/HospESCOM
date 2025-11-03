from django.shortcuts import render
from datetime import datetime

def index(request):
    context = {'year': datetime.now().year}
    return render(request, 'web/index.html', context)
