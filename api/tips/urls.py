from django.urls import path

from . import views

urlpatterns = [
    path('', views.Tips.as_view(), name='tips'),

    # path('create-tip/', views.CreateTip.as_view(), name='create_tip'),
    
    path('tipsters/', views.Tipsters.as_view(), name='tipsters')
]
