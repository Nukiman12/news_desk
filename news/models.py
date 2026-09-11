from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=199)



    
    def __str__(self):
        return self.title


class News(models.Model):
    news = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    Category = models.ForeignKey('Category', on_delete = models.PROTECT,null = True,default=1)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.news