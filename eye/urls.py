from django.urls import path
from eye import views

urlpatterns = [
    path('eye/', views.eye),
    path('report/', views.report),
    path('report/all', views.report_all_activities),
    path('count/session', views.session_count),
    path('count/category', views.category_count),
    path('count/name', views.name_count),

]

