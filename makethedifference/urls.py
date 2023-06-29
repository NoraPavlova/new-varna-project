from django.urls import path

from makethedifference import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('login/', views.login_page, name='login-page'),
    path('logout/', views.logout_user, name='logout-page'),
    path('register/', views.register_page, name='register-page'),

    path('cause/<str:pk>/', views.cause_page, name='cause'),
    path('all-causes/', views.all_causes, name='all-causes'),
    path('all-events/', views.all_events, name='all-events'),
    path('follow-cause-confirmation/<str:pk>/', views.follow_cause_confirmation, name='follow-cause-conf'),
    path('register-event-confirmation/<str:pk>/', views.register_event_confirmation, name='register-event-conf'),

    path('user-profile/<str:pk>/', views.user_profile_page, name='user-profile-page'),
    path('user-account/', views.user_account_page, name='user-account'),
    path('edit_account/', views.edit_account, name='edit-account'),
    path('delete_account/', views.delete_account, name='delete-account'),
    path('change-password/', views.change_password, name='change-password'),

    path('create-event/<str:pk>/', views.create_event, name='create-event'),
    path('update-event/<str:pk>/', views.update_event, name='update-event'),
    path('event-details/<str:pk>/', views.event_details, name='event-details'),

    path('suggest-cause', views.suggest_cause, name='suggest-cause'),
    path('about', views.about, name='about'),
    path('event-details/<str:pk>/comment/', views.PostCommentView.as_view(), name='post-comment'),
    path('search/', views.search_bar, name='search'),
    path('like-cause/<str:pk>/', views.like_cause, name='like-cause'),
    path('like-event/<str:pk>/', views.like_event, name='like-event'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_pass/password_reset_form.html'),
         name='reset_password'),
    path('reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_pass/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_pass/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass/password_reset_complete.html'),
         name='password_reset_complete'),
]