from celery import shared_task
import datetime
from django.conf import settings

from .models import Post, Category, User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail


@shared_task
def all_week_posts():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_created__gte=last_week)
    categories = set(posts.values_list('category__category', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('user__email', flat=True))
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,

        }
    )
    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_message_reply_created(email):
    send_mail(
        subject=f'Вы получили отклик на свое сообщение',
        message=f'На ваше объявление оставили отклик! Зайдите проверить!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )


@shared_task
def send_message_confirmed(email):
    send_mail(
        subject=f'Ваш отклик был принят.',
        message=f'Ваш отклик был принят.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
