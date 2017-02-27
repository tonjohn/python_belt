from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from .models import Item
from ..login.models import User


def index(request):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	user = User.objects.get(id=request.session['userid'])
	objects = user.wishlist
	items = Item.objects.all().exclude(id__in=[elem.id for elem in objects.all()])

	context = {
		"objects": objects,
		"items": items,
		"view": "index",
	}
	return render(request, 'belt/index.html', context)


def show(request, object_id):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	try:
		object = Item.objects.get(id=object_id)
	except ObjectDoesNotExist:
		messages.error(request, "Invalid ID")
		object = None

	context = {
		'object': object
	}
	return render(request, 'belt/show_object.html', context)


def create(request):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	if request.method == "POST":
		errors = Item.objects.create_product(request.POST, request.session['userid'])

		if errors:
			for error in errors:
				messages.error(request, error )
			return redirect( 'belt:create_item' )
		else:
			messages.success(request, "Item created and added to your wishlist!")

		return redirect('belt:index')
	else:
		return render(request, "belt/add_object.html")


def add(request, object_id):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	if request.method == "POST":
		errors = Item.objects.add_product(object_id, request.session['userid'])

		if errors:
			for error in errors:
				messages.error(request, error )
		else:
			messages.success(request, "Item added to your wishlist!")
	else:
		messages.error(request, "Invalid Request")

	return redirect('belt:index')


def delete(request, object_id):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	try:
		user = User.objects.get(id=request.session['userid'])
		item = Item.objects.get(id=object_id, added_by=user)
		if request.method == "POST":
			results = item.delete()
			print "Deleted Items:", results
			messages.success(request, "Your item has been deleted.")
	except ObjectDoesNotExist:
		messages.error(request, "You do not have permission to delete this item or this item does not exist.")

	return redirect('belt:index')


def remove(request, object_id):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	try:
		user = User.objects.get(id=request.session['userid'])
		item = Item.objects.get(id=object_id, user=user)
		if request.method == "POST":
			results = user.wishlist.remove( item )
			print str(results) + " items removed from user " + user.alias
			messages.success( request, "The item has been removed from your wishlist." )
	except ObjectDoesNotExist:
		messages.error(request, "You do not have permission to remove this item or this item does not exist.")

	return redirect('belt:index')
