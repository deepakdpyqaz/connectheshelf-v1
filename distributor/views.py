from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse,Http404
from reader.models import Reader
from distributor.models import Distributor,Payment, Book, Buybook, Rentbook,orderbook,orderreader,cod,nocod
from rest_framework.decorators import api_view
from distributor.extrafunctions import encrypter


actions=[{'name':'profile','link':''},{'name':'Manage books','link':'managebooks'},{'name':'View orders','link':'vieworders'}]

@api_view(['GET','POST'])
def home(request):
    if('distributor' in request.session):
        if(request.method=='GET'):
            params={'actions':actions,'type':'distributor'}
            dist=Distributor.objects.filter(username=request.session['distributor']).first()
            payment=Payment.objects.filter(username=dist).first()
            params['dist']=dist
            params['payment']=payment
            return render(request,'distributor/profile.html',params)
        if(request.method=='POST'):
            try:
                name=request.data['name']
                password=request.data['password']
                contact=request.data['contact']
                address=request.data['address']
                paymentinfo=request.data['paymentinfo']
                cod=request.data['cod']
                if('cod' in request.data.keys()):
                    cod=True
                else:
                    cod=False
                dist=Distributor.objects.filter(username=request.session['distributor']).first()
                payment=Payment.objects.filter(username=dist).first()
                dist.name=name
                dist.password=password
                dist.contact=contact
                dist.address=address
                payment.paymentinfo=paymentinfo
                payment.cod=cod
                dist.save()
                payment.save()
                return JsonResponse({'verified':True,'url':False})
            except:
                return JsonResponse({"error":"Request can't be processed"})
    return HttpResponse('not worked')


@api_view(['GET', 'POST'])
def login(request):
    if('distributor' in request.session):
        return redirect('distributor_home')
    if(request.method == 'GET'):
        params={'actions':actions,'type':'distributor'}
        return render(request,'login.html',params)
    if(request.method == 'POST'):
        username = request.data['username']
        password = request.data['password']
        params = {'verified': False}
        try:
            distr = Distributor.objects.filter(username=username)
            if(len(distr) == 0):
                params['error'] = 'username incorrect'
            else:
                distr = distr.first()
                if(distr.password == password):
                    params['verified'] = True
                    request.session['distributor']=username
                    params['url']='/distributor'
                else:
                    params['error'] = 'password incorrect'
        except:
            params = {'error': 'server error'}
        return JsonResponse(params)
    raise Http404("Not found")


@api_view(['GET', 'POST'])
def signup(request):
    if(request.method == 'POST'):
        username = request.data['username']
        name = request.data['name']
        email = request.data['email']
        contact = request.data['contact']
        address = request.data['address']
        password = request.data['password']

        try:
            distr = Distributor(username=username, name=name, email=email,
                                contact=contact, address=address, password=password)
            distr.save()
            params = {'added': True}
        except:
            params = {'added': False}

        return JsonResponse(params)
    else:
        params = {'added': False}
        return JsonResponse(params)


@api_view(['GET','POST'])
def managebook(request):
    if('distributor' in request.session):
        if(request.method=='GET'):
            params={'actions':actions,'type':'distributor'}
            user=Distributor.objects.get(username=request.session['distributor'])
            bk=list(Book.objects.filter(username=user))[::-1]
            params['bk']=bk
            return render(request,'distributor/managebook.html',params)

@api_view(['GET','POST'])
def viewbook(request):
    if(request.method=='POST'):
        name=request.data['name']
        author=request.data['author']
        book_type=request.data['book_type']
        bk=Book.objects.filter(name=name,author=author,book_type=book_type)
        if(book_type=='buy'):
            if(len(bk)!=0):
                user=Distributor.objects.get(username=request.session['distributor'])
                bkb=Buybook.objects.filter(username=user,name=name).first()
                params={'actions':actions,'bk':bk.first(),'bkb':bkb,'type':'distributor'}
                return render(request,'distributor/buybook.html',params)
            else:
                user=Distributor.objects.get(username=request.session['distributor'])
                bk=Book(username=user,name=name,author=author,book_type='buy',photo='',category='')
                bk.save()
                bk = Book.objects.filter(username=user, name=name, author=author,rating=3, book_type='buy', photo='', category='').first()
                params={'actions':actions,'bk':bk,'type':'distributor'}
                return render(request,'distributor/buybook.html',params)

