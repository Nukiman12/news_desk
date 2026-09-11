from django.contrib import admin
from .models import News,Category
# Register your models here.

class NewsAdminL(admin.ModelAdmin):
    list_display = ('id','news', 'description','created_at','content','Category')
    list_display_links = ('id','news')
    search_fields = ('title','content')    

admin.site.register(News,NewsAdminL)
admin.site.register(Category)