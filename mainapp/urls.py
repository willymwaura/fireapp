from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('report_fire', views.report_fire, name='report_fire'),
    path('login_page', views.login_page, name='login_page'),
    path('adminpage',views.official_login,name='adminpage'),
    path('confirm_fire/<int:case_id>/', views.confirm_fire, name='confirm_fire'),
    path('cancel_fire/<int:case_id>/', views.cancel_fire, name='cancel_fire'),
    path('heatmap', views.heatmap, name='heatmap'),
    path('preventitive', views.preventitive, name='preventitive'),
   

]
