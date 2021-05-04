from django.shortcuts import render, redirect
from django.core import management

def item_list(request):
    if request.method == 'POST':
        url = request.POST['mytextbox']
        management.call_command('parse_avito', f'{url}')
        print(url)
        return render(request, "home.html")
    else:
        return render(request, "home.html")
