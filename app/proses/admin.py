from django.contrib import admin
from .models import Prose, Book, ProseBook

# Register your models here.
admin.site.register(Prose)
admin.site.register(Book)
admin.site.register(ProseBook)

