import re

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import date
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet, CommentForm
from post.models import Post, Tag, Like

User = get_user_model()
class PostListView(ListView):
    queryset = Post.objects.all().select_related('user').prefetch_related('images', 'comments', 'likes')
    # select_related('user') :
    #   Post와 1:1 또는 다대일 관계(ForeignKey)인 User 테이블을 JOIN하여 한 번의 쿼리로 가져옴
    #
    # prefetch_related('images') :
    #   Post와 1:N 관계인 PostImage 테이블에서,
    #   각 게시글(Post)과 연결된 이미지(PostImage)들을 미리 한 번에 가져와서(속도 개선)
    #   post.images.all() 사용 시 추가 쿼리 없이 참조할 수 있도록 최적화함

    template_name = 'post/list.html'
    paginate_by = 5
    ordering = ('-created_at', )

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = CommentForm()
        return data


# post_save: 게시글 저장 된 이후
@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, **kwargs):
    if created:
        hashtags = re.findall(r'#(\w{1,100})(?=\s|$)', instance.content)

        tags = [
            Tag.objects.ge_or_create(tag=hashtag)
            for hashtag in hashtags

        ]

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        # 부모 클래스의 get_context_data를 호출해서 기존 context 데이터를 받아옴
        data = super().get_context_data(**kwargs)

        # 'formset'이라는 이름으로 PostImageFormSet 인스턴스를 context에 추가
        # 이렇게 하면 템플릿에서 {{ formset }}으로 이미지 입력 폼 여러 개를 출력할 수 있음
        data['formset'] = PostImageFormSet()

        # 완성된 context 데이터를 반환
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user=self.request.user)


@csrf_exempt
@login_required()
def toggle_like(request):
    post_pk = request.POST.get('post_pk')
    if not post_pk:
        raise Http404()

    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()

    return JsonResponse({'created': created})


def search(request):
    search_type = request.GET.get('type')
    q = request.GET.get('q', '')
    print('search_type', search_type)
    print('q', q)

    if search_type in ['user', 'tag'] and q:
        if search_type == 'user':
            object_list = User.objects.filter(nickname__icontains=q)
        else:
            object_list = Post.objects.filter(tags__tag=q)

        context = {
            'object_list': object_list,

        }
        return render(request, f'search/search_{search_type}.html', context)
    return render(request, 'search/search.html')




























