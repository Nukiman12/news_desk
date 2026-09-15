from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=199)


    # Каноничный URL категории — страница со списком её новостей
    # (url name = 'category' из news/urls.py). Позволяет в шаблонах
    # писать {{ item.get_absolute_url }} вместо {% url 'category' item.pk %}.
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id":self.pk})


    
    def __str__(self):
        return self.title


class News(models.Model):
    # upload_to указывает подпапку внутри MEDIA_ROOT (media/), а не сам MEDIA_ROOT —
    # иначе новые файлы попадали бы в media/media/. default — путь к заглушке,
    # которая реально лежит в media/default/new.jpg.
    image = models.ImageField(upload_to="news/", blank=True, null=True, default='default/new.jpg')
    news = models.CharField(max_length=100)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    Category = models.ForeignKey('Category', on_delete = models.PROTECT,null = True,default=1)




    # Каноничный URL самой новости — страница отдельной новости
    # (url name = 'view_news' из news/urls.py).
    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id":self.pk})

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.news