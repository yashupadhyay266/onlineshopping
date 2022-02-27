from django.shortcuts import render,redirect
from Store.forms import CreateUserForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Product,Order,OrderItem,ShippingAddress
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
    
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request,'store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)


def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)  
	                       
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def remove(request,pk):
    customer=request.user
    product = Product.objects.get(id=pk)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    orderitem.delete()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

 
    
#For Registering login and logout 
def registerPage(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
    if form.is_valid():
        user=form.save()
        username=form.cleaned_data.get('username')
        messages.success(request,'Account is Created Sucessfully!!'+username)
        return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

def loginPage(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        if user is None:
            messages.success(request,'Username or Password is Incorrect !!')
       
    context={}
    return render(request,'login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('store')



def passwordreset(request):
    if request.method=='POST':
        username=request.POST.get('username')
        u=User.objects.get(username=username)
        newpassword=request.POST['newpassword']
        u.set_password(newpassword)
        u.save()
        return redirect('Tasks:login')
   
    return render(request,'passwordreset.html')

   
        

