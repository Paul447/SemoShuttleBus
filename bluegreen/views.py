from django.shortcuts import render
from django.http import HttpResponse
from .models import Shuttle, GreenShuttle, greenShuttleStopIndex, LastStopGreenOccupancy, BlueShuttle
from django.shortcuts import render
from .models import BlueShuttle  # Import your BlueShuttle model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
def index(request):
    shuttle_data = BlueShuttle.objects.all().values()
    df = pd.DataFrame(shuttle_data)

    # print("Step 1: Fetched Data\n", df[['number_of_passangers_in', 'number_of_passangers_out']].head())
    # Extract the hour component directly from the time field
    df['hour'] = df['time'].apply(lambda t: t.hour if pd.notnull(t) else None)
    # print("\nStep 2: Added Hour Column\n", df[['stop_name', 'time', 'hour']].head())

    df_grouped = df.groupby(['stop_name', 'hour']).agg({
        'number_of_passangers_in': 'sum',
        'number_of_passangers_out': 'sum',
        'occupancy_detail': 'sum'  # Use 'occupancy_detail' for the initial occupancy for each stop
    }).reset_index()
    print("\nStep 3: Grouped Data by Stop and Hour\n", df_grouped.head())  
    shuttle_data_list = df[['date', 'time']].head().to_dict(orient='records')
    return render(request, 'index.html', {'shuttle_data': shuttle_data_list})
