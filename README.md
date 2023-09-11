# Assignment 2

## The App's link
[Click here](https://rafis-inventory.adaptable.app/main/) to access my app

## Steps
### Step 1. Create a django project
1. Create a virtual environment by running the following command:
  ```
  python -m venv env
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