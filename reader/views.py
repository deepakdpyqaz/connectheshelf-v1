from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
from django.template import loader
from django.template.loader import render_to_string
from reader.models import Reader,Treader,Coupon,Requestt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime,date,timedelta
import random
from django.core.mail import send_mail
from django.utils.html import strip_tags
from distributor.extrafunctions import encrypter
from distributor.models import Book,Buybook,Distributor,orderbook,orderreader,nocod,cod
from reader.serializers import Bookserializer
import time
from django.utils import timezone
actions=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
senderMail='deepprak2001@gmail.com'
# Create your views here.

def combinemodel(books):
    bks=[]
    for book in books:
        book.photo=str(book.photo)
        bbk=Buybook.objects.filter(username=book.username,name=book.name).first()
        book.price=bbk.price
        book.stock=bbk.stock
        book.bookid=book.id
        book.distributor=book.username.name
        bks.append(book)
    return bks
def home(request):
    return redirect('distributor_viewbook')


@api_view(['GET', 'POST'])
def login(request):
    if('reader' in request.session):
        return redirect('reader_home')
    if(request.method == 'GET'):
        params = {'actions': actions, 'type': 'reader'}
        return render(request, 'login.html', params)
    if(request.method == 'POST'):
        username = request.data['username']
        password = request.data['password']
        params = {'verified': False}
        try:
            distr = Reader.objects.filter(username=username)
            if(len(distr) == 0):
                params['error'] = 'username incorrect'
            else:
                distr = distr.first()
                if(distr.password == password):
                    params['verified'] = True
                    request.session['reader'] = username
                    params['url'] = '/reader/profile'
                else:
                    params['error'] = 'password incorrect'
        except:
            params = {'error': 'server error'}
        return JsonResponse(params)
    raise Http404("Not found")

@api_view(['GET','POST'])
def signup(request):
    if('reader' in request.session):
        return redirect('reader_home')
    if(request.method == 'GET'):
        params = {'actions': actions, 'type': 'reader', 'Error': False}
        return render(request, 'reader/signup.html', params)
    if(request.method == 'POST'):
        name = request.data['name']
        email = request.data['email']
        contact = request.data['contact']
        username = request.data['username']
        password = request.data['password']
        age = request.data['age']
        otp = random.randint(10000, 999999)
        rdr = Reader.objects.filter(username__iexact=username)
        Error = []
        if(len(rdr) != 0):
            Error.append("Username not available.")
        rdr = Reader.objects.filter(email=email)
        if(len(rdr) != 0):
            Error.append("Email is already registered.")
        rdr = Reader.objects.filter(contact=contact)
        if(len(rdr) != 0):
            Error.append("contact is already registered.")
        if(Error):
            error=''
            for er in Error:
                error+=er+'<br>'
            params = {'verified': False, 'error': error}
            return JsonResponse(params)
        else:
            treader=Treader(username=username,name=name,contact=contact,age=age,email=email,password=password,otp=otp,status='pending')
            treader.save()
            html_message = render_to_string('mail/otp.html', {'name': name, 'otp': otp})
            plain_message = strip_tags(html_message)
            send_mail('ConnecTheShelf verification', plain_message, senderMail,[email], html_message=html_message, fail_silently=False)
            params={'verified':True,'url':False,'otp':True,'callback':'/reader/verify'}
            return JsonResponse(params)


@api_view(['GET','POST'])
def verify(request):
    if(request.method=='POST'):
        name = request.data['name']
        email = request.data['email']
        contact = request.data['contact']
        username = request.data['username']
        password = request.data['password']
        age = request.data['age']
        otp = request.data['otp']

        try:
            treader=Treader.objects.filter(username=username,status='pending').last()
            if(treader.otp==int(otp)):
                rdr = Reader(username=username, name=name, contact=contact,age=age, email=email, password=password,address='')
                rdr.save()
                rdr=Reader.objects.get(username=username)
                coupon=Coupon(username=rdr,coupon=encrypter(rdr.username),used_by=0,max_limit=5)
                coupon.save()
                treader.delete()
                params={'verified':True,'url':'/reader/login'}
                return JsonResponse(params)
            else:
                params={'verified':False,'error':'OTP invalid'}
                return JsonResponse(params)
        except:
            params={'verified':False,'error':'Time out'}
            return JsonResponse(params)

def profile(request):
    if('reader' in request.session):
        if(request.method=='GET'):
            rdr=Reader.objects.get(username=request.session['reader'])
            ref=Coupon.objects.get(username=rdr)
            params={'actions':actions,'type':'reader','reader':rdr,'ref':ref}
            return render(request,'reader/profile.html',params)

        if(request.method=='POST'):
            name=request.POST['name']
            age=request.POST['age']
            password=request.POST['password']
            contact=request.POST['contact']
            address=request.POST['address']
            rdr=Reader.objects.get(username=request.session['reader'])
            email=rdr.email
            rdr.name=name
            rdr.age=age
            rdr.password=password
            rdr.address=address
            rdr.save()
            html_message=render_to_string('mail/changedetails.html',{'name':name})
            plain_message=strip_tags(html_message)
            send_mail('ConnecTheShelf Change profile',plain_message,senderMail,[email],html_message=html_message,fail_silently=False)
            return redirect('reader_profile')
        return redirect('reader_profile')


