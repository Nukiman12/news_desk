from django.shortcuts import render
from .models import News,Category
# Create your views here.
def main(request):
    news = News.objects.all()
    context = {'title': 'News', 
                'news': news,
                }
    return render(request, 'main.html', context=context)


def get_category(request,category_id):
    news = News.objects.filter(Category_id = category_id)
    
    category = Category.objects.get(pk = category_id)
    return render(request, "category.html",{'news':news, 'category':category})