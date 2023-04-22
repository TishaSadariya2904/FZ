"""FashionZone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fashion.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main, name="main"),
    path('', home, name="home"),
    
    path('admin-login/', adminLogin, name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),
    
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pid>/', edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', delete_product, name="delete_product"),
    
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change-password/', change_password, name="change_password"),
    
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    
    path('user-feedback/', user_feedback, name="user_feedback"),
    path('manage-feedback/', manage_feedback, name="manage_feedback"),
    path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    
    path('payment/', payment, name="payment"), 
    
    path('feedback-read/<int:pid>/', read_feedback, name="read_feedback"),
    
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    
    path('manage_contact/',manage_contact, name="manage_contact"),
    path('delete_contact/<int:pid>',delete_contact,name='delete_contact'),
    
    path('seller_pending',seller_pending,name='seller_pending'),
    path('change_status/<int:pid>',change_status,name='change_status'),
    path('seller_accepted',seller_accepted,name='seller_accepted'),
    path('seller_rejected',seller_rejected,name='seller_rejected'),
    path('seller_all',seller_all,name='seller_all'),
    path('delete_seller/<int:pid>',delete_seller,name='delete_seller'),
    
    path('seller_login',seller_login,name='seller_login'),
    path('seller_signup',seller_signup,name='seller_signup'),
    path('seller_home',seller_home,name='seller_home'),
    path('seller_dashboard/', seller_dashboard, name="seller_dashboard"),
    
    path('seller_profile',seller_profile,name='seller_profile'),
    path('change_passwordseller',change_passwordseller,name='change_passwordseller'),
        
    path('sadd-category/', sadd_category, name="sadd_category"),
    path('sview-category/', sview_category, name="sview_category"),
    path('sedit-category/<int:pid>/', sedit_category, name="sedit_category"),
    path('sdelete-category/<int:pid>/', sdelete_category, name="sdelete_category"),
    
    path('sadd-product/', sadd_product, name='sadd_product'),
    path('sview-product/', sview_product, name='sview_product'),
    path('sedit-product/<int:pid>/', sedit_product, name="sedit_product"),
    path('sdelete-product/<int:pid>/', sdelete_product, name="sdelete_product"),
    
    path('smanage-user/', smanage_user, name="smanage_user"),
    path('sdelete-user/<int:pid>/', sdelete_user, name="sdelete_user"),
    
    path('smanage_contact/',smanage_contact, name="smanage_contact"),
    path('sdelete_contact/<int:pid>',sdelete_contact,name='sdelete_contact'),
    
    path('smanage-feedback/', smanage_feedback, name="smanage_feedback"),
    path('sdelete-feedback/<int:pid>/', sdelete_feedback, name="sdelete_feedback"),
    path('sfeedback-read/<int:pid>/', sread_feedback, name="sread_feedback"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

