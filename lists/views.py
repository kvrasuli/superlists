from django.shortcuts import render


def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')