def viewbookbyname(request,id):
    bk=Book.objects.filter(id=id).first()
    if(bk.book_type=='buy'):
        user = Distributor.objects.get(username=request.session['distributor'])
        bkb=Buybook.objects.filter(username=user,name=bk.name).first()
        params={'actions':actions,'bk':bk,'bkb':bkb,'type':'distributor'}
        return render(request,'distributor/buybook.html',params)

def deletebookbyname(request,id):
    bk=Book.objects.filter(id=id).first()
    if(bk.book_type=='buy'):
        bk.delete()
        return redirect('distributor_managebook')


@api_view(['GET','POST'])
def editbook(request):
    if(request.method=='POST'):
        name=request.POST['name']
        author=request.POST['author']
        category=request.POST['category']
        stock=request.POST['stock']
        rating=request.POST['rating']
        price=request.POST['price']
        rating=request.POST['rating']
        book_type=request.POST['book_type']
        bkid=int(request.POST['book_id'])
        bkbid=request.POST['buybook_id']
        user=Distributor.objects.get(username=request.session['distributor'])
        bk=Book.objects.filter(id=bkid).first()
        bk.name=name
        bk.author=author
        bk.category=category
        bk.rating=rating
        try:
            photo=request.FILES['photo']
            bk.photo=photo
        except:
            pass
        bk.book_type=book_type
        bk.save()
        try:
            bkb=Buybook.objects.filter(id=int(bkbid)).first()
            bkb.stock=stock
            bkb.price=price
            bkb.save()
        except:
            user=Distributor.objects.get(username=request.session['distributor'])
            bkb=Buybook(name=name,username=user,stock=stock,price=price)
            bkb.save()
        return redirect('distributor_managebook')


def vieworders(request):
    if(request.method=='GET'):
        if('distributor' in request.session):
            dist=Distributor.objects.filter(username=request.session['distributor']).first()
            order=orderreader.objects.filter(distributor=dist).all()
            params={'actions':actions,'type':'distributor','order':order}
            return render(request,'distributor/vieworder.html',params)
    if(request.method == 'POST'):
        if('distributor' in request.session):
            orderId = request.POST['orderId']
            status = request.POST['status']
            order = orderreader.objects.filter(orderId=orderId).first()
            order.status = status
            order.save()
            return redirect('distributor_view_orders')


def vieworders_id(request,orderId):
    if(request.method=='GET'):
        if('distributor' in request.session):
            if(request.session['distributor'].lower()!='cts'):
                user=Distributor.objects.filter(username=request.session['distributor']).first()
                order=orderreader.objects.filter(orderId=orderId).first()
                bks=orderbook.objects.filter(orderId=order)
                for bk in bks:
                    price=Buybook.objects.filter(username=user,name=bk.bookid.name).first()
                    bk.price=price.price
                ncd=nocod.objects.filter(orderId=order).first()
                params={'actions':actions,'type':'distributor','orderId':orderId,'orders':bks,'order':order,'url':ncd.screenshot}
                return render(request,'distributor/vieworderother.html',params)
            else:
                user = Distributor.objects.filter(username=request.session['distributor']).first()
                order=orderreader.objects.filter(orderId=orderId).first()
                bks=orderbook.objects.filter(orderId=order)
                for bk in bks:
                    price=Buybook.objects.filter(username=user,name=bk.bookid.name).first()
                    bk.price=price.price
                cd=cod.objects.filter(orderId=order).first()
                params={'actions':actions,'type':'distributor','orderId':orderId,'orders':bks,'order':order,'coupon':cd.coupon}
                return render(request,'distributor/viewordercts.html',params)
