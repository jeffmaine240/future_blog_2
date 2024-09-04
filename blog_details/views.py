from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity

from blog_details.models import Author, BlogPost, Comment, Tag, Profile
from blog_details.forms import SearchForm, ContactForm, CommentPostForm , CreatePostForm, RegisterForm


# Create your views here.
class StartingPageView(View):
    def get(self, request, tag_caption=None):
        form = SearchForm()
        query = None
        tag = None
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                post_list = BlogPost.objects.annotate(
                    similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
        else:
            post_list = BlogPost.objects.all().order_by()
            if tag_caption:
                tag = get_object_or_404(Tag, caption=tag_caption)
                post_list = BlogPost.objects.all().filter(tag__in=[tag])

        paginator = Paginator(post_list, 1)
        page_number = request.GET.get('page', 1)
        print(page_number)
        try:
            details = paginator.page(page_number)
        except EmptyPage:
            details = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            details = paginator.page(1)
        return render(request, "blog_details/index.html", {"all_posts": details, "tag": tag, "query_form": form, "query": query})

        
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            redirect_path = reverse("home")
            return HttpResponseRedirect(redirect_path)
        form = RegisterForm()
        return render(request, "blog_details/register.html", {"form": form, "post_type": "Register"})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            redirect_path = reverse("home")
            return HttpResponseRedirect(redirect_path)
        return render(request, "blog_details/register.html", {"form": form, "post_type": "Register"})


class PostDetailView(View):
    login_url = reverse_lazy('login')
    def get_post(self, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        return post
    
    def get(self, request, slug):
        post = self.get_post(slug)
        all_comment = Comment.objects.filter(post=post)
        if post != None:
            form = CommentPostForm()
            return render(request, "blog_details/post.html", {"post":post, "form": form, "comments": all_comment})
        raise Http404()
    
    @method_decorator(login_required)
    def post(self, request, slug):
        submitted_form = CommentPostForm(request.POST)
        post = self.get_post(slug)
        if submitted_form.is_valid():
            cd = submitted_form.cleaned_data
            details = cd["comment_details"]
            comment = Comment(comment_details=details, post=post, comment_author=self.request.user )
            comment.save()
            redirect_path = reverse("specific", args=[slug])
            return HttpResponseRedirect(redirect_path)
        all_comment = Comment.objects.filter(post=post)
        if post != None:
            return render(request, "blog_details/post.html", {"post":post, "form": submitted_form, "comments": all_comment})


class AboutView(View):
    def get(self, request):
        return render(request, "blog_details/about.html")

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "blog_details/contact.html", {"form":form, "link_generated": False})
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            author_email = Author.objects.all()[0].email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']
            mailto_link = (
                f"mailto:{author_email}?subject={name} has contacted you&body=Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            return render(request, "blog_details/contact.html", {"form":form, "link": mailto_link,  "link_generated": True})
        return render(request, "blog_details/contact.html", {"form":form,  "link_generated": False})

class DeletePostView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    # was suppose to be def delete(self, request, slug):
    def get(self, request, slug):
        if self.request.user.id == 1:
            selected = BlogPost.objects.get(slug=slug)
            selected.delete()
            redirect_path = reverse("home")
            return HttpResponseRedirect(redirect_path)
        raise Http404('not authorized')
    
class UpdatePostView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request, slug):
        selected = BlogPost.objects.get(slug=slug)
        form = CreatePostForm(instance=selected)
        return render(request, "blog_details/make-post.html", {"form": form, "post_type": "Edit Post"})
    
    
    def post(self, request, slug):
        selected = get_object_or_404(BlogPost, slug=slug)
        form = CreatePostForm(instance=selected, data=request.POST, files=request.FILES)
        if form.is_valid():
            # selected = BlogPost.objects.get(slug=slug)
            selected.delete()
            form.save()
            redirect_path = reverse("home")
            return HttpResponseRedirect(redirect_path)
        return render(request, "blog_details/make-post.html", {"form": form, "post_type": "New Post"})
    
class CreatePostView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request):
        form = CreatePostForm()
        return render(request, "blog_details/make-post.html", {"form": form, "post_type": "New Post"})
    

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redirect_path = reverse("home")
            return HttpResponseRedirect(redirect_path)
        return render(request, "blog_details/make-post.html", {"form": form, "post_type": "New Post"})

class PostSearchView(View):
    def get(self, request):
        form = SearchForm()
        query = None
        results = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = BlogPost.objects.annotate(
                    similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
            return render(request, "blog_details/index.html", {"all_posts": results, "query": query, "form": form})

