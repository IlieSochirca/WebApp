from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.conf.urls.static import static
from application import views

app_name='application'

urlpatterns = [
    url(r'^$', views.start_page, name="startapp"),
    url(r'^home/', login_required(views.HomeView.as_view()), name="home"),
    # url(r'^search/$', views.HomeView.as_view(), name='group_search_list_view'),
    url(r'^profile/$', views.view_profile, name="profile"),
    url(r'^profile/edit/$', views.edit_profile, name="profile-edit"),
    url(r'^register/', views.RegitrationView.as_view(), name="register"),

#     reset password urls
url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ), name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'
        ), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),

#   change password urls for logged users

    url(r'^profile/settings/password/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),
    url(r'^profile/settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'),

    #The rest of the URLS for Groups and Posts Pages
    url(r'^group/(?P<pk>[0-9]+)/$', login_required(views.PostGroupDetailView.as_view()), name="group_detail"),
    # url(r'^searching/post/$', views.PostGroupDetailView.as_view(), name='post_search_list_view'),
    url(r'^group/add/$', views.GroupCreate.as_view(), name="group-add"),
    url(r'^group/(?P<pk>[0-9]+)/edit/$', views.GroupUpdate.as_view(), name="group-edit"),  # this way we tell django to capture the value of regex into an argument name pk
    url(r'^group/(?P<pk>[0-9]+)/delete/$', views.GroupDelete.as_view(), name="group-delete"),
    url(r'^group/(?P<group_pk>[0-9]+)/post/(?P<pk>[0-9]+)/$', login_required(views.PostDetail.as_view()), name="post_detail"),
    url(r'^group/(?P<group_pk>[0-9]+)/post/add/$', views.PostCreate.as_view(), name="post-add"),
    url(r'^group/(?P<group_pk>[0-9]+)/post/(?P<pk>[0-9]+)/edit/$', views.PostUpdate.as_view(), name="post-edit"),
    url(r'^group/(?P<group_pk>[0-9]+)/post/(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name="post-delete"),
    url(r'^posts/(?P<post_pk>[0-9]+)/comments/all/$', views.CommentView.as_view(), name="comment-view"),
    url(r'^posts/(?P<post_pk>[0-9]+)/comment/add/$', views.CommentCreate.as_view(), name="comment-add"),
    url(r'^posts/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/edit/$', views.CommentUpdate.as_view(), name="comment-edit"),
    url(r'^posts/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/delete/$', views.CommentDelete.as_view(), name="comment-delete"),
    url(r'^post-like/', views.PostLike, name="post-like"),
    url(r'^comment-like/', views.CommentLike, name="comment-like"),



]

