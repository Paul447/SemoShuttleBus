from django.shortcuts import render
from .models import Shuttle,BlueShuttle
from django.shortcuts import render
from .models import BlueShuttle  # Import your BlueShuttle model
from django.db.models import Sum
from datetime import date
import pandas as pd
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast


def demands_by_hour(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Get the current date and calculate the date for 1 year ago
    one_year_ago = datetime.now() - timedelta(days=365)
    
    # Filter data for the last year and between 6:00 AM and 10:00 PM
    filtered_data = BlueShuttle.objects.filter(
        time__gte=one_year_ago,
        time__hour__gte=6,  # Starting from 6:00 AM
        time__hour__lt=22  # Up to 10:00 PM
    )
    
    # Aggregate boarding and alighting data by hour and stop
    hourly_data = filtered_data.values('stop_name', 'time__hour').annotate(
        total_boarding=Sum('number_of_passangers_in'),
        total_alighting=Sum('number_of_passangers_out')
    ).order_by('time__hour', 'stop_name')

    # Prepare data for visualization
    hours = [f"{hour}:00" for hour in range(6, 22)]  # 6:00 AM to 10:00 PM
    stops = list(set([data['stop_name'] for data in hourly_data]))  # List of unique stop names

    # Initialize dictionaries for storing data for each stop and hour
    boarding_counts = {stop: [0] * len(hours) for stop in stops}
    alighting_counts = {stop: [0] * len(hours) for stop in stops}

    # Populate the data for each stop and hour
    for data in hourly_data:
        hour_index = data['time__hour'] - 6  # Adjust hour to start from 0 (6:00 AM)
        boarding_counts[data['stop_name']][hour_index] = data['total_boarding'] or 0
        alighting_counts[data['stop_name']][hour_index] = data['total_alighting'] or 0

    # Pass the data to the template
    context = {
        'hours': hours,
        'boarding_counts': boarding_counts,
        'alighting_counts': alighting_counts,
    }

    return render(request, 'demands_by_hour.html', context)


stops = [
    "Towers", "Grauel", "UC/Kent/Academic", "Vandiver/Merick", "Rear Kent", "Pacific/Grauel",
    "Catapult", "Mass Media", "Spanish/Independence", "River Campus", "Band Annex",
    "River Campus Arts Building", "Vandiver/Merick", "Bookstore", "Memorial/Parker/Academic",
    "Scully/Parker", "Dempster", "Polytech/Laferla", "MMTF", "International Village"
]

# Map of stop names to their index for sorting
stop_index_map = {stop: index for index, stop in enumerate(stops)}

@login_required
def last_7_days_data_view(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")
    # Define the desired stop order with index mapping for efficient sorting
    stops = [
        "Towers", "Grauel", "UC/Kent/Academic", "Vandiver/Merick", "Rear Kent", "Pacific/Grauel", 
        "Catapult", "Mass Media", "Spanish/Independence", "River Campus", "Band Annex", 
        "River Campus Arts Building", "Vandiver/Merick", "Bookstore", "Memorial/Parker/Academic", 
        "Scully/Parker", "Dempster", "Polytech/Laferla", "MMTF", "International Village"
    ]
    stop_index_map = {stop: index for index, stop in enumerate(stops)}

    # Calculate the start date for the last 7 days
    last_7_days_start = date.today() - timedelta(days=7)

    # Fetch and aggregate data from the database
    last_7_days_data = (
        BlueShuttle.objects.filter(date__gte=last_7_days_start)
        .values('stop_name')
        .annotate(total_passengers_in=Sum('number_of_passangers_in'))
    )

    # Sort the data based on the desired stop order
    sorted_data = sorted(
        last_7_days_data, 
        key=lambda x: stop_index_map.get(x['stop_name'], len(stops))
    )

    # Calculate the total passengers directly in the database
    last_7_days_total = last_7_days_data.aggregate(total=Sum('total_passengers_in'))['total'] or 0

    # Render the template
    return render(
        request,
        'last-7-days.html',
        {
            'last_7_days_data': sorted_data,
            'last_7_days_total': last_7_days_total,
            'stops': stops,  # For reference or additional display
        }
    )



@login_required
def filtered_shuttle_data_view(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")
    # Get filter parameters from the request
    specific_date = request.GET.get('date')
    specific_stop = request.GET.get('stop')
    custom_start_date = request.GET.get('start_date')
    custom_end_date = request.GET.get('end_date')

    # Build filter conditions dynamically based on the parameters
    filter_conditions = {}

    # Handle specific date filter
    if specific_date and specific_date != 'None':  # Avoid 'None' string value
        try:
            # Ensure the date is in valid format
            datetime.strptime(specific_date, '%Y-%m-%d')
            filter_conditions['date'] = specific_date
        except ValueError:
            # Handle invalid date format
            pass  # You can handle this with an error message if needed

    # Handle specific stop filter
    if specific_stop and specific_stop != 'None':  # Avoid 'None' string value
        filter_conditions['stop_name'] = specific_stop
    
    # Handle custom date range filter
    if custom_start_date and custom_end_date:
        try:
            # Ensure the dates are in valid format
            datetime.strptime(custom_start_date, '%Y-%m-%d')
            datetime.strptime(custom_end_date, '%Y-%m-%d')
            filter_conditions['date__range'] = [custom_start_date, custom_end_date]
        except ValueError:
            pass  # Handle invalid date formats if needed

    # Query BlueShuttle model with the filter conditions
    stop_data = (
        BlueShuttle.objects.filter(**filter_conditions)
        .values('date', 'stop_name')
        .annotate(total_passengers_in=Sum('number_of_passangers_in'))
    )

    # Sort stop data using the pre-mapped stop index
    stop_data = sorted(stop_data, key=lambda x: stop_index_map.get(x['stop_name'], len(stops)))

    # Create paginator object to paginate the data (10 items per page)
    paginator = Paginator(stop_data, 10)

    # Get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate the total number of passengers
    total_passengers = sum(entry['total_passengers_in'] for entry in stop_data)

    # Render the template with the paginated data
    return render(
        request,
        'filtered-data.html',  # Template name
        {
            'page_obj': page_obj,  # The paginated object
            'total_passengers': total_passengers,  # The total passengers count
            'stops': stops,  # List of stops for the dropdown filter
            'selected_date': specific_date,  # Selected date filter
            'selected_stop': specific_stop,  # Selected stop filter
            'custom_start_date': custom_start_date,  # Custom start date filter
            'custom_end_date': custom_end_date,  # Custom end date filter
        }
    )



@login_required
def shuttle_data(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")
    # Get the current year
    current_year = date.today().year
    current_month = date.today().month

    # Aggregate the total number of passengers by month for the current year
    monthly_data = BlueShuttle.objects.filter(date__year=current_year) \
        .values('date__month') \
        .annotate(total_passengers_in=Sum('number_of_passangers_in')) \
        .order_by('date__month')

    # Prepare an array for months and the sum of passengers
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    passengers_per_month = [0] * 12  # Initialize all months with 0

    # Fill the data for months that have entries
    for data in monthly_data:
        month_index = data['date__month'] - 1
        passengers_per_month[month_index] = data['total_passengers_in']

    # Get the data up to the current month
    passengers_per_month = passengers_per_month[:current_month]  # Trim data for months not reached yet

    # Pass the data to the template
    context = {
        'months': months[:current_month],
        'passengers_per_month': passengers_per_month,
        'current_year': current_year,
    }

    return render(request, 'chart.html', context)



def demands_by_stop(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Aggregate boarding and alighting data by stop
    stop_data = BlueShuttle.objects.values('stop_name').annotate(
        total_boarding=Sum('number_of_passangers_in'),
        total_alighting=Sum('number_of_passangers_out')
    ).order_by('stop_name')

    # Prepare data for visualization
    stops = [data['stop_name'] for data in stop_data]
    boarding_counts = [data['total_boarding'] for data in stop_data]
    alighting_counts = [data['total_alighting'] for data in stop_data]

    # Pass the data to the template
    context = {
        'stops': stops,
        'boarding_counts': boarding_counts,
        'alighting_counts': alighting_counts,
    }

    return stops , boarding_counts , alighting_counts

@login_required
def index(request):
    # Get the current year
    stops , boarding_counts , alighting_counts = demands_by_stop(request)
    
    if not request.user.is_superuser:
        # If the user is not a superuser, return a Forbidden response
        return HttpResponseForbidden("You do not have permission to view this page.")
    current_year = date.today().year

    # List of stop names in the correct order
    stop_order = [
        "Towers", "Grauel", "UC/Kent/Academic", "Vandiver/Merick", "Rear Kent", "Pacific/Grauel", 
        "Catapult", "Mass Media", "Spanish/Independence", "River Campus", "Band Annex", 
        "River Campus Arts Building", "Vandiver/Merick", "Bookstore", "Memorial/Parker/Academic", 
        "Scully/Parker", "Dempster", "Polytech/Laferla", "MMTF", "International Village"
    ]
    
    # Aggregate the total number of passengers by stop for the current year
    stop_data = BlueShuttle.objects.filter(date__year=current_year) \
        .values('stop_name') \
        .annotate(
            total_passengers_in=Sum('number_of_passangers_in'),
            total_passengers_out=Sum('number_of_passangers_out')
        ) \
        .order_by('stop_name')

    # Create dictionaries for easy lookup
    stop_dict = {data['stop_name']: data for data in stop_data}

    # Prepare arrays to hold stop names and corresponding data
    stop_names = []
    passengers_in = []
    passengers_out = []

    # Ensure stops are added in the correct order
    for stop in stop_order:
        if stop in stop_dict:
            stop_names.append(stop)
            passengers_in.append(stop_dict[stop]['total_passengers_in'] or 0)
            passengers_out.append(stop_dict[stop]['total_passengers_out'] or 0)

    context = {
        'stop_names': stop_names,
        'passengers_in': passengers_in,
        'passengers_out': passengers_out,
        'current_year': current_year,
        'stops' : stops,
        'boarding_counts' : boarding_counts,
        'alighting_counts' : alighting_counts

    }

    return render(request, 'index.html', context)
