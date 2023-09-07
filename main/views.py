from django.shortcuts import render

def show_main(request):
    context = {
        'application_name': "Rafi's Inventory",
        'name': 'Rafi Ardiel Erinaldi',
        'class' : 'PBP Int'
    }

    return render(request, 'main.html', context)