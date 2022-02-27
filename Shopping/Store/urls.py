from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name='store'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('passwordreset/',views.passwordreset,name='passwordreset'),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('remove/<int:pk>',views.remove,name='remove')
]

