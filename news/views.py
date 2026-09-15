from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from .models import News,Category
from .forms import NewsForm
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


def view_news(request,news_id):
    # Страница отдельной новости (по ссылке "читать дальше").
    # Ищем новость по pk; если такой нет — отдаём страницу 404,
    # а не падаем с необработанным исключением DoesNotExist.
    # (то же самое можно было бы сделать короче через get_object_or_404,
    # закомментированные варианты ниже оставлены как альтернатива)
    # news_item = get_object_or_404(News,pk= news_id)
    try:
        news_item = News.objects.get(pk= news_id)
        return render(request,'view_news.html',{'news_item':news_item})

    except News.DoesNotExist:
        raise Http404("not found")




def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # new = News.objects.create(**form.cleaned_data)
            new = form.save()
            return redirect(new)
    else:
        form = NewsForm()
    return render(request,"add_news.html",{'form':form})