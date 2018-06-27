from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(req):
    rst = "hello, kvm index"
    return HttpResponse(rst)
    
