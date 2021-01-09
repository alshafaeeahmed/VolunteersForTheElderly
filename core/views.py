from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect  # sss
from django.shortcuts import get_object_or_404  # ss
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from .forms import UserForm, UpdateUserForm, UpdateProfileForm, CreatePost, CreateComment, \
    PageUpdate, Contact_UsForm, UrgentRequestForm
from .models import User, Profile, UrgentRequest, Following, Follower


def get_all_volunteers():
    result = list()
    users_list = Profile.objects.all()
    for user_item in users_list:
        if getattr(user_item, "is_volunteer"):
            result.append(user_item)
    return result


# return the Urgent Requests from the data base
def all_UrgentRequests():
    result = list()
    users_list = UrgentRequest.objects.all()
    for user_item in users_list:
        result.append(user_item)
    return result


def get_UrgentRequests(request):
    context = {}
    context.update({'all_UrgentRequests': all_UrgentRequests()})
    return render(request, 'core/all_urgent_request.html', context)


def all_contact_us():
    result = list()
    users_list = contact_us.objects.all()
    for user_item in users_list:
        result.append(user_item)
    return result


def get_contact_us(request):
    context = {}
    context.update({'all_contact_us': all_contact_us()})
    return render(request, 'core/all_contact_us.html', context)


# Return all volunteers who are available in the system
def get_all_available_volunteers(request):
    context = {}
    context.update({'all_volunteers': get_all_volunteers()})
    return render(request, 'core/available_profiles.html', context)


# Return all volunteers genders
def get_all_volunteers_gender(request):
    context = {}
    context.update({'all_volunteers': get_all_volunteers()})
    return render(request, 'core/profiles_gender.html', context)


def get_all_elderly():
    result = list()
    users_list = Profile.objects.all()
    for user_item in users_list:
        if not getattr(user_item, "is_volunteer"):
            result.append(user_item)
    return result


def index(request):
    return render(request, 'core/index.html')


def Thanks(request):
    return render(request, 'core/Thank.html')


@login_required
def profile(request, username):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            target_user = User.objects.get(username=username)
            target_profile = Profile.objects.get(user=target_user)
            if not getattr(target_profile, 'is_active'):
                target_user.delete()
                target_profile.delete()
                return HttpResponseRedirect('/')
            url = reverse('profile', kwargs={'username': username})
            return redirect(url)

    else:
        if username == request.user.username or 'admin' == request.user.username:
            u_form = UpdateUserForm(instance=request.user)
            p_form = UpdateProfileForm(instance=request.user.profile)
            post_form = CreatePost()
            person = User.objects.get(username=username)

            context = {
                'u_form': u_form,
                'p_form': p_form,
                'post_form': post_form,
                'person': person,

            }
        else:
            person = User.objects.get(username=username)
            already_a_follower = 0
            for followers in person.follower_set.all():
                if followers.follower_user == request.user.username:
                    already_a_follower = 1
                    break;

            if already_a_follower == 1:
                context = {
                    'person': person,

                }
            else:
                context = {
                    'person': person,
                    'f': 1,

                }
        comment_form = CreateComment()
        context.update({'comment_form': comment_form})
        context.update({'all_volunteers': get_all_volunteers()})
        context.update({'all_elderly': get_all_elderly()})
        context.update({'available_volunteers': get_all_available_volunteers(request)})
        context.update({'volunteers_gender': get_all_available_volunteers(request)})
        context.update({'all_UrgentRequests': all_UrgentRequests()})
        context.update({'get_all_UrgentRequests': get_UrgentRequests(request)})
        context.update({'my_followers': get_user_following(person)})
        context.update({'my_following': get_user_follower(person)})
        context.update({'all_contact_us': all_contact_us()})
        context.update({'get_contact_us': get_contact_us(request)})
    return render(request, 'core/profile.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            Profile(user=user).save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Account created for {username}!')
                    return HttpResponseRedirect('/profile/' + username + '/')

        return render(request, self.template_name, {'form': form})


def follow_elderly(request, username):
    if request.user.username != username:
        if request.method == 'POST':
            disciple = User.objects.get(username=request.user.username)
            leader = User.objects.get(username=username)
            leader.follower_set.create(follower_user=disciple)
            disciple.following_set.create(following_user=leader)
            url = reverse('profile', kwargs={'username': username})
            return redirect(url)


def unfollow_elderly(request, username):
    if request.method == 'POST':
        disciple = User.objects.get(username=request.user.username)
        leader = User.objects.get(username=username)
        leader.follower_set.get(follower_user=disciple).delete()
        disciple.following_set.get(following_user=leader).delete()
        url = reverse('profile', kwargs={'username': username})
        return redirect(url)


def welcome(request):
    url = reverse('profile', kwargs={'username': request.user.username})
    return redirect(url)


def create_post(request, username):
    if request.method == 'POST':
        post_form = CreatePost(request.POST, request.FILES)
        if post_form.is_valid():
            post_text = post_form.cleaned_data['post_text']
            post_picture = request.FILES.get('post_picture')
            request.user.post_set.create(post_text=post_text, post_picture=post_picture)
            messages.success(request, f'You have successfully posted!')
    url = reverse('profile', kwargs={'username': username})
    return redirect(url)


# like in the comment
def BlogPostLike(request, pk):
    post = get_object_or_404(create_post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('core/profile.html', args=[str(pk)]))


def create_comment(request, username, post_id):
    if request.method == 'POST':
        comment_form = CreateComment(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            user = User.objects.get(username=username)
            post = user.post_set.get(pk=post_id)
            post.comment_set.create(user=request.user, comment_text=comment_text)
            messages.success(request, f'Your Comment has been posted')
    url = reverse('profile', kwargs={'username': username})
    return redirect(url)


def PageUpdate(request):
    form_class = PageUpdate

    return render(request, 'core/updates.html', {
        'form': form_class,
    })


def Site_info(request):
    form_class = Site_info
    return render(request, 'core/site_info.html', {
        'form': form_class,
    })


def get_all_profiles(request):
    context = {}
    context.update({'all_volunteers': get_all_volunteers()})
    context.update({'all_elderly': get_all_elderly()})
    return render(request, 'core/profiles_table.html', context)


def Urgent_Request(request):
    if request.method == 'POST':
        f = UrgentRequestForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'קיים בקשה דחופה חדשה')
            return redirect('core/Thank.html')
    else:
        f = UrgentRequestForm()
    return render(request, 'core/urgent_request.html', {'form': f})


def contact_us(request):
    if request.method == 'POST':
        f = Contact_UsForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'קיים הודעה חדשה ביצירת קשר')
            return redirect('core/Thank.html')
    else:
        f = Contact_UsForm()
    return render(request, 'core/contact_us.html', {'form': f})


def get_user_following(target_user):
    result = list()
    for following in Following.objects.filter(user=target_user):
        try:
            result.append(getattr(following, 'following_user'))
        except:
            pass
    return result


def get_user_follower(target_user):
    result = list()
    for follower in Follower.objects.filter(user=target_user):
        try:
            follower_user = User.objects.get(username=getattr(follower, 'follower_user'))
            if getattr(Profile.objects.get(user=follower_user), 'is_volunteer'):
                result.append(getattr(follower, 'follower_user'))
        except:
            pass
    return result
