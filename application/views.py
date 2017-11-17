from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.template import RequestContext
from django.views import generic
from django.shortcuts import render, render_to_response, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, request, Http404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime, operator
from django.db.models import Q
from dal import autocomplete
from django.views.generic.edit import ModelFormMixin

from application.mixins import UserAuthorMixinPost, UserAuthorMixin
from .forms import *
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.core.urlresolvers import reverse_lazy
from .models import *
from .models import Comment, Group, Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def start_page(request):
    now = datetime.datetime.now()
    return render(request,'application/startpage.html', locals())

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        userprofile = User.objects.get(username=username)
        return render(request, 'registration/profile.html', locals())

def get_user_profile(request,username):
    userprofile = get_object_or_404(User, username=username)
    return render(request, 'registration/user_profile.html', locals())

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
                    return render(request, 'registration/profile.html')
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
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )
        return result

#  USING LISTVIEW CLASS INSTEAD OF DETAILVIEW IN ORDER TO MAKE THE PAGINATION

class PostGroupDetailView(generic.ListView):
    model = Post
    context_object_name = 'all_posts'
    template_name = 'application/group_detail.html'
    paginate_by = 4

    def get_queryset(self):
        self.group = get_object_or_404(Group, pk = self.kwargs.get('pk'))
        queryset = self.group.post_set.order_by('-created')

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
# class GroupCategoryAutoComplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated():
#             return GroupCategory.objects.none()
#         qs = GroupCategory.objects.all()
#
#         if self.q:
#             qs = qs.filter(title__istartswith=self.q)
#         return qs

class GroupCategoryAdd(LoginRequiredMixin, CreateView):
    model = GroupCategory
    fields = ['name']
    template_name = 'application/group_category_form.html'

    def get_success_url(self):
        return reverse('application:group-add')

class GroupCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name ='application/group_add_form.html'
    # fields = ['name', 'description', 'category', 'is_favorite']

    def form_valid(self, form):
        print("valid function")
        instance = form.save(commit=False)
        instance.added_by = self.request.user
        instance.save()
        messages.success(self.request, "Group Successfully Created!")
        super(GroupCreate, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('invalid form')
        return HttpResponse("INVALID FORM")

    def get_success_url(self):
        return reverse('application:home')

class GroupUpdate(SuccessMessageMixin,UserAuthorMixin, UpdateView):
    model = Group
    template_name ='application/group_add_form.html'
    fields = ['name', 'category', 'description', 'is_favorite']
    success_message = "Group was Updated with success!"

    def form_valid(self, form):
        self.success_url = reverse_lazy('application:home')
        return super(GroupUpdate, self).form_valid(form)



class GroupDelete(UserAuthorMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('application:home')  # this is the path where the user will be redirected after he delete a group

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Group was deleted!")
        return super(GroupDelete, self).delete(request, *args, **kwargs)

def GroupFollow(request):
    user = request.user
    group_id= None
    if request.method =="GET":
        group_id= request.GET["group_pk"]
    followers = 0
    if group_id:
        group = Group.objects.get(id = int(group_id))
        print(group,group_id,user)
        # follow_users = group.follow.all()
        # print(follow_users)
        if group:
            if user in group.follow.all():
                group.follow.remove(user)
                followers = group.followers - 1
                print('scade')
                print(followers)
            else:
                group.follow.add(user)
                followers = group.followers + 1
                print('adauga')
                print(followers)
            follower_users = group.follow.all()
            print(follower_users)
        group.followers=followers
        group.save()
        print(followers)
    return HttpResponse(followers)

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


class PostCreate(SuccessMessageMixin, CreateView):
    model = Post
    fields = ['name','group_post', 'description', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.posted_by = self.request.user
        instance.save()
        messages.success(self.request, "You successfully added a new Post!")
        return super(PostCreate, self).form_valid(form)
        # return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

class PostUpdate(SuccessMessageMixin, UserAuthorMixinPost, UpdateView):
    model = Post
    fields = ['name','group_post', 'description']
    success_message = "Post was updated!"

    def form_valid(self, form):
        return super(PostUpdate, self).form_valid(form)

    def get_success_url(self): # this is done to redirect the user for the last page where he came from, keep attention to mention the id, ok of the page element
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

class PostDelete(SuccessMessageMixin, UserAuthorMixinPost, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('application:group_detail', kwargs={"pk": self.kwargs.get('group_pk', None)})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post Was Deleted!")
        return super(PostDelete, self).delete(request, *args, **kwargs)


class CommentView(ListView):
    model = Comment


class CommentCreate(SuccessMessageMixin, CreateView):
    model= Comment
    fields = ['description', 'comment_post', 'is_active', 'is_favorite', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.added_by = self.request.user
        instance.save()
        messages.success(self.request, "You added a comment!")
        return super(CommentCreate, self).form_valid(form)
        # return HttpResponseRedirect(instance.get_absolute_url())

class CommentUpdate(SuccessMessageMixin, UserAuthorMixin, UpdateView):
    model = Comment
    fields = ['description', 'comment_post', 'is_active', 'is_favorite', 'image']
    success_message = "Comment was updated!"
    def form_valid(self, form):
        return super(CommentUpdate, self).form_valid(form)

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

class CommentDelete(SuccessMessageMixin, UserAuthorMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        group=self.object.comment_post.group_post.pk
        return reverse('application:post_detail', kwargs={"group_pk":group, "pk" : self.kwargs.get('post_pk'),})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "You deleted the comment:(")
        return super(CommentDelete, self).delete(request, *args, **kwargs)
