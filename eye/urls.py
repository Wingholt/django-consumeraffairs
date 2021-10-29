from django.urls import path
from eye import views

urlpatterns = [
    path('eye/', views.main),
    path('report/all', views.report_all_activities),
    path('report/session/count', views.session_count),
    path('report/category/count', views.category_count),
    path('report/name/count', views.name_count),
    path('report/', views.report),
]

