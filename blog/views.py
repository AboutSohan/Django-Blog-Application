from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from .forms import CommentForm


# Create your views here.
def home_view(request):
    blogs = BlogInfo.objects.all().first()
    #pagination
    queryset = BlogPost.objects.filter(status = 'publish')
    per_page = 10
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    fetured_one = BlogPost.objects.filter(featured_post = True)[:1].get()
    fetured_two = BlogPost.objects.filter(featured_post = True)[1:2].get()
    fetured_three = BlogPost.objects.filter(featured_post = True)[2:3].get()

    context = {'posts':posts, 'blogs': blogs, 'fetured_one':fetured_one, 'fetured_two':fetured_two, 'fetured_three':fetured_three}
    template_name = 'tech-index.html'
    return render(request, template_name, context)

def singlePost(request, slug):
    all_post = BlogPost.objects.filter(status = 'publish')[:5]
    blogs = BlogInfo.objects.all().first()

    myPost = get_object_or_404(BlogPost, slug=slug)
    theme_name = 'tech-single.html'

    # comment section/system start here
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    context = {'myPost':myPost, 'all_post':all_post,'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'blogs':blogs}
    return render(request, theme_name, context)
