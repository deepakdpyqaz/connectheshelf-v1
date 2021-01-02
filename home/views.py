from django.shortcuts import render,HttpResponse,redirect
from home.models import Donate,Contact
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template import loader
from django.template.loader import render_to_string
# Create your views here.
senderMail='connectheshelf@gmail.com'
def home(request):
    params={}
    if('reader' in request.session):
        actions=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
        params={'actions':actions,'type':'reader'}
    if('distributor' in request.session):
        actions=[{'name':'profile','link':''},{'name':'Manage books','link':'managebooks'},{'name':'View orders','link':'vieworders'}]
        params={'actions':actions,'type':'distributor'}
    return render(request,'index.html',params)

def logout(request):
    if('reader' in request.session):
        del request.session['reader']
    if('distributor' in request.session):
        del request.session['distributor']
    return redirect('home')

def donate(request):
    if(request.method=="GET"):
        params = {}
        if('reader' in request.session):
            actions=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
            params={'actions':actions,'type':'reader'}
        if('distributor' in request.session):
            actions=[{'name':'profile','link':''},{'name':'Manage books','link':'managebooks'},{'name':'View orders','link':'vieworders'}]
            params={'actions':actions,'type':'distributor'}
        return render(request,'donate.html',params)
    if(request.method=="POST"):
        name=request.POST['name']
        email=request.POST['email']
        contact=request.POST['contact']
        address=request.POST['address']
        books=request.POST['books']
        dnt=Donate(name=name,email=email,contact=contact,address=address,books=books)
        dnt.save()
        html_message = render_to_string('mail/donate.html', {'name': name,'books':books})
        plain_message = strip_tags(html_message)
        send_mail('ConnecTheShelf Donation', plain_message, senderMail, [senderMail, email], html_message=html_message, fail_silently=False)
    return redirect('home')

def contact(request):
    if(request.method=="GET"):
        params={}
        if('reader' in request.session):
            actions=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
            params={'actions':actions,'type':'reader'}
        if('distributor' in request.session):
            actions=[{'name':'profile','link':''},{'name':'Manage books','link':'managebooks'},{'name':'View orders','link':'vieworders'}]
            params={'actions':actions,'type':'distributor'}
        return render(request,'contact.html',params)
    if(request.method=="POST"):
        name=request.POST['name']
        email=request.POST['email']
        contact=request.POST['contact']
        query=request.POST['query']

        contact=Contact(name=name,email=email,contact=contact,query=query)
        contact.save()
        html_message = render_to_string('mail/contact.html', {'name': name})
        plain_message = strip_tags(html_message)
        send_mail('ConnecTheShelf Contact', plain_message, senderMail, [senderMail,email], html_message=html_message, fail_silently=False)
    return redirect('home')
