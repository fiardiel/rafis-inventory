from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Rafi Ardiel Erinaldi',
        'class': 'PBP Int'
    }

    return render(request, 'main.html', context)