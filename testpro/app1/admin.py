from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Comment)
admin.site.register(Any)