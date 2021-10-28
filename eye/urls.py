from django.urls import path
from eye import views

urlpatterns = [
    path('eye/', views.main),
    path('report/', views.report),
    path('report/session', views.report_session),
    path('report/category', views.report_category),
    path('report/time', views.report_time),
]

