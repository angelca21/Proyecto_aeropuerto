from django.urls import path
from .views import home_view, login_view, register_view, index_view, home2_view, reserve_view, succesfully_view, change_language_view,logout_view, pasajeros_view, form_pasajeros


urlpatterns = [
    path('', index_view, name='index'),
    path('home/', home_view, name='home'),
    path('home2/', home2_view, name='home2'),
    path('reserve/', reserve_view, name='reserve'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('succesfully/', succesfully_view, name='succesfully'),
    path('change-language/', change_language_view, name='change_language'),
    path('logout/', logout_view, name='logout'),
    path('form-pasajeros/', form_pasajeros, name='form_pasajeros'),
    path('pasajeros/', pasajeros_view, name='pasajeros_view'),
]