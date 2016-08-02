from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("<!DOCTYPE html><html><head><title>Home</title></head><body><h1>Home</h1></body></html>")
