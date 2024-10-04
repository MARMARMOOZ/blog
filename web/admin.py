from django.contrib import admin
from .models import *
# Register your models here.
#accsesing to important models trough admin page
admin.site.register(Topic)
admin.site.register(Token)
admin.site.register(Comments)