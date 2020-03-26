from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('to_register', views.takes_to_register_page),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('users/new', views.redirects_to_add_user_page),
    path('register/new', views.new_user),
    path('users/update/<int:user_id>', views.update_user_page),
    path('users/<int:user_id>/update_info', views.update_info),
    path('users/<int:user_id>/update_password', views.update_password),
    path('users/show/<int:user_id>', views.user_profile),
    path('users/remove/<int:user_id>', views.remove_user),
    path('users/show/<int:user_id>/post', views.post_text),
    path('users/show/<int:user_id>/<int:message_id>/comment', views.comment),
    path('users/<int:user_id>/update_description', views.update_description),
    path('users/show/<int:user_id>/<int:comment_id>/delete_comment', views.delete_comment),
    path('users/show/<int:user_id>/<int:message_id>/delete_message', views.delete_message),
    path('users/search_results', views.results_page),
    path('users/result_page', views.results_age),
    path('users/likes/<int:user_id>', views.add_to_favorites),
    path('users/disliked/<int:user_id>', views.remove_from_favorites)
]
