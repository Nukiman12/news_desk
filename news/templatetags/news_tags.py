"""
news_tags.py — кастомные шаблонные теги приложения news.

Подключаются в шаблоне через {% load news_tags %} (файл обязательно лежит
в news/templatetags/ рядом с __init__.py).

Нужны, чтобы получать список категорий прямо в шаблоне, не прокидывая его
через контекст в каждой вью (например, в общей шапке/блоке категорий).
"""
from django import template

from news.models import Category

# Регистр тегов/фильтров — Django ищет эту переменную при загрузке библиотеки.
register = template.Library()


@register.simple_tag()
def get_categories():
    """
    simple_tag: возвращает QuerySet всех категорий.

    Использование в шаблоне:
        {% get_categories as category %}
        {% for item in category %} ... {% endfor %}
    """
    return Category.objects.all()


@register.inclusion_tag('list_categories.html')
def show_categories():
    """
    inclusion_tag: сам рендерит шаблон list_categories.html.

    Возвращаемый словарь становится контекстом этого шаблона
    (categories -> список всех категорий).

    Использование в шаблоне:
        {% show_categories %}
    """
    categories = Category.objects.all()
    return {"categories": categories}
