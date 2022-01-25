from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, you are at the poll index.")