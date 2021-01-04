from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core import views as user_views
from core import views

urlpatterns = [
    url(r'^$', views.index, name='core/home'),
    url(r'^contact/$', views.contact, name='core/contact'),
    url(r'^all_profiles/$', views.get_all_profiles, name='core/profiles_table'),
    path('', user_views.feed, name='home'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('welcome/', user_views.welcome, name="welcome"),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', user_views.UserFormView.as_view(template_name='core/registration_form.html'), name='register'),
    url(r'^profile/(?P<username>\w+)/$', user_views.profile, name='profile'),
    url(r'^follow_elderly/(?P<username>\w+)/$', user_views.follow_elderly, name="follow_elderly"),
    url(r'^unfollow_elderly/(?P<username>\w+)/$', user_views.unfollow_elderly, name="unfollow_elderly"),
    url(r'^create_post/(?P<username>\w+)/$', user_views.create_post, name="create_post"),
    url(r'^create_comment/(?P<username>\w+)/(?P<post_id>\d+)/$', user_views.create_comment, name="create_comment"),
    path('feed/', user_views.feed, name="feed"),
    # url(r'^urgent_request/$', views.urgent_request, name='core/urgent_request'),
    url('feedback/', views.feedback, name='core/feedback'),
    url(r'^blog/$', views.test_redirect, name='test_redirect')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
