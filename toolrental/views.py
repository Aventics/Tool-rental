from django.shortcuts import render
from django.http import JsonResponse

def home_page(request):
    return JsonResponse({'message':'OK'})