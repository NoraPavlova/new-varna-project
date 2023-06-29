from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


from makethedifference.forms import EventForm, CustomUserCreationForm, UserForm, UserDeleteForm, CommentForm
from makethedifference.models import User, Cause, Event, Comment

from .filters import AllEventsFilter, AllCausesFilter


def login_page(request):
    page = 'login'
    if request.method == "POST":
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('home-page')
        else:
            messages.error(request, 'Email or password is not valid')
            return redirect('login-page')

    context = {
        'page': page,
    }
    return render(request, 'login_register.html', context)


def register_page(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'User account was created')
            return redirect('home-page')
        else:
            messages.error(request, 'An error has occurred during registration')

    page = 'register'
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login-page')


def home_page(request):
    # limit = request.GET.get('limit')
    #
    # if limit is None:
    #     limit = 20

    users = User.objects.all().order_by('-date_joined')[0:5]
    users_count = User.objects.all().count()
    causes = Cause.objects.all().order_by('-created')[0:3]
    events = Event.objects.all().order_by('-created')[0:4]
    causes_count = Cause.objects.all().count()
    events_count = Event.objects.all().count()

    context = {
        'users': users,
        'users_count': users_count,
        'causes': causes,
        'causes_count': causes_count,
        'events': events,
        'events_count': events_count,
    }
    return render(request, 'home.html', context, )


def user_profile_page(request, pk):
    user = User.objects.get(id=pk)
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
def user_account_page(request):
    user = request.user

    context = {'user': user}
    return render(request, 'user_account.html', context)


@login_required(login_url='/login')
def edit_account(request):
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'edit_account.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('home-page')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'delete_account.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST['oldpassword']
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if request.user.check_password(oldpassword):
            if password1 == password2:
                new_pass = make_password(password1)
                request.user.password = new_pass
                request.user.save()
                messages.success(request, 'You have reset your password')
                return redirect('user-account')
            else:
                messages.error(request, "Passwords don't match!")
        else:
            messages.error(request, 'Wrong current password!')
    return render(request, 'account_password.html')


def cause_page(request, pk):
    cause = Cause.objects.get(id=pk)
    following = False
    submitted_event = False
    total_likes = cause.total_cause_likes()
    liked = False
    if cause.likes.filter(id=request.user.id).exists():
        liked = True

    if request.user.is_authenticated:
        following = request.user.causes.filter(id=cause.id).exists()
        submitted_event = Event.objects.filter(creator_id=request.user, cause=cause).exists()
    context = {'cause': cause,
               'following': following,
               'submitted_event': submitted_event,
               'cause_tags': cause.tags.all(),
               'total_likes': total_likes,
               'liked': liked,
               }
    return render(request, 'cause.html', context)


@login_required()
def follow_cause_confirmation(request, pk):
    template = render_to_string('email_templates/follow_cause_confirmation_email.html',
                                {'name': request.user.username})
    email = EmailMessage(
        'subject',  # change with desired subject
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()

    cause = Cause.objects.get(id=pk)

    if request.method == 'POST':
        if cause.followers.filter(id=request.user.id).exists():
            cause.followers.remove(request.user)
        else:
            cause.followers.add(request.user)
            return redirect('cause', pk=cause.id)
    context = {
        'cause': cause,
    }
    return render(request, 'follow_cause_confirmation.html', context)


@login_required()
def register_event_confirmation(request, pk):

    template = render_to_string('email_templates/register_event_confirmation.html',
                                {'name': request.user.username})
    email = EmailMessage(
        'subject',  # change with desired subject
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()

    event = Event.objects.get(id=pk)
    context = {
        'event': event
    }

    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event-details', pk=event.id)

    return render(request, 'register_event_confirmation.html', context)


@login_required()
def create_event(request, pk):
    cause = Cause.objects.get(id=pk)
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.cause = cause
            event.save()

            return redirect('user-account')

    context = {
        'cause': cause,
        'form': form,
    }

    return render(request, 'create_event_form.html', context)


@login_required()
def update_event(request, pk):
    event = Event.objects.get(id=pk)

    if request.user != event.creator:
        return HttpResponse("You can't be here!")

    cause = event.cause
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('user-account')
    context = {'form': form,
               'cause': cause,
               }
    return render(request, 'create_event_form.html', context)


def event_details(request, pk):
    event = Event.objects.get(id=pk)

    registered = False
    total_event_likes = event.total_event_likes()
    liked = False
    if event.likes.filter(id=request.user.id).exists():
        liked = True

    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()

    return render(request, 'event_details.html', {'event': event,
                                                  'registered': registered,
                                                  'event_tags': event.tag.all(),
                                                  'total_event_likes': total_event_likes,

                                                  })


def suggest_cause(request):
    return render(request, 'suggest_cause.html')


def about(request):
    return render(request, 'about_us.html')


class PostCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post_comment.html'

    def form_valid(self, form):
        form.instance.event_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.kwargs['pk']})


def all_causes(request):
    causes = Cause.objects.all().order_by('-created')
    causes_count = Cause.objects.all().count()
    page = request.GET.get('page')
    paginator = Paginator(causes, 3)
    all_causes_filter = AllCausesFilter(request.GET, queryset=causes)
    # causes = all_causes_filter.qs

    # def load_more(request):
    #     loaded_item = request.GET.get('loaded_item')
    #     loaded_item_int = int(offset)
    #     limit = 2
    #     causes_list = list(Cause.objects.values()[loaded_item_int:loaded_item_int + limit])
    #     data = {'causes': causes_list}
    #     return JsonResponse(data=data)

    try:
        causes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        causes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        causes = paginator.page(page)

    # pages = list(range(1, (paginator.num_pages + 1)))
    return render(request, 'all_causes.html', context={'causes': causes,
                                                       'paginator': paginator,
                                                       'causes_count': causes_count,
                                                       'all_causes_filter': all_causes_filter}
                                                       )


def all_events(request):
    events = Event.objects.all().order_by('-created')
    events_count = Event.objects.all().count()
    all_events_filter = AllEventsFilter(request.GET, queryset=events)
    events = all_events_filter.qs
    page = request.GET.get('page')
    paginator = Paginator(events, 3)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        events = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        events = paginator.page(page)

    # pages = list(range(1, (paginator.num_pages + 1)))
    return render(request, 'all_events.html', context={'events': events,
                                                       'all_events_filter': all_events_filter,
                                                       'paginator': paginator,
                                                       'events_count': events_count,
                                                       })


def search_bar(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        causes = Cause.objects.filter(title__contains=searched)
        events = Event.objects.filter(title__contains=searched)

        return render(request, 'search_bar.html', {'searched': searched, 'events': events, 'causes': causes})

    return render(request, 'search_bar.html')


def like_cause(request, pk):
    cause = get_object_or_404(Cause, id=request.POST.get('cause_like_id'))
    liked = False
    if cause.likes.filter(id=request.user.id).exists():
        cause.likes.remove(request.user)
        liked = False
    else:
        cause.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('cause', args=[str(pk)]))


def like_event(request, pk):
    event = get_object_or_404(Event, id=request.POST.get('event_like_id'))
    liked = False
    if event.likes.filter(id=request.user.id).exists():
        event.likes.remove(request.user)
        liked = False
    else:
        event.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('event-details', args=[str(pk)]))


def dashboard(request):
    return render(request, 'dashboard.html')


