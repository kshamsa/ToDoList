from django.shortcuts import render
from django.http 	  import HttpResponse, HttpResponseRedirect
from .models		  import ToDoList, Item
from .forms			  import CreateNewList

def index(response, id):
	ls = ToDoList.objects.get(id=id)

	if response.method == "POST":
		if response.POST.get("save"):
			for item in ls.item_set.all():
				if response.POST.get("c" + str(item.id)) == "clicked":
					item.complete = True
				else:
					item.complete = False

				item.save()

		elif response.POST.get("newItem"):
			txt = response.POST.get("new")

			if len(txt) > 2:
				ls.item_set.create(text=txt, complete=False)
				
		elif response.POST.get("delete-list"):
			ls.delete()
			toDoLists = ToDoList.objects.all()
			return HttpResponseRedirect("/")

		elif response.POST.get("delete-item"):
			item_id = response.POST.get("delete-item")
			toDoItem = Item.objects.get(id=item_id)
			toDoItem.delete()

		else:
			print(response.POST)

	return render(response, "main/list.html", {"ls":ls})

def home(response):

	toDoLists = ToDoList.objects.all()

	return render(response, "main/home.html", {"toDoLists": toDoLists})


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