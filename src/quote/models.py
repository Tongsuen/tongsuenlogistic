
import random
import os
from datetime import datetime

from django.db import models

# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(isinstance, filename):
    new_filename = random.randint(1,902323345)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "quote/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class TypeQuote(models.Model):

    name_type_th = models.CharField(max_length=30)
    name_type_en = models.CharField(max_length=30)
    name_type_cn = models.CharField(max_length=30)
    detail_type = models.CharField(max_length=120,default="no description here.")

    def __str__(self):
        return self.name_type_en

class QuoteModel(models.Model):
    type_quote = models.ForeignKey(TypeQuote,on_delete=models.CASCADE,default=None)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60,default='')
    name_company = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    tel_office = models.CharField(max_length=20,default=None,null=True, blank=True)
    tel_mobile = models.CharField(max_length=20,default=None,null=True,  blank=True)
    tel_fax = models.CharField(max_length=20,default=None,null=True,  blank=True)
    type_product = models.CharField(max_length=60)
    direction = models.CharField(max_length=110)
    detail = models.TextField()
    file_path = models.FileField(upload_to=upload_image_path,null=True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
