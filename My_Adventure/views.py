from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

def post_share(request, post_id):
    post=get_object_or_404(Post, id=post_id, status='published')
    sent=False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends you reading"{}"'.format(cd['name'],cd['email'],post.title)
            messege='Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,messege,'admin@My_Adventure.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request, 'My_Adventure/share.html', {'post':post,
                                                       'form':form,
                                                       'sent':sent})

'''class PostListView(ListView):
    queryset = Post.published.all()
    #model=Post  Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name='My_Adventure/post/list.html' '''

def post_list(request, tag_slug=None):
    #posts=Post.published.all()
    object_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,
                  'My_Adventure/post/list.html',
                  {'posts': posts,
                   'tag':tag})

def post_details(request, year, month, day, post):
    post=get_object_or_404(Post, slug=post,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)

    #list of active components for this post
    comments=post.comments.filter(active=True)
    new_comment=None

    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
            comment_form=CommentForm()
    
    return render(request,
                  'My_Adventure/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form})
