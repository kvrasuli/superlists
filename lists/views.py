from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List

def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')

def new_list(request):
	'''новый список'''
	list_ = List.objects.create()
	item = Item(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect(list_)

def view_list(request, list_id):
	'''представление списка'''
	list_ = List.objects.get(id=list_id)
	error = None
	if request.method == 'POST':
		try:
			item = Item(text=request.POST['item_text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			error = "You can't have an empty list item"
	return render(request, 'list.html', {'list': list_, 'error': error})
