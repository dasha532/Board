from django.urls import path
from .views import PostsList, PostDetail, SearchNewsList, PostCreate, PostUpdate, PostDelete, \
   ReplyCreate, ReplyDelete, ReplyConfirmed

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search/', SearchNewsList.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('news/<int:pk>/comment/', ReplyCreate.as_view(), name='comment_create'),
   path('comment/<int:pk>/delete/', ReplyDelete.as_view(), name='comment_delete'),
   path('comment/<int:pk>/confirm/', ReplyConfirmed.as_view(), name='comment_confirm'),
]