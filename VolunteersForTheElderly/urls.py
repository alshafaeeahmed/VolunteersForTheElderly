from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core import views
from core import views as user_views

urlpatterns = [
    url(r'^$', views.index, name='core/home'),
    path('homepage/', user_views.index, name='home'),
    path('Thank/', views.Thanks, name='core/Thank.html'),
    url(r'^Contact_us/$', views.contact_us, name='core/Contact_us'),
    url(r'^updates/$', views.PageUpdate, name='core/updates'),
    url(r'^about/$', views.Site_info, name='core/site_info'),
    url(r'^all_profiles/$', views.get_all_profiles, name='core/profiles_table'),
    url(r'^all_UrgentRequests/$', views.get_UrgentRequests, name='core/all_urgent_request'),
    url(r'^all_contact_us/$', views.get_contact_us, name='core/all_contact_us.html'),
    url(r'^available_profiles/$', views.get_all_available_volunteers, name='core/available_profiles.html'),
    url(r'^profiles_gender/$', views.get_all_volunteers_gender, name='core/profiles_gender.html'),
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
    url(r'^urgent_request/$', views.Urgent_Request, name='core/urgent_request'),
    path('blogpost-like/<int:pk>', views.BlogPostLike, name="blogpost_like"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
