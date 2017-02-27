from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(request):
	if 'userid' in request.session:
		print "Userid: ", request.session['userid']
		return redirect('books:index')

	# if validate_user(request):
	# 	return redirect(reverse('login:success'))

	if 'userid' in request.session:
		print "Userid, post validation: ", request.session['userid']

	if not 'alias' in request.session:
		request.session['alias'] = ""
	if not 'name' in request.session:
		request.session['name'] = ""
	if not 'email' in request.session:
		request.session.email = ""
	# if not 'error' in request.session:
	# 	request.session['email'] = ""
	# 	request.session['name'] = ""
	# 	request.session['alias'] = ""

	return render(request, 'base.html')


def login(request):
	if request.session.get('is_authed'):
		return redirect('books:index')

	if request.method == "POST":
		print "Processing Login for", request.POST['email']
		results = User.objects.login(request.POST)
		if not results['error']:
			messages.success(request, "Successfully logged in!")
			user = results['user']
			# print user['id'], user['alias']
			print user.id, user.alias
			request.session['userid'] = user.id
			request.session['alias'] = user.alias
			request.session['name'] = user.name
			request.session['email'] = user.email
			request.session['is_authed'] = True
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['email'] = request.POST['email']
		return redirect("books:index")
	else:
		return render(request, "base.html")


def do_register(request):
	if request.method == "POST":
		print "Processing Registration!"
		action = "registered"
		results = User.objects.register(request.POST)
		if not results['error']:
			messages.success(request, "Successfully " + action + "!")
			user = results['user']
			# print user['id'], user['alias']
			print user.id, user.alias
			request.session['userid'] = user.id
			request.session['alias'] = user.alias
			request.session['name'] = user.name
			request.session['email'] = user.email
			request.session['is_authed'] = True
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['alias'] = request.POST['alias']
			request.session['name'] = request.POST['name']
			request.session['email'] = request.POST['email']
		return redirect( "books:index" )
	else:
		return render(request, "register.html")


def process(request):
	print "process function"
	if request.method == "POST":
		if request.POST['action'] == "Login":
			print "Processing Login for", request.POST['email']
			action = "logged in"
			results = User.objects.login(request.POST['email'], request.POST['password'])
		elif request.POST['action'] == "Register":
			print "Processing Registration!"
			action = "registered"
			results = User.objects.register(request.POST['alias'], request.POST['name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['dob'])

		print results
		if not results['error']:
			messages.success(request, "Successfully " + action + "!")
			user = results['user']
			# print user['id'], user['alias']
			print user.id, user.alias
			request.session['userid'] = user.id
			request.session['alias'] = user.alias
			request.session['name'] = user.name
			request.session['email'] = user.email
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['alias'] = request.POST['alias']
			request.session['name'] = request.POST['name']
			request.session['email'] = request.POST['email']

	return redirect("login:success")


def success(request):
	return render(request, 'success.html')


def logout(request):
	request.session.clear()
	return redirect("login:index")


def view_user(request, userid=1):
	if not request.session.get('is_authed'):
		messages.error(request, "Please login.")
		return redirect('login:login')

	user = User.objects.get( id=userid )
	context = {
		'user': user,
	}
	return render(request, 'login/view_user.html', context)
