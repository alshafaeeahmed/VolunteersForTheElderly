from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from .forms import UserForm, UpdateUserForm, UpdateProfileForm, CreatePost, CreateComment, ContactForm, FeedbackForm
from .models import User, Post, Profile
from django.shortcuts import get_object_or_404  # ss
from django.http import HttpResponseRedirect  # sss


def get_all_volunteers():
    result = list()
    users_list = Profile.objects.all()
    for user_item in users_list:
        if getattr(user_item, "is_volunteer"):
            result.append(user_item)
    return result


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
        context.update({'volunteers_gender': get_all_volunteers_gender(request)})
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


def feed(request):
    post_all = Post.objects.order_by('created_at').reverse()
    comment_form = CreateComment()
    context = {
        'post_all': post_all,
        'comment_form': comment_form,
    }
    return render(request, 'core/index.html', context)


# build the contact function
def contact(request):
    form_class = ContactForm

    return render(request, 'core/contact.html', {
        'form': form_class,
    })


def get_all_profiles(request):
    context = {}
    context.update({'all_volunteers': get_all_volunteers()})
    context.update({'all_elderly': get_all_elderly()})
    return render(request, 'core/profiles_table.html', context)


# print(User.objects)
# print(User.objects.get(username="ahmed"))
def feedback(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('feedback')
    else:
        f = FeedbackForm()
    return render(request, 'core/feedback.html', {'form': f})


def UrgentRequest(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'הבקשה שלך נשלך למנהל האתר !.')
            return redirect('UrgentRequest')
    else:
        f = FeedbackForm()
    return render(request, 'core/urgent_request.html', {'form': f})


class Category(object):
    pass


def test_redirect():
    c = Category.objects.get(name='python')
    return redirect(c)
