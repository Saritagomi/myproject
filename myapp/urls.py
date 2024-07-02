from django.urls import path
from . import views
urlpatterns = [ 
    path('login/', views.login_view, name = 'login'),
    # path('forgot-password/', views.forgot_p    assword_view, name = 'forgot_password'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),

    
]