@api_view(['GET','POST'])
def viewbook(request):
    if(request.method=='GET'):
        if('reader' in request.session):
            params={'actions':actions,'type':'reader'}
        else:
            params={'type':'reader'}
        fst = Book.objects.filter(category='novel')[::10]
        params['novel']=combinemodel(fst)
        fst=Book.objects.filter(category='literature')[::2]
        params['literature']=combinemodel(fst)
        fst=Book.objects.filter(category='thriller')[::5]
        params['thriller']=combinemodel(fst)
        fst=Book.objects.filter(category='exam')[::5]
        params['exam']=combinemodel(fst)
        fst=Book.objects.filter(category='comics')[::5]
        params['comics']=combinemodel(fst)
        fst=Book.objects.filter(category='religion')[::5]
        params['religion']=combinemodel(fst)
        return render(request,'reader/allbooks.html',params)

    if(request.method=='POST'):
        method=request.data['type']
        if(method=='search'):
            query=request.data['query']
            bks=[]
            bk=Book.objects.filter(name__icontains=query)
            bks+=combinemodel(bk)
            bk=Book.objects.filter(author__icontains=query)
            bks+=combinemodel(bk)
            bk=Book.objects.filter(category__icontains=query)
            bks+=combinemodel(bk)
            Serializer=Bookserializer(bks,many=True)
            return JsonResponse(Serializer.data,safe=False)
        elif(method=='filter'):
            category=request.data['category'].strip()
            author=request.data['author'].strip()
            username=request.data['distributor']
            if(username==''):
                bks=[]
                bk=Book.objects.filter(category__icontains=category,author__icontains=author)
                bks+=combinemodel(bk)
                Serializer=Bookserializer(bks,many=True)
                return JsonResponse(Serializer.data,safe=False)
            else:
                user=Distributor.objects.filter(name__iexact=username).first()
                bks=[]
                bk=Book.objects.filter(category__icontains=category,author__icontains=author,username=user)
                bks+=combinemodel(bk)
                Serializer=Bookserializer(bks,many=True)
                return JsonResponse(Serializer.data,safe=False)

def viewcategory(request,category):
    if('reader' in request.session):
        params={'actions':actions,'type':'reader'}
    else:
        params={'type':'reader'}
    fst = Book.objects.filter(category__icontains=category)
    params['books']=combinemodel(fst)
    params['title']=category
    return render(request,'reader/books.html',params)

def viewdistributor(request,name):
    if('reader' in request.session):
        params={'actions':actions,'type':'reader'}
    else:
        params={'type':'reader'}
    user=Distributor.objects.filter(name=name).first()
    fst = Book.objects.filter(username=user)
    params['books']=combinemodel(fst)
    params['title']=name
    return render(request,'reader/books.html',params)

@api_view(['GET','POST'])
def view_order(request):
    if('reader' in request.session):
        if(request.method=='GET'):
            params={'actions':actions,'type':'reader'}
            rdr=Reader.objects.filter(username=request.session['reader']).first()
            order=list(orderreader.objects.filter(reader=rdr))[::-1]
            params['order']=order
            return render(request,'reader/cart.html',params)

def view_order_id(request,orderId):
    if('reader' in request.session):
        try:
            ordreader=orderreader.objects.filter(orderId__iexact=orderId).first()
            rdr=Reader.objects.filter(username=request.session['reader']).first()
            if(ordreader.reader==rdr):
                order=orderbook.objects.filter(orderId=ordreader)
                params={'actions':actions,'type':'reader','order':order,'orderId':ordreader.orderId,'status':ordreader.status}
                return render(request,'reader/vieworder.html',params)
        except:
            return HttpResponse('page not found')
        
@api_view(['GET','POST'])
def getbook(request):
    if(request.method=='POST'):
        bids=(request.data['bookid'])
        book=[]
        for bid in bids:
            book+=Book.objects.filter(id=bid)
        books=combinemodel(book)
        serializer=Bookserializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)

