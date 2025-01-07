from django.shortcuts import render, HttpResponse
from django.http import HttpRequest


# Create your views here.
def about(request: HttpRequest) -> HttpResponse:
    template_name = "pages/about.html"

    return render(request, template_name, {})


def rules(request: HttpRequest) -> HttpResponse:
    template_name = "pages/rules.html"

    return render(request, template_name, {})
