from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import date
import json, random
from django.core.mail import send_mail,EmailMultiAlternatives
import pandas as pd
from django.conf import settings
import uuid


# Create your views here.

def navigation(request):
    return render(request, 'navigation.html')

def main(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic)

def home(request):
    return render(request, 'home.html')

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    scount = Seller.objects.all().count()
    ccount = ContactUs.objects.all().count()
    dic = {'msg': msg, 'scount':scount, 'ccount':ccount}
    return render(request, 'admin_login.html', dic)

def adminHome(request):
    return render(request, 'admin_base.html')

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        msg = "Category added"
    return render(request, 'add_category.html', locals())

def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())

def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())

def view_product(request):
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())

def profile(request):
    data = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('main')

def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def uuser_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "uuser-product.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())


def addToCart(request, pid):
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    deduction = 0
    discounted = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * float(product.price)
        price = float(product.price) * (100 - float(product.discount)) / 100
        discounted += int(j) * price
    deduction = total - discounted
    if request.method == "POST":
        return redirect('/payment/?total='+str(total)+'&discounted='+str(discounted)+'&deduction='+str(deduction))
    return render(request, "booking.html", locals())

def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_feedback')

def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def payment(request):
    total = request.GET.get('total')
    discounted = request.GET.get('discounted')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=discounted)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())

def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals()) 

def manage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals()) 

def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 

def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def admin_dashboard(request):
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())

def contact(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        m = request.POST['message']

        try:
            ContactUs.objects.create(fname=f,lname=l,mobile=c,message=m)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'contact.html',d)

def about(request):
    return render(request, 'about.html')


def manage_contact(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = ContactUs.objects.all()
    d = {'data':data}
    return render(request, 'manage_contact.html', d)

def delete_contact(request,pid):
    if not request.user.is_authenticated:
        return redirect('delete_contact')
    contactus = ContactUs.objects.get(id=pid)
    contactus.delete()
    return redirect('manage_contact')


def seller_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = Seller.objects.get(user=user)
                if user1.utype == "seller" and user1.status!="pending":
                    login(request,user)
                    error="no"
                else:
                    error="not"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'seller_login.html',d)

def seller_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        e = request.POST['email']
        p = request.POST['pwd']
        i = request.FILES['image']

        try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           Seller.objects.create(user=user,mobile=c,image=i,utype="seller",status="pending")
           error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'seller_signup.html',d)

def seller_home(request):
    if not request.user.is_authenticated:
        return redirect('seller_login')
    return render(request,'seller_home.html')

def seller_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Seller.objects.filter(status="pending")
    d = {'data':data}
    return render(request,'seller_pending.html',d)

def seller_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Seller.objects.filter(status="Accept")
    d = {'data':data}
    return render(request,'seller_accepted.html',d)

def seller_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Seller.objects.filter(status="Reject")
    d = {'data':data}
    return render(request,'seller_rejected.html',d)

def seller_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Seller.objects.all()
    d = {'data':data}
    return render(request,'seller_all.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    seller = Seller.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        seller.status=s
        try:
            seller.save()
            error="no"
        except:
            error="yes"
    d = {'seller':seller,'error':error}
    return render(request,'change_status.html',d)

def delete_seller(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    seller = Seller.objects.get(id=pid)
    seller.delete()
    return redirect('seller_all')

def change_passwordseller(request):
    if not request.user.is_authenticated:
        return redirect('seller_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordseller.html',d)

def seller_profile(request):
    if not request.user.is_authenticated:
        return redirect('seller_login')
    user = request.user
    seller = Seller.objects.get(user=user)

    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']

        seller.user.first_name = f
        seller.user.last_name = l
        seller.mobile = c

        try:
            seller.save()
            seller.user.save()
            error="no"
        except:
            error="yes"

        try:
            i = request.FILES['image']
            seller.image = i
            seller.save()
            error="no"
        except:
            pass
    d = {'seller':seller,'error':error}
    return render(request,'seller_profile.html',d)

def seller_dashboard(request):
    user = Seller.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'seller_dashboard.html', locals())

def sadd_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        msg = "Category added"
    return render(request, 'sadd_category.html', locals())

def sview_category(request):
    category = Category.objects.all()
    return render(request, 'sview_category.html', locals())

def sedit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'sedit_category.html', locals())

def sdelete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('sview_category')

def sadd_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'sadd_product.html', locals())

def sview_product(request):
    product = Product.objects.all()
    return render(request, 'sview_product.html', locals())

def sedit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
    return render(request, 'sedit_product.html', locals())

def sdelete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('sview_product')

def smanage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'smanage_user.html', locals()) 

def sdelete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('smanage_user') 

def smanage_contact(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = ContactUs.objects.all()
    d = {'data':data}
    return render(request, 'smanage_contact.html', d)

def sdelete_contact(request,pid):
    if not request.user.is_authenticated:
        return redirect('sdelete_contact')
    contactus = ContactUs.objects.get(id=pid)
    contactus.delete()
    return redirect('smanage_contact')

def smanage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'smanage_feedback.html', locals())

def sdelete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('smanage_feedback')

def sread_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def forgot_password(request):
    return render(request,"forgot_password.html")

def reset_password(request):
    if request.method == 'POST' :
        new = request.POST['new']
        old = request.POST['old']
        if new == old :
            email = request.session.get('Email')
            user = User.objects.get(email=email)
            user.password = new
            user.save()
            return redirect("userlogin")
        else :
            return redirect("reset_password")
    return render(request,"reset_password.html")

def fChange_Password(request):
    return render(request,"fChange_Password.html")

def verify(request):
        if request.method == 'POST':
            OTP = request.session.get('OTP')
            email = request.session.get('Email')
            otp = request.POST['otp']
            user = User.objects.get(email=email)
            if str(OTP) == otp:
                # OTP verified successfully, redirect to the reset password page
                
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP.')
                return redirect('forgot_password')
        return render(request,"verify.html")

def function_forgot(request):
    if request.method=="POST":
        Email=request.POST['email']
        try:
            data=User.objects.get(email=Email)
            OTP= random.randint(100000, 999999)
            request.session['OTP'] = OTP
            request.session['Email'] = data.email
            topic='Mender Company'
            data='<p style="font-style: oblique;">OTP is <b>'+str(OTP)+'</b></p>'
            from_email='mender.company@gmail.com'
            to_email=Email
            msg=EmailMultiAlternatives(topic,data,from_email,[to_email])
            msg.content_subtype='html'
            msg.send()
            return redirect("verify")
        except:
            return redirect("forgot_password")
        
def Function_Change(request):
    if request.method=="POST":
        old=request.POST['currentpassword']
        New=request.POST['newpassword']
        unique=request.POST['confirmpassword']
        data=User.objects.filter(uniqueId=unique)
        if data is not None:
            data=User.objects.get(uniqueId=unique)
            if old==data.password:
                data.password=New
                data.save()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('Change_Password')
        else:
                return redirect('Change_Password')
                        