@api_view(['GET','POST'])
def payment(request,distributor):
    if(request.method=='GET'):
        if(distributor.lower()=='connectheshelf'):
            rdr=Reader.objects.filter(username=request.session['reader']).first()
            params={'address':rdr.address,'distributor':distributor,'actions':actions,'type':'reader'}
            return render(request,'reader/checkoutcts.html',params)
        else:
            rdr=Reader.objects.filter(username=request.session['reader']).first()
            params={'address':rdr.address,'distributor':distributor,'actions':actions,'type':'reader'}
            return render(request, 'reader/checkoutother.html', params)
    if(request.method=='POST'):
        if(distributor.lower()=='connectheshelf'):
            coupon=request.data['coupon']
            if(len(coupon)>0):
                cpn=Coupon.objects.filter(coupon__iexact=coupon)
                if(len(cpn)==0):
                    return JsonResponse({'error':'Invalid Coupon','success':False})
                else:
                    cpn=cpn.first()
                if(cpn.used_by>=cpn.max_limit):
                    return JsonResponse({'error':'Coupon had been used many times','success':False})
                if(cpn.username.username==request.session['reader']):
                    return JsonResponse({'error':'Cannot use your own coupon','success':False})
                orderid=encrypter(str(time.time()).split('.')[0])
                dist=Distributor.objects.filter(name__iexact=distributor).first()
                rdr=Reader.objects.filter(username=request.session['reader']).first()
                tme=timezone.now()
                status='pending'
                deliveryaddress=request.data['address']
                odr=orderreader(orderId=orderid,distributor=dist,reader=rdr,tme=tme,status=status,deliveryaddress=deliveryaddress)
                odr.save()
                booklist=request.data['orders'].split('/cts/')
                booklist.pop()
                for book in booklist:
                    bks=book.split('/qty/')
                    bkid=Book.objects.filter(id=bks[0]).first()
                    buybk=Buybook.objects.filter(username=bkid.username,name=bkid.name).first()
                    qty=int(bks[1])
                    bk=orderbook(orderId=odr,bookid=bkid,quantity=qty)
                    bk.save()
                    buybk.stock=buybk.stock-qty
                    buybk.save()
                if(request.data['express']==1):
                    express=True
                else:
                    express=False
                if(request.data['old']==1):
                    old=True
                else:
                    old=False
                
                cd=cod(orderId=odr,coupon=cpn,validcoupon=True,express=express,oldbooks=old)
                cd.save()
                cpn.used_by+=1
                cpn.save()

                return JsonResponse({'success':'True','callbackurl':'/reader/view_order'})
            else:
                orderid = encrypter(str(time.time()).split('.')[0])
                dist = Distributor.objects.filter(
                    name__iexact=distributor).first()
                rdr = Reader.objects.filter(
                    username=request.session['reader']).first()
                tme = datetime.now()
                status = 'pending'
                deliveryaddress = request.data['address']
                odr = orderreader(orderId=orderid, distributor=dist, reader=rdr,tme=tme, status=status, deliveryaddress=deliveryaddress)
                odr.save()

                booklist = request.data['orders'].split('/cts/')
                booklist.pop()
                for book in booklist:
                    bks = book.split('/qty/')
                    bkid = Book.objects.filter(id=bks[0]).first()
                    buybk=Buybook.objects.filter(username=bkid.username,name=bkid.name).first()
                    qty = int(bks[1])
                    bk = orderbook(orderId=odr, bookid=bkid, quantity=qty)
                    bk.save()
                    buybk.stock-=qty
                    buybk.save()
                if(request.data['express'] == 1):
                    express = True
                else:
                    express = False
                if(request.data['old'] == 1):
                    old = True
                else:
                    old = False
                cd = cod(orderId=odr, coupon=None, validcoupon=False, express=express, oldbooks=old)
                cd.save()
                return JsonResponse({'success': 'True','callbackurl':'/reader/view_order'})
            return JsonResponse({'error':'Coupon invalid','success':'True'})
        else:
            orderid = encrypter(str(time.time()).split('.')[0])
            dist = Distributor.objects.filter(name__iexact=distributor).first()
            rdr = Reader.objects.filter(username=request.session['reader']).first()
            tme = timezone.now()
            status = 'pending'
            deliveryaddress = request.POST['address']
            odr = orderreader(orderId=orderid, distributor=dist, reader=rdr,tme=tme, status=status, deliveryaddress=deliveryaddress)
            odr.save()
            booklist = request.POST['orders'].split('/cts/')
            booklist.pop()
            for book in booklist:
                bks = book.split('/qty/')
                bkid = Book.objects.filter(id=bks[0]).first()
                buybk = Buybook.objects.filter(username=bkid.username, name=bkid.name).first()
                qty = int(bks[1])
                bk = orderbook(orderId=odr, bookid=bkid, quantity=qty)
                bk.save()
                buybk.stock = buybk.stock-qty
                buybk.save()
            photo=request.FILES['photo']
            nocd = nocod(orderId=odr,screenshot=photo)
            nocd.save()
            return redirect('view_order')

@api_view(['GET','POST'])
def requestt(request):
    if(request.method=="GET"):
        params={'actions':actions,'type':'reader'}
        return render(request,'reader/request.html',params)
    if(request.method=="POST"):
        usr=Reader.objects.filter(username=request.session['reader']).first()
        name=request.data['name']
        author=request.data['author']
        req=Requestt(username=usr,name=name,author=author)
        req.save()
        html_message = render_to_string('mail/request.html', {'name': name, 'author': author,'username':usr.name})
        plain_message = strip_tags(html_message)
        send_mail('ConnecTheShelf book request', plain_message, senderMail,[senderMail,usr.email], html_message=html_message, fail_silently=False)
        return JsonResponse({"verified":True,"url":"/reader/viewbook"})