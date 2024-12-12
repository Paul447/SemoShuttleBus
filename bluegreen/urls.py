from django.urls import path

from . import views
from . import green_views

urlpatterns = [
    path("", views.index, name="index"),
    path('shuttle-data/', views.shuttle_data, name='shuttle_data'),
    path('last-7-days/', views.last_7_days_data_view, name='last_7_days_data'),
    path('filtered-data/', views.filtered_shuttle_data_view, name='filtered_shuttle_data'),
    path('demands_by_stop/', views.demands_by_stop, name='demands_by_stop'),
    path('demands_by_hour/', views.demands_by_hour, name='demands_by_hour'),
    path('green/', green_views.index, name='green_index'),
    path('gyear/', green_views.greenyeardata, name='green_year_data'),
    path('ghour/', green_views.demands_by_hour_green, name='green_hour_data'),
    path('gsevendays/', green_views.last_7_days_data_view_green, name='green_last_7_days_data'),
    path('gfiltered/', green_views.filtered_shuttle_data_view_green, name='green_filtered_shuttle_data'),
    path('shuttleround/', views.calculate_and_plot_average_time, name='shuttle_round'),
]
