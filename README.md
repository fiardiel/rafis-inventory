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
	```
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
	```
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
	```
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
	```
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
   ```	
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