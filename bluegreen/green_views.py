from django.shortcuts import render
from .models import GreenShuttle
from django.db.models import Sum
from datetime import datetime, timedelta, date, time
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

# Create your views here.
# List of stops in a specific order
stops = [
    "Towers",
    "Grauel",
    "Houck/Alumni",
    "Vandiver/Merick",
    "UC/Kent/Academic",
    "Rear Kent",
    "Pacific",
    "Grauel",
    "Rear of Academic",
    "Memorial",
    "Scully/Parker",
    "Dempster",
    "LaFerla/Polytech",
    "MMTF",
    "DPS/Greek Village",
    "International Village" 
]

# Mapping stops to indices for sorting
stop_index_map = {stop: index for index, stop in enumerate(stops)}

# Function to get demands by hour
@login_required
def demands_by_hour_green(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    one_year_ago = datetime.now() - timedelta(days=365)

# Define the start and end times for each day (6:00 AM to 10:00 PM)
    start_time = time(6, 0)  # 6:00 AM
    end_time = time(22, 0)  # 10:00 PM

# Filter data based on the datetime range and time range
    filtered_data = GreenShuttle.objects.filter(
    date__gte=one_year_ago.date(),  # Filter by date from one year ago
    time__range=(start_time, end_time)  # Filter by time range
    )

    # Aggregate data by hour and stop for boarding and alighting
    hourly_data = filtered_data.values('stop_name', 'time__hour').annotate(
        total_boarding=Sum('number_of_passangers_in'),
        total_alighting=Sum('number_of_passangers_out')
    ).order_by('time__hour', 'stop_name')

    hours = [f"{hour}:00" for hour in range(6, 22)]  # 6:00 AM to 10:00 PM
    stops_list = list(set([data['stop_name'] for data in hourly_data]))  # List of unique stops

    # Initialize dictionaries for boarding and alighting counts per stop and hour
    boarding_counts = {stop: [0] * len(hours) for stop in stops_list}
    alighting_counts = {stop: [0] * len(hours) for stop in stops_list}
    stop_names = {stop: stop for stop in stops_list}  # Store stop names

    # Populate the dictionaries with the aggregated data
    for data in hourly_data:
        hour_index = data['time__hour'] - 6  # Adjust to start at 0 for 6:00 AM
        boarding_counts[data['stop_name']][hour_index] = data['total_boarding'] or 0
        alighting_counts[data['stop_name']][hour_index] = data['total_alighting'] or 0

    # Calculate highest and lowest counts per hour
    highest_boarding = {}
    lowest_boarding = {}
    highest_alighting = {}
    lowest_alighting = {}

    highest_boarding_stop = {}
    lowest_boarding_stop = {}
    highest_alighting_stop = {}
    lowest_alighting_stop = {}

    for hour_index in range(len(hours)):
        # Get boarding and alighting values for all stops at this hour
        boarding_values = [boarding_counts[stop][hour_index] for stop in stops_list]
        alighting_values = [alighting_counts[stop][hour_index] for stop in stops_list]

        # Calculate the highest and lowest boarding counts and their respective stop names
        highest_boarding[hours[hour_index]] = max(boarding_values)
        lowest_boarding[hours[hour_index]] = min(boarding_values)

        highest_boarding_stop[hours[hour_index]] = stops_list[boarding_values.index(max(boarding_values))]
        lowest_boarding_stop[hours[hour_index]] = stops_list[boarding_values.index(min(boarding_values))]

        # Calculate the highest and lowest alighting counts and their respective stop names
        highest_alighting[hours[hour_index]] = max(alighting_values)
        lowest_alighting[hours[hour_index]] = min(alighting_values)

        highest_alighting_stop[hours[hour_index]] = stops_list[alighting_values.index(max(alighting_values))]
        lowest_alighting_stop[hours[hour_index]] = stops_list[alighting_values.index(min(alighting_values))]

    # Prepare context data for rendering the template
    context = {
        'hours': hours,
        'boarding_counts': boarding_counts,
        'alighting_counts': alighting_counts,
        'highest_boarding': highest_boarding,
        'lowest_boarding': lowest_boarding,
        'highest_alighting': highest_alighting,
        'lowest_alighting': lowest_alighting,
        'highest_boarding_stop': highest_boarding_stop,
        'lowest_boarding_stop': lowest_boarding_stop,
        'highest_alighting_stop': highest_alighting_stop,
        'lowest_alighting_stop': lowest_alighting_stop,
    }

    return render(request, 'demands_by_hour.html', context)


@login_required
def demands_by_stop(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Aggregate boarding and alighting data by stop
    stop_data = GreenShuttle.objects.values('stop_name').annotate(
        total_boarding=Sum('number_of_passangers_in'),
        total_alighting=Sum('number_of_passangers_out')
    ).order_by('stop_name')

    # Prepare data for visualization
    stops = [data['stop_name'] for data in stop_data]
    boarding_counts = [data['total_boarding'] for data in stop_data]
    alighting_counts = [data['total_alighting'] for data in stop_data]

    # Render the demands by stop data to the template
    return stops, boarding_counts, alighting_counts

@login_required
def index(request):
    # Check if the user is a superuser before proceeding
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Get the current year
    current_year = date.today().year

    # Call the demands_by_stop function to get the required data
    stops, boarding_counts, alighting_counts = demands_by_stop(request)
    
    # List of stop names in the correct order
    stop_order = [
    "Towers",
    "Grauel",
    "Houck/Alumni",
    "Vandiver/Merick",
    "UC/Kent/Academic",
    "Rear Kent",
    "Pacific",
    "Grauel",
    "Rear of Academic",
    "Memorial",
    "Scully/Parker",
    "Dempster",
    "LaFerla/Polytech",
    "MMTF",
    "DPS/Greek Village",
    "International Village" 
    ]
 
    
    # Aggregate the total number of passengers by stop for the current year
    stop_data = GreenShuttle.objects.filter(date__year=current_year) \
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

    # Prepare the context to pass to the template
    context = {
        'stop_names': stop_names,
        'passengers_in': passengers_in,
        'passengers_out': passengers_out,
        'current_year': current_year,
        'stops': stops,
        'boarding_counts': boarding_counts,
        'alighting_counts': alighting_counts
    }
    return render(request, 'index.html', context)
@login_required
def greenyeardata(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Get the current year and month
    current_year = date.today().year
    current_month = date.today().month

    # Aggregate monthly data for the current year
    monthly_data = GreenShuttle.objects.filter(date__year=current_year).values('date__month').annotate(
        total_passengers_in=Sum('number_of_passangers_in')
    ).order_by('date__month')

    # Prepare the months and corresponding passenger data
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    passengers_per_month = [0] * 12

    # Populate data for the months that have entries
    for data in monthly_data:
        month_index = data['date__month'] - 1
        passengers_per_month[month_index] = data['total_passengers_in']

    # Trim data for months that haven't occurred yet
    passengers_per_month = passengers_per_month[:current_month]

    # Render the monthly data to the template
    return render(
        request,
        'chart.html',
        {
            'months': months[:current_month],
            'passengers_per_month': passengers_per_month,
            'current_year': current_year,
        }
    )
@login_required
def last_7_days_data_view_green(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Calculate the start date for the last 7 days
    last_7_days_start = date.today() - timedelta(days=7)

    # Fetch and aggregate data for the last 7 days
    last_7_days_data = GreenShuttle.objects.filter(date__gte=last_7_days_start).values('stop_name').annotate(
        total_passengers_in=Sum('number_of_passangers_in')
    )

    # Sort data based on the pre-defined stop order
    sorted_data = sorted(last_7_days_data, key=lambda x: stop_index_map.get(x['stop_name'], len(stops)))

    # Calculate the total number of passengers in the last 7 days
    last_7_days_total = last_7_days_data.aggregate(total=Sum('total_passengers_in'))['total'] or 0

    # Render the data to the template
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
def filtered_shuttle_data_view_green(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Get filter parameters from the request
    specific_date = request.GET.get('date')
    specific_stop = request.GET.get('stop')
    custom_start_date = request.GET.get('start_date')
    custom_end_date = request.GET.get('end_date')

    # Prepare dynamic filter conditions
    filter_conditions = {}

    # Handle specific date filter
    if specific_date and specific_date != 'None':  # Avoid 'None' string value
        try:
            datetime.strptime(specific_date, '%Y-%m-%d')
            filter_conditions['date'] = specific_date
        except ValueError:
            pass  # Handle invalid date format if needed

    # Handle specific stop filter
    if specific_stop and specific_stop != 'None':
        filter_conditions['stop_name'] = specific_stop

    # Handle custom date range filter
    if custom_start_date and custom_end_date:
        try:
            datetime.strptime(custom_start_date, '%Y-%m-%d')
            datetime.strptime(custom_end_date, '%Y-%m-%d')
            filter_conditions['date__range'] = [custom_start_date, custom_end_date]
        except ValueError:
            pass  # Handle invalid date formats if needed

    # Query BlueShuttle model with the filter conditions
    stop_data = GreenShuttle.objects.filter(**filter_conditions).values('date', 'stop_name').annotate(
        total_passengers_in=Sum('number_of_passangers_in')
    )

    # Sort the stop data using the predefined stop index map
    stop_data = sorted(stop_data, key=lambda x: stop_index_map.get(x['stop_name'], len(stops)))

    # Paginate the results
    paginator = Paginator(stop_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate the total number of passengers
    total_passengers = sum(entry['total_passengers_in'] for entry in stop_data)

    # Render the filtered data to the template
    return render(
        request,
        'filtered-data.html',
        {
            'page_obj': page_obj,
            'total_passengers': total_passengers,
            'stops': stops,
            'selected_date': specific_date,
            'selected_stop': specific_stop,
            'custom_start_date': custom_start_date,
            'custom_end_date': custom_end_date,
        }
    )


