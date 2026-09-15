# Как устроен и как создавался проект «Новости» (Django)

Этот файл подробно описывает шаги, из которых собран проект: от создания
Django-проекта до текущего состояния с моделями, вьюхами, шаблонами,
кастомными тегами и стилями.

Стек: **Python + Django 6.1.1**, база данных — **SQLite** (`db.sqlite3`),
шаблонизатор — стандартный Django Template Language.

---

## 1. Создание виртуального окружения и установка Django

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install django
```

Появилась папка `venv/` — окружение проекта.

---

## 2. Создание Django-проекта

```bash
django-admin startproject core .
```

Точка в конце — проект создаётся в текущей папке, а не во вложенной.
В результате появился пакет `core/` с файлами:

- `core/settings.py` — настройки проекта
- `core/urls.py` — корневой роутинг
- `core/wsgi.py`, `core/asgi.py` — точки входа для серверов
- `manage.py` — служебный скрипт (`runserver`, `migrate`, `startapp` и т.д.)

---

## 3. Создание приложения `news`

```bash
python manage.py startapp news
```

Появилась папка `news/` со стандартной структурой Django-приложения:
`models.py`, `views.py`, `admin.py`, `apps.py`, `migrations/`.

Приложение зарегистрировано в `core/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'news.apps.NewsConfig',
]
```

---

## 4. Настройка `core/settings.py`

Ключевые изменения относительно шаблона Django «по умолчанию»:

- **Шаблоны** — добавлена папка `templates/` в корне проекта, чтобы
  Django искал `.html`-файлы не только внутри приложений:

  ```python
  TEMPLATES = [
      {
          ...
          'DIRS': [BASE_DIR / 'templates'],
          'APP_DIRS': True,
          ...
      },
  ]
  ```

- **Статика** — добавлена папка `static/` в корне проекта:

  ```python
  STATIC_URL = 'static/'
  STATICFILES_DIRS = [BASE_DIR / 'static']
  ```

- **Локализация** — язык и часовой пояс под проект:

  ```python
  LANGUAGE_CODE = 'ru'
  TIME_ZONE = 'Asia/Almaty'
  ```

- **База данных** оставлена стандартной — SQLite (`db.sqlite3`).

---

## 5. Модели (`news/models.py`)

Две модели: категория новости и сама новость.

```python
class Category(models.Model):
    title = models.CharField(max_length=199)


class News(models.Model):
    news = models.CharField(max_length=100)          # заголовок
    description = models.TextField()                 # краткое описание
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()                      # полный текст
    Category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                  null=True, default=1)
```

Особенности:

- `Category` в `News` — это **ForeignKey**, а не строка: одна новость
  относится к одной категории, но у категории может быть много новостей.
- `on_delete=models.PROTECT` — нельзя удалить категорию, если на неё
  ссылаются новости (защита от «осиротевших» новостей).
- `auto_now_add=True` у `created_at` — дата подставляется автоматически
  при создании и не редактируется вручную.

После описания моделей применены миграции — Django сам создаёт таблицы
в БД на основе классов моделей:

```bash
python manage.py makemigrations   # создаёт news/migrations/0001_initial.py
python manage.py migrate          # применяет миграции к db.sqlite3
```

---

## 6. Админка (`news/admin.py`)

Модели зарегистрированы в стандартной Django-админке, чтобы новости и
категории можно было добавлять/редактировать без написания форм:

```python
class NewsAdminL(admin.ModelAdmin):
    list_display = ('id', 'news', 'description', 'created_at', 'content', 'Category')
    list_display_links = ('id', 'news')
    search_fields = ('title', 'content')

admin.site.register(News, NewsAdminL)
admin.site.register(Category)
```

Чтобы попасть в админку, нужен суперпользователь:

```bash
python manage.py createsuperuser
```

Дальше админка доступна по `/admin/`.

---

## 7. Вьюхи (`news/views.py`)

Две простые функции-вью:

```python
def main(request):
    news = News.objects.all()
    context = {'title': 'News', 'news': news}
    return render(request, 'main.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(Category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, "category.html", {'news': news, 'category': category})
```

- `main` — отдаёт главную страницу со всеми новостями.
- `get_category` — принимает `category_id` из URL и отдаёт только те
  новости, у которых `Category_id` совпадает с этим значением.

---

## 8. Маршрутизация (URLs)

Сначала — локальные адреса приложения `news/urls.py`:

```python
urlpatterns = [
    path('', views.main, name='main'),
    path('category/<int:category_id>/', views.get_category, name='category'),
]
```

Затем эти адреса подключены к проекту в `core/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]
```

Именованные маршруты (`name='main'`, `name='category'`, `name='view_news'`)
позволяют в шаблонах ссылаться на URL по имени, а не хардкодить строку:
`{% url 'main' %}`, `{% url 'category' item.pk %}`.

---

## 9. Шаблоны (`templates/`)

Структура папки `templates/`:

```
templates/
├── base.html            # общий каркас (шапка + подвал)
├── main.html            # главная страница ("Лента")
├── category.html        # страница одной категории
├── view_news.html       # страница одной новости
├── list_categories.html # список категорий (рендерится тегом show_categories)
└── inc/
    └── _category.html   # переиспользуемый блок со списком категорий
