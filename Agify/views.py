import requests
from django.http import JsonResponse
from django.shortcuts import render

def predict_form(request):
    return render(request, "predict_form.html")

def predict_age(request):
    if request.method == "POST":
        name = request.POST.get("name")
        response = requests.get(f"https://api.agify.io?name={name}")
        data = response.json()
        return render(request, "agify_result.html", {"data": data})