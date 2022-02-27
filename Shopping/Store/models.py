from itertools import product
from re import L
from django.db import models
from tkinter import CASCADE
from django.contrib.auth.models import User

# Create your models here.
'''class Customer(models.Model):
    storeuser=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)

    def __str__(self):
        return self.name'''


class Product(models.Model):
   
    price=models.FloatField()
    name=models.CharField(max_length=100)
    digital = models.BooleanField(default=False,null=True, blank=True)
    image=models.ImageField(null=True,blank=True,)
    
    def __str__(self):
        return self.name
    
    @property
    def ImageUrl(self):
        try:
             url=self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    customer=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total_cost=sum([items.get_total for items in orderitems])
        return total_cost
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total_items=sum([items.quantity for items in orderitems])
        return total_items
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

   

class OrderItem(models.Model):
    customer=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,null=True,blank=True,on_delete=models.SET_NULL)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=(self.product.price)*self.quantity
        return total

    
class ShippingAddress(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address