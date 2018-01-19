"""tongsuenlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from django.contrib import admin

from .views import home_page, home_page_th, home_page_en, home_page_cn
from quote.views import pdf_generate
urlpatterns = [
    url(r'^$', home_page),
    url(r'^admin/', admin.site.urls),
    url(r'^th/', home_page_th),
    url(r'^en/', home_page_en),
    url(r'^cn/', home_page_cn),
    url(r'^pdfgenertate/', pdf_generate,name="gen_pdf"),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
