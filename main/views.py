from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    BlogForm,
    ContactForm,
    GalleryForm,
    ProjectForm,
    SkillForm,
    ThemedAuthenticationForm,
)
from .models import BlogPost, ContactMessage, GalleryImage, Project, Skill


def home(request):
    skills = Skill.objects.all()
    projects = Project.objects.all()
    gallery_items = GalleryImage.objects.all()
    blog_posts = BlogPost.objects.filter(is_published=True)

    paginator = Paginator(blog_posts, 4)
    page_number = request.GET.get('page')
    blog_page = paginator.get_page(page_number)

    contact_form = ContactForm()
    if request.method == 'POST' and request.POST.get('form_type') == 'contact':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
        messages.error(request, 'Please correct the form errors.')

    context = {
        'skills': skills,
        'projects': projects,
        'gallery_items': gallery_items,
        'blog_page': blog_page,
        'contact_form': contact_form,
        'project_form': ProjectForm(),
        'blog_form': BlogForm(),
        'gallery_form': GalleryForm(),
        'experience_years': 3,
        'happy_clients': 12,
        'current_year': timezone.now().year,
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = ThemedAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Welcome back!')
        return redirect('home')
    context = {'form': form, 'current_year': timezone.now().year}
    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def skill_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = SkillForm(request.POST or None, instance=skill)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Skill updated.')
        return redirect('home')
    context = {'form': form, 'skill': skill, 'current_year': timezone.now().year}
    return render(request, 'dashboard/skill_form.html', context)


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Project added!')
        return redirect('home')
    context = {'form': form, 'project': None, 'current_year': timezone.now().year}
    return render(request, 'dashboard/project_form.html', context)


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Project updated.')
        return redirect('home')
    context = {'form': form, 'project': project, 'current_year': timezone.now().year}
    return render(request, 'dashboard/project_form.html', context)


@login_required
@require_POST
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.info(request, 'Project removed.')
    return redirect('home')


@login_required
def gallery_create(request):
    form = GalleryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Image uploaded.')
        return redirect('home')
    return render(
        request,
        'dashboard/gallery_form.html',
        {'form': form, 'current_year': timezone.now().year},
    )


@login_required
@require_POST
def gallery_delete(request, pk):
    item = get_object_or_404(GalleryImage, pk=pk)
    item.delete()
    messages.info(request, 'Image removed.')
    return redirect('home')


@login_required
def blog_create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        blog_post = form.save(commit=False)
        blog_post.author = request.user
        blog_post.save()
        messages.success(request, 'Blog post published.')
        return redirect('home')
    context = {'form': form, 'post': None, 'current_year': timezone.now().year}
    return render(request, 'dashboard/blog_form.html', context)


@login_required
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Blog post updated.')
        return redirect('home')
    context = {'form': form, 'post': post, 'current_year': timezone.now().year}
    return render(request, 'dashboard/blog_form.html', context)


@login_required
@require_POST
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.info(request, 'Blog post deleted.')
    return redirect('home')


@login_required
def contact_messages(request):
    messages_qs = ContactMessage.objects.all()
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    context = {'messages_list': messages_qs, 'current_year': timezone.now().year}
    return render(request, 'dashboard/contact_messages.html', context)


def custom_404(request, exception):
    return render(request, 'errors/404.html', {'current_year': timezone.now().year}, status=404)


def custom_500(request):
    return render(request, 'errors/500.html', {'current_year': timezone.now().year}, status=500)
