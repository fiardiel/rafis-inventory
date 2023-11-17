from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from main.forms import ProductForm
from main.models import Items
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login')
def show_main(request):
    products = Items.objects.filter(user=request.user)
    data_count = products.count()

    context = {
        'name': request.user.username,
        'class': 'PBP Int',
        'products': products,
        'data_count': data_count,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, 'main.html', context)


def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)


def show_xml(request):
    data = Items.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = Items.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request, id):
    data = Items.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json_by_id(request, id):
    data = Items.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def increment_amount(request, id):
    item = Items.objects.get(id=id)
    item.amount += 1
    item.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def decrement_amount(request, id):
    item = Items.objects.get(id=id)
    if item.amount > 1:
        item.amount -= 1
        item.save()
    else:
        item.delete()
    
    return HttpResponseRedirect(reverse('main:show_main'))

def delete_product(request, id):
    # Get data by ID
    product = Items.objects.get(pk=id)
    # Delete data
    product.delete()
    # Return to the main page
    return HttpResponseRedirect(reverse('main:show_main'))
    

def edit_product(request, id):
    # Get product by ID
    product = Items.objects.get(pk = id)

    # Set product as instance of form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Save the form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)


def get_product_json(request):
    product_item = Items.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        damage = request.POST.get("damage")
        user = request.user

        new_product = Items(name=name, amount=amount, description=description, 
                            category=category, damage=damage, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def ajax_delete(request, id):
    # Get data by ID
    product = Items.objects.get(pk=id)
    # Delete data
    product.delete()
    # Return to the main page
    return HttpResponse(b"OK", status=201)

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Items.objects.create(
            user = request.user,
            name = data["name"],
            amount = int(data["amount"]),
            description = data["description"],
            category = data["category"],
            damage = int(data["damage"])
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
def filter_items_by_rarity(request):
    rarity = request.GET.get('rarity', 'all')

    if rarity == 'all':
        items = Items.objects.all()
    elif rarity == 'S':
        items = Items.objects.exclude(genre__icontains='S')
    elif rarity == 'SR':
        items = Items.objects.filter(genre__icontains='SR')
    elif rarity == 'SSR':
        items = Items.objects.filter(genre__icontains='SSR')
    else:
        return JsonResponse({'error': 'Invalid category'})

    item_data = []

    for item in items:
        item_data.append({
            'itemid': items.pk,
            'name': items.name,
            'amount': items.amount,
            'description': items.description,
            'category': items.category,
            'damage': items.damage,
            'rarity': items.rarity
        })

    return JsonResponse({'datas': item_data})