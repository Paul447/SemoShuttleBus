from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('shuttle-data/', views.shuttle_data, name='shuttle_data'),
    path('last-7-days/', views.last_7_days_data_view, name='last_7_days_data'),
    path('filtered-data/', views.filtered_shuttle_data_view, name='filtered_shuttle_data'),
    path('demands_by_stop/', views.demands_by_stop, name='demands_by_stop'),
    path('demands_by_hour/', views.demands_by_hour, name='demands_by_hour'),
]
