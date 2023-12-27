from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


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