```

### `base.html`

Базовый шаблон с общей шапкой (логотип + навигация) и подвалом.
Всё изменяемое содержимое находится внутри `{% block content %}`.

### `main.html` и `category.html`

Оба наследуются от `base.html`:

```django
{% extends "base.html" %}
{% block content %}
    ...
{% endblock %}
```

и переопределяют только `content` — так шапка/подвал не дублируются в
каждом файле.

- `main.html` выводит **все** новости и подключает блок категорий
  (`{% include 'inc/_category.html' %}`).
- `category.html` выводит новости, отфильтрованные по конкретной
  категории (контекст `news` уже отфильтрован во вью `get_category`).

В обоих шаблонах используется `{% for item in news %} ... {% empty %} ... {% endfor %}` —
если список новостей пуст, вместо карточек показывается заглушка
«Пока нет новостей».

### `inc/_category.html` и `list_categories.html`

Блок категорий вынесен отдельно, чтобы не дублировать разметку —
подробнее в следующем пункте про кастомные теги.

---

## 10. Кастомные шаблонные теги (`news/templatetags/news_tags.py`)

Чтобы получать список категорий прямо в шаблоне (без передачи через
каждую вью), создана папка `templatetags` внутри приложения `news`:

```
news/
└── templatetags/
    ├── __init__.py       # обязателен, чтобы Django видел пакет тегов
    └── news_tags.py
```

```python
from django import template
from news.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {"categories": categories}
```

Разница между двумя тегами:

- **`get_categories`** (`simple_tag`) — просто возвращает значение,
  которое нужно самому сохранить в переменную и вывести в шаблоне:

  ```django
  {% load news_tags %}
  {% get_categories as category %}
  {% for item in category %}
      <a href="{% url 'category' item.pk %}">{{ item.title }}</a>
  {% endfor %}
  ```

- **`show_categories`** (`inclusion_tag`) — сам рендерит отдельный
  шаблон (`list_categories.html`), подставляя туда `categories`:

  ```django
  {% show_categories %}
  ```

Оба варианта в проекте используются одновременно в `inc/_category.html`
как демонстрация двух подходов к одной и той же задаче.

---

## 11. Статика и стили (`static/css/style.css`)

Django находит статику через `STATICFILES_DIRS` (см. пункт 4) и тег
`{% load static %}` в начале `base.html`:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

В `style.css` — единая тема оформления на CSS-переменных
(`:root { --bg; --surface; --accent; ... }`) с автоматической светлой/
тёмной темой через `@media (prefers-color-scheme: dark)`, стили шапки,
карточек новостей, чипов категорий и подвала.

---

## 12. Запуск проекта локально

```bash
venv\Scripts\activate
python manage.py migrate
python manage.py createsuperuser   # один раз, для доступа к /admin/
python manage.py runserver
```

- `http://127.0.0.1:8000/` — главная страница со списком новостей
- `http://127.0.0.1:8000/category/<id>/` — новости одной категории
- `http://127.0.0.1:8000/news/<id>/` — отдельная новость
- `http://127.0.0.1:8000/admin/` — админка для добавления новостей и категорий

---

## 13. Страница отдельной новости и `get_absolute_url` (в разработке, ещё не закоммичено)

Раньше со страницы «Лента» перейти на конкретную новость было нельзя —
были только списки (`main.html`, `category.html`). Добавлена страница
одной новости и ссылка «читать дальше», ведущая на неё.

### `get_absolute_url` в моделях (`news/models.py`)

Вместо того чтобы в каждом шаблоне собирать URL через
`{% url 'category' item.pk %}` / `{% url 'view_news' item.pk %}`,
у моделей появился стандартный для Django метод `get_absolute_url`:

```python
class Category(models.Model):
    ...
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})


class News(models.Model):
    ...
    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk})
```

`reverse()` строит URL по имени маршрута — так же, как тег `{% url %}`,
только на уровне Python/модели. В шаблоне это теперь просто:

```django
<a href="{{ item.get_absolute_url }}">...</a>
```

`list_categories.html` и ссылка «читать дальше» в `main.html` уже
переведены на `get_absolute_url` вместо `{% url %}`.

### Новый маршрут (`news/urls.py`)

```python
path('news/<int:news_id>/', views.view_news, name="view_news")
```

### Новая вью (`news/views.py`)

```python
def view_news(request, news_id):
    try:
        news_item = News.objects.get(pk=news_id)
        return render(request, 'view_news.html', {'news_item': news_item})
    except News.DoesNotExist:
        raise Http404("not found")
```

Если новости с таким `id` нет — отдаётся стандартная страница 404,
а не падение с `DoesNotExist`. (В коде оставлен закомментированный
более короткий вариант через `get_object_or_404` как альтернатива —
делает то же самое в одну строку.)

### Новый шаблон (`templates/view_news.html`)

Наследуется от `base.html`, как и остальные страницы, и выводит один
объект `news_item` — по сути та же карточка новости, что и в
`main.html`, но без остального списка.

> Эти изменения ещё не закоммичены в git — раздел описывает уже
> сделанную, но пока не зафиксированную работу.

---

## 14. Возможные следующие шаги

Не сделано в текущей версии, но логично напрашивается дальше:

- Пагинация списка новостей.
- Поиск по новостям (поле `search_fields` в админке уже намекает на это).
- Вынос `SECRET_KEY` и `DEBUG` в переменные окружения перед деплоем.
