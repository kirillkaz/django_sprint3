from datetime import datetime

from django.db.models import Q
from django.http import Http404, HttpRequest
from django.shortcuts import HttpResponse, render
from django.utils import timezone

from .models import Category, Post


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    template_name = "blog/index.html"

    posts = Post.objects.filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=datetime.now())
    ).order_by("-id")[:5]

    context = {"post_list": posts}

    return render(request, template_name, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    template_name = "blog/detail.html"

    post = Post.objects.filter(id=id).first()

    if not post:
        raise Http404(f"Error. Post with {id=} was not found.")

    if (
        post.pub_date > timezone.make_aware(datetime.now())
        or post.is_published is False
        or post.category.is_published is False
    ):
        raise Http404()

    context = {
        "post": post,
    }

    return render(request, template_name, context)


def category(request: HttpRequest, category_slug: str) -> HttpResponse:
    template_name = "blog/category.html"

    category = Category.objects.get(slug=category_slug)

    if not category.is_published:
        raise Http404()

    posts = Post.objects.filter(
        Q(category__slug=category_slug)
        & Q(pub_date__lte=datetime.now())
        & Q(is_published=True)
    )

    context = {
        "category": category,
        "post_list": posts,
    }

    return render(request, template_name, context)
