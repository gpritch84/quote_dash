from django.urls import path
from . import views

urlpatterns = [ 
    path('', (views.index)),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('user/<int:id_from_route>', views.user),
    path('add_quote', views.add_quote),
    path('edit_account/<int:id_from_route>', views.edit_account),
    path('update_user/<int:id_from_route>', views.update_user),
    path('delete_quote/<int:id_from_route>', views.delete_quote),
    path('like/<int:quote_id>/<int:user_id>', views.like),
]