from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('category/<int:category_id>/',views.get_category,name = "category")
]
