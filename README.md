# Assignment 2

## The App's link
[Click here](https://rafis-inventory.adaptable.app/main/) to access my app

## Steps
### Step 1. Create a django project
1. Create a virtual environment by running the following command:
  ```
  python3 -m venv env
  ```
2. Activate the virtual environment by running this command:
  - Windows:
    ```
    env\Scripts\activate.bat
    ```
  - Mac:
    ```
    source env/bin/activate
    ```
3. Create a `requirements.txt` in your directory file to install some dependencies

4. Download all the dependencies by running this command:
	```
	python3 -m pip install requirements.txt
	```
5. Start my django project by running the following command:
	```
	django-admin startproject rafis_inventory .
	```

### Step 2. Create an app with the name main on that project.
1. Run the following command to make a main application
	```
	python manage.py startapp main
	```
2. Add a directory called `templates` in the main app, and then create a `main.html` file in it

3. Fill in my main.html file with the html code below:
	``` html
	<h1>Rafi's Inventory Page</h1>

	<h5>Application Name:</h5>
	<p>{{ application_name }}</p>

	<h5>Name:</h5>
	<p>{{ name }}</p>

	<h5>Class:</h5>
	<p>{{ class }}</p>
	```
	What it does is creating the design, and taking the application name, name, and class from the views.py file which I will be talking in the next steps

4. Fill in the views.py with this code:
	``` py
	from django.shortcuts import render

	def show_main(request):
		context = {
			'application_name': "Rafi's Inventory",
			'name': 'Rafi Ardiel Erinaldi',
			'class' : 'PBP Int'
		}

		return render(request, 'main.html', context)
	```
	This code sends the application_name, name, and class variable to the html template

### Step 3. Create a URL routing configuration to access the main app.
1. Create `urls.py` inside the main directory and then fill in with the following code:
	``` py
	from django.urls import path
	from main.views import show_main

	app_name = 'main'

	urlpatterns = [
		path('', show_main, name='show_main'),
	]
	```
	This is responsible for configuring URL patterns to the main application

### Step 4. URL Routing for the project
1. Open the `urls.py` in the project's `rafis_inventory` directory
2. Fill the `urls.py` file with this code:
	``` py
	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
		path("admin/", admin.site.urls),
		path('main/', include('main.urls')),
	]
	```
	This is responsible for configuring the top-level project URL routes.


### Step 5. Editing the models for your app
1. Create the attributes such as `name, amount, description, category, damage` by filling your
   `models.py` file with this code:
   	```	py
	from django.db import models
	class Items(models.Model):
			name = models.CharField(max_length=255)
			amount = models.IntegerField()
			description = models.TextField()
			category = models.CharField(max_length=255)
			damage = models.IntegerField()
	```

## Client request flow
<img src="/assets/PBPImage.png">

A `user` requests entering the app using the url by clicking the link. The url will find
a way to route to the app. The `urls.py` file contains a link/mapping to the function in `views.py`.
The `views.py` file will return the HTML template and render it to the user. And then the `views.py`
file will interact with `models.py` if data is needed. Finally, `models.py` will get the data
from your database.


## Purpose of virtual environment
Before we talk about the purpose, yes, a django app can run without a virtual environment.
But, there is a downside to that. The downside is that without a virtual environment,
the dependencies that's installed would be installed globally, which would cause conflicts with 
other projects and system packages. One possible case that causes problem is that different projects
use different versions of python.

## MVC, MVT, MVVM, and the difference between the three
MVC stands for Model-View-Controller. It seperates the application into model, view, controller. The 
model is responsible for the data structure and the logic, the view for the display of the data,
and the controller as the middle man who receives update from view and notifies model to add something.

MVT stands for Model-View-Template. The difference with MVC is that MVT uses template as the user
interface

MVVM stands for Model-View-ViewModel. This pattern supports two-way data binding between view and View model. 
This enables automatic propagation of changes, within the state of view model to the View.

The key difference between the 3 are the mediators and the entry point to the app



# Assignment 3

## Steps
### 1. Create `forms.py` in the main folder
Fill in your `forms.py` with this code:

	``` py

	from django.forms import ModelForm
	from main.models import Items

	class ProductForm(ModelForm):
		class Meta:
			model = Items
			fields = ["name", "amount", "description", "category", "damage"]

	```

this code's purpose is to make a form to take input and store it

### 2. Methods in the `views.py` file
Fill in your `views.py` with this code:

	``` py
	from django.shortcuts import render
	from django.http import HttpResponseRedirect
	from django.urls import reverse
	from main.forms import ProductForm
	from main.models import Items
	from django.http import HttpResponse
	from django.core import serializers

	def show_main(request):
		products = Items.objects.all()
		data_count = products.count()

		context = {
			'name': 'Rafi Ardiel Erinaldi',
			'class': 'PBP Int',
			'products': products,
			'data_count': data_count
		}

		return render(request, 'main.html', context)


	def create_product(request):
		form = ProductForm(request.POST or None)

		if form.is_valid() and request.method == "POST":
			form.save()
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
	```

These methods will handle requests such as showing your main page, xml, json, and xml and jason by
their IDs when you access their respective urls.

### 3. Configure your URLs for the requests

	``` py
	from django.urls import path
	from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id

	app_name = 'main'

	urlpatterns = [
		path('', show_main, name='show_main'), path('create-product', create_product, name='create_product'),
		path('xml/', show_xml, name='show_xml'),
		path('json/', show_json, name='show_json'),
		path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
		path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
	]
	```

whenever one of those urls are accessed, they will route you to their respective paths


## Difference between POST and GET in django
The use of POST and GET is distinguishable by their usage. POST is used to submit/modify data
to your server and will change the state of the server. On the other hand, GET's purpose is to 
request data from the server without affecting the state of the server.


## HTML, JSON, XML
HTML's purpose is to display the data. JSOn and XML on the other hand are to
store the data. The difference between XML and JSON is that XML uses the tree
data structure and treats all data as text, while JSON uses key-value pairs and
supports simple data types such as strings, booleans, arrays, and objects.


## JSON in modern web applications
JSON is often used in modern web applications due to it being more human-readable than
XML. It also is easier to parse for programming languages. Since, it uses key-value pairs,
it can be converted to Python as a dictionary.


## Postman accessing the urls

### Main
<img src="/assets/postman_main.png">

### XML
<img src="/assets/postman_xml.png">

### JSON
<img src="/assets/postman_json.png">


### XML by ID
<img src="/assets/postman_xml_by_id.png">


### JSON by ID
<img src="/assets/postman_json_by_id.png">



# Assignment 4
## Steps
### Step 1. Make the register, login, and logout functions
Open `views.py` and add these imports code:
	``` py
	from django.contrib.auth.forms import UserCreationForm
	from django.contrib import messages  
	from django.contrib.auth import authenticate, login
	from django.contrib.auth import logout
	```

Write this code in your `views.py`:
	``` py
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
	```

Open your `urls.py` in your main directory and copy these imports:
	``` py
	from main.views import register
	from main.views import login_user
	from main.views import logout_user
	```

Add these paths to your urlpatterns:

	``` py
	path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
	```

Modify your `show_main` function like this:

	``` py
	@login_required(login_url='/login')
	def show_main(request):
		products = Items.objects.all()
		data_count = products.count()

		context = {
			'name': request.user.username,
			'class': 'PBP Int',
			'products': products,
			'data_count': data_count,
			'last_login': request.COOKIES['last_login'],
		}

		return render(request, 'main.html', context)
	```

Make the login page in the template in `login.html` by adding this code:
	``` html
	{% extends 'base.html' %}

	{% block meta %}
		<title>Login</title>
	{% endblock meta %}

	{% block content %}

	<div class = "login">

		<h1>Login</h1>

		<form method="POST" action="">
			{% csrf_token %}
			<table>
				<tr>
					<td>Username: </td>
					<td><input type="text" name="username" placeholder="Username" class="form-control"></td>
				</tr>
						
				<tr>
					<td>Password: </td>
					<td><input type="password" name="password" placeholder="Password" class="form-control"></td>
				</tr>

				<tr>
					<td></td>
					<td><input class="btn login_btn" type="submit" value="Login"></td>
				</tr>
			</table>
		</form>

		{% if messages %}
			<ul>
				{% for message in messages %}
					<li>{{ message }}</li>
				{% endfor %}
			</ul>
		{% endif %}     
			
		Don't have an account yet? <a href="{% url 'main:register' %}">Register Now</a>

	</div>

	{% endblock content %}

	```

Do the same with your register.html but with this code:
	``` html
	{% extends 'base.html' %}

	{% block meta %}
		<title>Register</title>
	{% endblock meta %}

	{% block content %}  

	<div class = "login">
		
		<h1>Register</h1>  

			<form method="POST" >  
				{% csrf_token %}  
				<table>  
					{{ form.as_table }}  
					<tr>  
						<td></td>
						<td><input type="submit" name="submit" value="Daftar"/></td>  
					</tr>  
				</table>  
			</form>

		{% if messages %}  
			<ul>   
				{% for message in messages %}  
					<li>{{ message }}</li>  
					{% endfor %}  
			</ul>   
		{% endif %}

	</div>  

	{% endblock content %}
	```

Finally in the main.html add the logout button by adding this code
	``` html
	<a href="{% url 'main:logout' %}">
        <button>
            Logout
        </button>
    </a>
	```


### Step 2. Apply cookies
Make these imports in the `views.py` file

	``` py
	import datetime
	from django.http import HttpResponseRedirect
	from django.urls import revers
	```

Add this code to your `context` in your `show_main` function of the `views.py` file

	``` py
	'last_login': request.COOKIES['last_login'],
	```

The other steps to add cookie I've already done in the 1st step


## Django's UserCreationForm and its advantages and disadvantages
Django's UserCreationForm is a built in form in django that mainly is used to 
create a user for your website. There, you need to fill in your username, password,
and password confirmation, where the password's strength is emphasized.
The advantage of it is that it is easy to use and there's a template for it. The downside
is that it's not quite customizable.

## Authentication vs Authorization. Why are they both important?
Authentication is a process to verify whether someone is who they exactly are or not,
whereas authorization is a process to verify whether someone have access to certain files,
apps, or data. They're both important since there are informations that can't be shared publicly
or there are things that you don't want any random people to have access to.

## Cookies
A cookie is a small piece of information which is stored in the client browser. It is used to store 
user's data in a file permanently (or for the specified time). Cookie has its expiry date and time 
and removes automatically when gets expire. Django provides built-in methods to set and fetch cookie.

Cookies are secure, but if used incorrectly, someone can access your data/sensitive information



# Assignment 5

## HTML tags


`<a>` is for hyperlinks
`<h5>, <h1>, <h2>,` etc. are for headers
`<p>` is for paragraph/text

## Bootstrap vs Tailwind
So tailwind is more do-it-yourself and more customizable. You can make your own custom designs
from scratch with tailwind, and with flowbite you can search for templates/examples. With bootstrap,

## Margin and Padding
Margin is the space outside of your element, whilst padding is the space inside your element, for exaxmple 
if you have a button, the padding is the space inside the button for the space between the text and the outline

## Steps
1. Install Tailwind
2. Create a navbar in the templates with the file name `navbar.html` and modify using tailwind codes
3. Modify the product tables using tailwind
4. Make cards for the login, create, edit, and register pages and insert hyperlinks to each other.




# Assignment 6
## Steps

### Installing Flowbite
Since I already installed `node.js` and also `tailwind` I just need to follow
the installation steps for Flowbite CSS, which you can see in this link:

[Flowbite Installation](https://flowbite.com/docs/getting-started/quickstart/)

### Perform AJAX GET and POST
1. Create a `add_product_ajax` function in your `views.py`:

	``` py
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
	```

2. Create a `get_product_json` function in your `views.py`:

	``` py
	def get_product_json(request):
		product_item = Items.objects.all()
		return HttpResponse(serializers.serialize('json', product_item))
	```

3. In your `urls.py`, import the `add_product_ajax` and `get_product_json` function


### Showing the product data using fetch() API
1. Add these scripts to your `main.html` file:

	```html
	<script>
        async function getProducts() {
            return fetch("{% url 'main:get_product_json' %}").then((res) => res.json())
        }


        async function refreshProducts() {
            document.getElementById("product_table").innerHTML = ""
            const products = await getProducts()
            let htmlString = `\n
            <div id="product_table" class="grid justify-center px-10 py-10">
                <table class="w-fit text-left bg-slate-600 rounded-xl">
                    <thead class="bg-indigo-700 rounded-t-xl border-b dark:border-gray-600">
                        <tr>
                            <th class="px-5 py-2 rounded-tl-xl">Name</th>
                            <th class="px-5 py-2">Amount</th>
                            <th class="px-5 py-2">Description</th>
                            <th class="px-5 py-2">Category</th>
                            <th class="px-5 py-2">Damage</th>
                            <th class="px-5 py-2 rounded-tr-xl">Actions</th>
                        </tr>
                    </thead>`

            products.forEach((item) => {
                htmlString += `\n
                    <tbody>
                        <tr>
                            <td class="px-5 py-2">${ item.fields.name }</td>
                            <td class="px-5 py-2">${ item.fields.amount }</td>
                            <td class="px-5 py-2">${ item.fields.description }</td>
                            <td class="px-5 py-2">${ item.fields.category }</td>
                            <td class="px-5 py-2">${ item.fields.damage }</td>
                            <td class="px-5 py-2">
                                <a href="/increment_amount/${ item.pk }">
                                    <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-cloud-plus-fill" viewBox="0 0 16 16">
                                            <path d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zm.5 4v1.5H10a.5.5 0 0 1 0 1H8.5V10a.5.5 0 0 1-1 0V8.5H6a.5.5 0 0 1 0-1h1.5V6a.5.5 0 0 1 1 0z"/>
                                        </svg>
                                    </button>
                                </a>

                                <a href="/decrement_amount/${ item.pk }">
                                    <button type="button" class="text-white bg-yellow-600 hover:bg-yellow-500 focus:ring-4 font-medium rounded-lg text-sm px-3 py-2 mr-2 mb-2 focus:outline-none">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-cloud-minus-fill" viewBox="0 0 16 16">
                                            <path d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zM6 7.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1z"/>
                                        </svg>
                                    </button>
                                </a>


                                <a href="/delete/${item.pk}">
                                    <button type="button" class="text-white bg-red-700 hover:bg-red-600 focus:ring-4 font-medium rounded-lg text-sm px-3 py-2 mr-2 mb-2 focus:outline-none">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                            <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                                        </svg>
                                    </button>
                                </a>

                                <a href="/edit-product/${item.pk}">
                                    <button type="button" class="py-2 px-3 mr-2 mb-2 text-sm font-medium text-gray-500 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                                        </svg>
                                    </button>
                                </a>

                            </td>

                        </tr>`

                    
            })
            htmlString += `</tbody>

                <tfoot>
                    <tr class="font-semibold text-gray-900 dark:text-white">
                        <th scope="row" class="px-6 py-3 text-base">Total</th>
                        <td id="item_count" class="px-6 py-3"> 
                            {{ data_count }}
                        </td>
                    </tr>
                </tfoot>

                </table>
            </div>` 

            document.getElementById("product_table").innerHTML = htmlString
            document.getElementById("item_count").innerHTML = `${products.length}`
        }

        refreshProducts()


        function addProduct() {
            fetch("{% url 'main:add_product_ajax' %}", {
                method: "POST",
                body: new FormData(document.querySelector('#form'))
            }).then(refreshProducts)

            document.getElementById("form").reset()
            return false
        }

        document.getElementById("button_add").onclick = addProduct
    </script>
	 
	```

### Creating a modal to add product using AJAX
1. Create the modal by copying this code to your `main.html` file

	```	html
	<div id="add_product_modal" tabindex="-1" aria-hidden="true" class="fixed top-0 left-0 right-0 z-50 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full">
        <div class="relative w-full max-w-md max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <button type="button" class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="add_product_modal">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
                <div class="font-bold text-2xl px-6 py-6 lg:px-8 mb-5">Add a new item</h3>
                    <form class="space-y-6" action="#" method="POST" id="form">
                        {% csrf_token %}
                        
                        <div>
                            <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Item name</label>
                            <input type="text" name="name" id="name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white" placeholder="Your item name" required>
                        </div>

                        <div>
                            <label for="amount" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Item amount</label>
                            <input type="number" name="amount" id="amount" placeholder="Enter an amount (integer)" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white" required>
                        </div>

                        <div>
                            <label for="description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Description</label>
                            <input type="text" name="description" id="description" placeholder="Item description" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white" required>
                        </div>

                        <div>
                            <label for="category" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Item Category</label>
                            <input type="text" name="category" id="category" placeholder="Enter your item category" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white" required>
                        </div>

                        <div>
                            <label for="damage" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Damage</label>
                            <input type="number" name="damage" id="damage" placeholder="Enter your item damage (0 if not a weapon)" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white" required>
                        </div>

                        <button type="submit" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" id="button_add" data-modal-hide="add_product_modal">Add an item</button>

                    </form>
                </div>
            </div>
        </div>
    </div> 
	```
	In that step, one thing you have to note is 
	specify the button id and the modal id so that 
	it can be accessed

2. In my `navbar.html` file, change the add product button:
	```html
	<button data-modal-target="add_product_modal" data-modal-toggle="add_product_modal" class="block text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:focus:ring-blue-800 transition ease-in-out delay-50 hover:-translate-y-1 hover:scale-110 duration-150" type="button">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
            </svg>
    </button>
	```


## Synchronous vs Asynchronous Programming
The difference between the both of them is that synchronous programming runs the code
sequentially while asynchronous can run them as parallel


## Event-driven programming paradigm
Event-driven programming is a paradigm where the flow of a program is determined by 
events like user actions or system signals. In JavaScript and AJAX, it means that code 
responds to events such as button clicks, data arrival, or timers.


## Asynchronous programming using AJAX
In AJAX, asynchronous programming is used to make requests to a server without blocking 
the rest of the web page. It allows for non-blocking operations, so the webpage remains 
responsive. You typically define a callback function that is executed when the data is 
received from the server, ensuring the user interface remains interactive while waiting for data.







