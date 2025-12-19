from django.contrib import admin
from .models import Post,Category,Aboutus

# Register your models here.
class PostAdmin(admin.ModelAdmin):

    list_display=('title','content') 
    search_fields=('title','content')
    list_filter=('created_at','category')
    list_per_page = 10
    ordering = ('created_at',)
    date_hierarchy = 'created_at'





admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Aboutus)
