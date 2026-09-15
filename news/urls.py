from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('category/<int:category_id>/',views.get_category,name = "category"),
    # Страница одной новости: /news/<id>/ -> views.view_news
    path('news/<int:news_id>/',views.view_news,name="view_news"),
    path("news/add-news/",views.add_news,name= "add_news")
]
