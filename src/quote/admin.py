from django.contrib import admin

from .models import QuoteModel, TypeQuote
# Register your models here.

admin.site.register(QuoteModel)

admin.site.register(TypeQuote)
