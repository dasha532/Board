## "Доска объявлений"
### Описание проекта:
Написано веб-приложение, в котором можно добавлять персонажей с игры, оставлять отклики, присутствует регистрация и оповещение по почте.
Прописаны функции и шаблоны создания новости, удаления, комментариев и ответов.
Можно добавлять новость только в определенную категорию.

### Модели в базе данных:
 ```
tank = 'Танк'
healer = 'Хил'
damager = 'ДД'
guild_master = 'Гилдмастер'
quest_giver = 'Квестгивер'
smith = 'Кузнец'
tanner = 'Кожевник'
potion_maker = 'Зельевар'
spell_master = 'Мастер заклинаний'

CATEGORIES = [
    (tank, 'Танк'),
    (healer, 'Хил'),
    (guild_master, 'Гилдмастер'),
    (quest_giver, 'Квестгивер'),
    (smith, 'Кузнец'),
    (tanner, 'Кожевник'),
    (potion_maker, 'Зельевар'),
    (spell_master, 'Мастер заклинаний')
]


class Category(models.Model):
    category = models.CharField(max_length=17, choices=CATEGORIES, default=tank)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Название")
    text = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

 ```

### Технологии и библиотеки:
- Django              4.2.3- 
- django-filter       23.2
- djangorestframework 3.14.0
- importlib-metadata  6.8.0
- Markdown            3.4.4
- Pillow              10.0.0
- pip                 22.3.1
- psycopg2-binary     2.9.6
- python-dotenv       1.0.0
- pytz                2023.3
- setuptools          65.5.1
- sqlparse            0.4.4
- typing_extensions   4.7.1
- tzdata              2023.3
- wheel               0.38.4
- zipp                3.16.2
- drf-yasg            1.21.7

#### Языки :
|     | Язык   |
|----:|--------|
|   1 | Python |
|   2 | CSS    |
|   3 | HTML   |