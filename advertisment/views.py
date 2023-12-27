from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, User
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, get_object_or_404, render
from .forms import PostForm, ReplyForm
from .filters import PostFilter
from .tasks import send_message_reply_created, send_message_confirmed


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchNewsList(ListView):  # Отсортированные отклики
    model = Comment
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('post_list')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно оставили отклик'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Comment
    template_name = 'reply_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        form.instance.parent_id = self.request.POST.get('parent_id', None)
        return super().form_valid(form)


class ReplyDelete(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('post_list')


class ReplyConfirmed(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'reply_confirmed.html'
    form_class = ReplyForm
    context_object_name = 'confirmed'
    success_url = reverse_lazy('post_list')

