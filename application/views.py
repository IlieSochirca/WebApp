from django.views import generic
from django.shortcuts import render, render_to_response, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, request
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime, operator
from django.db.models import Q
from .forms import *
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.core.urlresolvers import reverse_lazy
from .models import *
from .models import Comment, Group, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

def start_page(request):
    now = datetime.datetime.now()
    return render(request,'application/startpage.html', locals())

def view_profile(request):
    return render(request, 'registration/profile.html')

# REGISTRATION VIEW BASED CLASSES

class RegitrationView(CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(RegitrationView, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('/')

  # PROFILE EDIT FUNCTION
@login_required()  #only logged users should access this
def edit_profile(request):
    pk=request.user.pk
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('phone', 'birth_date', 'hobby', 'city','current_project', 'image'))
    #we exposed above the fields we want from Profile Model, the fields from User Model were exposed in UserForm
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method=="POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/profile/')

        return render(request, "registration/profile-edit.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

# GROUP CLASS BASED VIEWS

class HomeView(generic.ListView):
    now = datetime.datetime.now()
    template_name = 'application/home.html'
    context_object_name = "all_groups"
    paginate_by = 4
    queryset = Group.objects.all() # this is what will be displayed on our webpage

    def get_queryset(self):
        result = super(HomeView, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            from functools import reduce
            result = result.filter(
                # reduce(operator.and_,
                #        (Q(category__icontains=q)for q in query_list))|
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )
        return result

# class GroupDetailView(generic.DetailView):
#     model= Group
#     template_name = 'application/group_detail.html'

#  USING LISTVIEW CLASS INSTEAD OF DETAILVIEW IN ORDER TO MAKE THE PAGINATION

class PostGroupDetailView(generic.ListView):
    model = Post
    context_object_name = 'all_posts'
    template_name = 'application/group_detail.html'
    paginate_by = 4

    def get_queryset(self):
        self.group = get_object_or_404(Group, pk = self.kwargs.get('pk'))
        queryset = self.group.post_set.order_by('-created')
        # result = super(PostGroupDetailView, self).get_queryset().filter(pk=self.kwargs.get('pk'))

        query_list = self.request.GET.get("p")
        if query_list:
            query_list = query_list.split()
            from functools import reduce
            queryset = queryset.filter(
                reduce(operator.and_,
                       (Q(name__icontains=p) for p in query_list))
            )
            return queryset
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['group'] = self.group
        return super(PostGroupDetailView, self).get_context_data(**kwargs)


# OR WE CAN CREATE SEPARATE CLASSES FOR THIS SEARCH ENGINES, which need separate url patterns to be declared
#
# class PostSearchListView(PostList):
#     def get_queryset(self):
#         result2 = super(PostSearchListView, self).get_queryset()
#         query = self.request.GET.get("p")
#         if query:
#             query_list=query.split()
#             from functools import reduce
#             result2 = result2.filter(
#                 reduce(operator.and_,
#                           (Q(name__icontains=p)for p in query_list))
#                 )
#         return result2


# class GroupSearchListView(HomeView):
#     def get_queryset(self):
#         result = super(GroupSearchListView, self).get_queryset()
#         query = self.request.GET.get("q")
#         if query:
#             query_list = query.split()
#             from functools import reduce
#             result = result.filter(
#                 # reduce(operator.and_,
#                 #        (Q(category__icontains=q)for q in query_list))|
#                 reduce(operator.and_,
#                        (Q(name__icontains=q)for q in query_list))
#             )
#         return result

class GroupCreate(CreateView):
    model = Group
    fields = ['name', 'category', 'description', 'is_favorite']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.added_by = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('application:home')

class GroupUpdate(UpdateView):
    model = Group
    fields = ['name', 'category', 'description', 'is_favorite']
    success_url = reverse_lazy('application:home')

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('application:home')  # this is the path where the user will be redirected after he delete a group


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'application/post_detail.html'


# POST LIKES BUTTONS FOR POSTS AND COMMENTS
#this view finds the post with the post_pk id passed from AJAX GET and is updating the number of likes and return this number to AJAX

@login_required 
def PostLike(request):
    user = request.user
    post_id= None
    if request.method =='GET':   #the GET request is necessary to identify the id of the post we want to like
        post_id = request.GET['post_pk']

    likes=0
    if post_id:
        post = Post.objects.get(id=int(post_id)) # in this moment, we are declaring a vriable which will be equal to each of the post using it's unique id
        print(post_id, post)
        if post:
            if user in post.post_user_likes.all():
                post.post_user_likes.remove(user)
                likes = post.likes - 1
            else:
                post.post_user_likes.add(user)
                likes = post.likes+1
        post.likes = likes
        post.save()
    return HttpResponse(likes)


class PostCreate(CreateView):
    model = Post
    fields = ['name','group_post', 'description', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.posted_by = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

class PostUpdate(UpdateView):
    model = Post
    fields = ['name','group_post', 'description']

    def get_success_url(self): # this is done to redirect the user for the last page where he came from, keep attention to mention the id, ok of the page element
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

class PostDelete(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

class CommentView(ListView):
    model = Comment


class CommentCreate(CreateView):
    model= Comment
    fields = ['description', 'comment_post', 'is_active', 'is_favorite', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.added_by = self.request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['description', 'comment_post', 'is_active', 'is_favorite', 'image']


@login_required
def CommentLike(request):
    user = request.user
    comment_id=None
    if request.method =='GET':
        comment_id = request.GET['comment_pk']
    likes=0
    if comment_id:
        comment = Comment.objects.get(id=int(comment_id))
        if comment:
            if user in comment.comment_user_likes.all():
                print("add")
                comment.comment_user_likes.remove(user)
                likes = comment.likes-1
            else:
                print("remove")
                comment.comment_user_likes.add(user)
                likes = comment.likes+1
        comment.likes = likes
        comment.save()
    return HttpResponse(likes)

class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        group=self.object.comment_post.group_post.pk
        return reverse('application:post_detail', kwargs={"group_pk":group, "pk" : self.kwargs.get('post_pk'),})

