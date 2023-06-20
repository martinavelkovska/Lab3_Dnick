from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Avtor, Komentar, Post, Blok
from .forms import PostForm, BlokForm

# Create your views here.
@login_required
def posts(request):
    blocked = Blok.objects.filter(blokiran__user=request.user).values_list('bloker__user', flat=True)
    qs = Post.objects.exclude(avtor__user=request.user).exclude(avtor__user__in=blocked)
    context = {"posts": qs}
    return render(request, "index.html", context=context)

@login_required
def addpost(request):
    if request.method == "POST":
        form_data = PostForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.avtor = Avtor.objects.get(user=request.user)
            post.save()

            return redirect("posts")

    return render(request, "add.html", {"form": PostForm})

def profile(request):
    user = get_object_or_404(Avtor, user=request.user)
    avtor_list = [user]
    posts = Post.objects.filter(avtor=user)
    context = {"users": avtor_list, "posts": posts}
    return render(request, "profile.html", context=context)

def blocked(request):
    if request.method == "POST":
        form_data = BlokForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            blok = form_data.save(commit=False)
            avtor = get_object_or_404(Avtor, user=request.user)
            blok.bloker = avtor
            blok.save()
            return redirect("blocked")

    blocks = Blok.objects.filter(bloker__user=request.user)
    blocked_users = Avtor.objects.filter(user__in=blocks.values_list("blokiran__user", flat=True)).exclude(user=request.user)
    form = BlokForm()

    return render(request, "blocked.html", {"form": form, "users": blocked_users})

