from django.http    import HttpResponse
from django.shortcuts import render

from .forms import ContactForm
from quote.form import QuoteForm
from quote.models import TypeQuote
def home_page(request):
    form = TypeQuote()
    context = {
        "title" : "tongsuen logistic",
        "lang"  : "th",
        "quote_type"    :   TypeQuote.objects.all(),
        "form"  : form
    }
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('email'))
    return render(request, "homepage.html",context)

def home_page_th(request):
    form = TypeQuote()
    context = {
        "title" : "tongsuen logistic",
        "lang"  : "th",
        "quote_type"    :   TypeQuote.objects.all(),
        "form"  : form
    }
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('email'))
    return render(request, "homepage.html",context)

def home_page_en(request):
    form = TypeQuote()
    context = {
        "title" : "tongsuen logistic",
        "lang"  : "en",
        "quote_type"    :   TypeQuote.objects.all(),
        "form"  : form
    }
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('email'))
    return render(request, "homepage.html",context)

def home_page_cn(request):
    form = TypeQuote()
    context = {
        "title" : "tongsuen logistic",
        "lang"  : "cn",
        "quote_type"    :   TypeQuote.objects.all(),
        "form"  : form
    }
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('email'))
    return render(request, "homepage.html",context)
