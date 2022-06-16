from django.shortcuts import render
from django.http 	  import HttpResponse, HttpResponseRedirect
from .models		  import ToDoList, Item
from .forms			  import CreateNewList

def index(response, id):

	ls = ToDoList.objects.get(id=id)

	return render(response, "main/list.html", {"ls":ls})

def home(response):
	return render(response, "main/home.html", {})


def create(response):
	if response.method == "POST":
		#response.POST will hold dictionary of all the values from
		#the submitted form
		form = CreateNewList(response.POST)

		if form.is_valid():
			name     = form.cleaned_data["name"]
			toDoList = ToDoList(name=name)
			toDoList.save()

		return HttpResponseRedirect("/%i" % toDoList.id)

	else:
		form = CreateNewList()
	
	return render(response, "main/create.html", {"form": form})