from django.contrib import admin
from .models import Shuttle , GreenShuttle ,    BlueShuttle, ShuttleStopIndex , greenShuttleStopIndex , LastStopGreenOccupancy, LastStopBlueOccupancy
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
import pdb

@admin.register(Shuttle)
class ShuttleAdmin(admin.ModelAdmin):
    list_display = ('shuttle_name',  'shuttle_capacity', )
    search_fields = ('shuttle_name', )
    list_filter = ('shuttle_name',)

    # Using fieldsets to organize fields
    fieldsets = (
        ('Basic Information', {
            'fields': ('shuttle_name',)
        }),
        ('Capacity and Driver', {
            'fields': ('shuttle_capacity',)
        }),
    )

@admin.register(BlueShuttle)
class BlueShuttleAdmin(admin.ModelAdmin):
    list_display = ('stop_name', 'number_of_passangers_in', 'number_of_passangers_out', 'date', 'time', 'shuttle_driver', 'shuttle_detail','occupancy_detail')
    search_fields = ( 'number_of_passangers_in', 'number_of_passangers_out',)
    list_filter = ( 'number_of_passangers_in', 'number_of_passangers_out',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('blue_name_display', 'number_of_passangers_in','time', 'number_of_passangers_out','blue_occupancy_display', 'blue_available_seats_display')
        }),
    )
    readonly_fields = ('blue_name_display','blue_occupancy_display','blue_available_seats_display' )

    stops = [
    "Towers",
    "Grauel",
    "UC/Kent/Academic",
    "Vandiver/Merick",
    "Rear Kent",
    "Pacific/Grauel",
    "Catapult",
    "Mass Media",
    "Spanish/Independence",
    "River Campus",
    "Band Annex",
    "River Campus Arts Building",
    "Vandiver/Merick",
    "Bookstore",
    "Memorial/Parker/Academic",
    "Scully/Parker",
    "Dempster",
    "Polytech/Laferla",
    "MMTF",
    "International Village"
    ]

    # Occupancy Calculation
    def blue_occupancy_display(self, obj):
        stop_occcupancy_value, _ = LastStopBlueOccupancy.objects.get_or_create(id=1)
        return stop_occcupancy_value.blue_occupancy
    blue_occupancy_display.short_description = 'Blue Occupancy'


    # Seat Availability Calculation
    def blue_available_seats_display(self, obj):
        stop_occcupancy_value, _ = LastStopBlueOccupancy.objects.get_or_create(id=1) # Getting the last stop occupancy value of blue
        shuttle_capacity_value = Shuttle.objects.get(shuttle_name='Blue Route') # Getting the shuttle capacity of blue 
        return shuttle_capacity_value.shuttle_capacity - stop_occcupancy_value.blue_occupancy # Subtracting the current occupancy from the shuttle capacity
    blue_available_seats_display.short_description = 'Blue Available Seats'

    # Stop Name Calculation
    def blue_name_display(self, obj):
        stop_index, created = ShuttleStopIndex.objects.get_or_create(id=1) 
        return self.stops[stop_index.blue_index_value]
    blue_name_display.short_description = 'Stop Name'

    def save_model(self, request, obj, form, change):
        # Retrieve the current index from the database
        stop_index, created = ShuttleStopIndex.objects.get_or_create(id=1)  # Assume single row for index

        # Set the stop name based on the current index value
        stop_occcupancy_value,created = LastStopBlueOccupancy.objects.get_or_create(id=1)
        if obj.number_of_passangers_out > stop_occcupancy_value.blue_occupancy :
             self.message_user(request, "Passengers departing must be fewer than passengers in the shuttle.", messages.ERROR)
             return
        
        if stop_occcupancy_value.blue_occupancy <=0:
            stop_occcupancy_value.blue_occupancy = obj.number_of_passangers_in - obj.number_of_passangers_out
            stop_occcupancy_value.save()
        else:
            stop_occcupancy_value.blue_occupancy = stop_occcupancy_value.blue_occupancy + obj.number_of_passangers_in - obj.number_of_passangers_out
            stop_occcupancy_value.save()
        obj.stop_name = self.stops[stop_index.blue_index_value]

        # Update the index value for the next entry
        stop_index.blue_index_value += 1
        if stop_index.blue_index_value >= len(self.stops):
            stop_index.blue_index_value = 0  # Reset to 0 when the last stop is reached

        # Save the new index value back to the database
        stop_index.save()

        # Optionally, assign shuttle driver and details if not set
        if not obj.shuttle_driver:
            obj.shuttle_driver = request.user
            obj.shuttle_detail = Shuttle.objects.get(shuttle_name='Blue Route')
        if not obj.occupancy_detail:
            obj.occupancy_detail = stop_occcupancy_value.blue_occupancy


        # Save the BlueShuttle object
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Optionally customize the queryset for foreign key fields here
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(ShuttleStopIndex)
class ShuttleStopIndexAdmin(admin.ModelAdmin):
    list_display = ('blue_index_value',)
    actions = ['reset_index_to_zero']  # Add action here
    def reset_index_to_zero(self, request, queryset):
        stop_index = ShuttleStopIndex.objects.first()  # Assuming there's one index record
        stop_index.blue_index_value = 0
        stop_index.save()
        self.message_user(request, "Index reset to 0 successfully.", messages.SUCCESS)

    reset_index_to_zero.short_description = "Reset index to 0"


@admin.register(LastStopBlueOccupancy)
class LastStopBlueOccupancyAdmin(admin.ModelAdmin):
    list_display = ('blue_occupancy',)
    actions = ['reset_occupancy_to_zero']
    def reset_occupancy_to_zero(self, request, queryset):
        stop_occupancy = LastStopBlueOccupancy.objects.first()
        stop_occupancy.blue_occupancy = 0
        stop_occupancy.save()
        self.message_user(request, "Occupancy reset to 0 successfully.", messages.SUCCESS)
        


@admin.register(GreenShuttle)
class GreenShuttleAdmin(admin.ModelAdmin):
    list_display = ( 'stop_name','number_of_passangers_in','number_of_passangers_out','date','time','shuttle_driver','shuttle_detail')
    search_fields = (  'number_of_passangers_in','number_of_passangers_out',)
    list_filter = ('number_of_passangers_in','number_of_passangers_out',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('stop_name_display', 'number_of_passangers_in','number_of_passangers_out', 'green_occupancy_display', 'green_available_seats_display')
        }),
    )

    class Meta:
        verbose_name = "Green Shuttle Entry"
        verbose_name_plural = "Green Shuttle Entries"

    readonly_fields = ('stop_name_display','green_occupancy_display','green_available_seats_display' )
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


    def green_occupancy_display(self, obj):
        stop_occcupancy_value, _ = LastStopGreenOccupancy.objects.get_or_create(id=1)
        return stop_occcupancy_value.green_occupancy
    green_occupancy_display.short_description = 'Green Occupancy'

    def green_available_seats_display(self, obj):
        stop_occcupancy_value, _ = LastStopGreenOccupancy.objects.get_or_create(id=1)
        shuttle_capacity_value = Shuttle.objects.get(shuttle_name='Green Route')
        return shuttle_capacity_value.shuttle_capacity - stop_occcupancy_value.green_occupancy
    green_available_seats_display.short_description = 'Green Available Seats'

    def stop_name_display(self, obj):
        stop_index, created = greenShuttleStopIndex.objects.get_or_create(id=1) 
        return self.stops[stop_index.green_index_value]
    stop_name_display.short_description = 'Stop Name'


    def save_model(self, request, obj, form, change):
        stop_index, created = greenShuttleStopIndex.objects.get_or_create(id=1)  # Assume single row for index
        stop_occcupancy_value,created = LastStopGreenOccupancy.objects.get_or_create(id=1)
        if obj.number_of_passangers_out > stop_occcupancy_value.green_occupancy :
             self.message_user(request, "Passengers departing must be fewer than passengers in the shuttle.", messages.ERROR)
             return
        
        if stop_occcupancy_value.green_occupancy <=0:
            stop_occcupancy_value.green_occupancy = obj.number_of_passangers_in - obj.number_of_passangers_out
            stop_occcupancy_value.save()
        else:
            stop_occcupancy_value.green_occupancy = stop_occcupancy_value.green_occupancy + obj.number_of_passangers_in - obj.number_of_passangers_out
            stop_occcupancy_value.save()
        
        
        # Set the stop name based on the current index value
        obj.stop_name = self.stops[stop_index.green_index_value]

        # Update the index value for the next entry
        stop_index.green_index_value += 1
        if stop_index.green_index_value >= len(self.stops):
            stop_index.green_index_value = 0  # Reset to 0 when the last stop is reached

        # Save the new index value back to the database
        stop_index.save()
        if not obj.shuttle_driver:
            obj.shuttle_driver = request.user
            obj.shuttle_detail = Shuttle.objects.get(shuttle_name='Green Route')
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Optionally customize the queryset for foreign key fields here
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(greenShuttleStopIndex)   
class greenShuttleStopIndexAdmin(admin.ModelAdmin):
    list_display = ('green_index_value',)
    actions = ['reset_index_to_zero']  # Add action here
    def reset_index_to_zero(self, request, queryset):
        stop_index = greenShuttleStopIndex.objects.first()  # Assuming there's one index record
        stop_index.green_index_value = 0
        stop_index.save()
        self.message_user(request, "Index reset to 0 successfully.", messages.SUCCESS)
    reset_index_to_zero.short_description = "Reset index to 0"

@admin.register(LastStopGreenOccupancy)
class LastStopGreenOccupancyAdmin(admin.ModelAdmin):
    list_display = ('green_occupancy',)
    actions = ['reset_occupancy_to_zero']
    def reset_occupancy_to_zero(self, request, queryset):
        stop_occupancy = LastStopGreenOccupancy.objects.first()
        stop_occupancy.green_occupancy = 0
        stop_occupancy.save()
        self.message_user(request, "Occupancy reset to 0 successfully.", messages.SUCCESS)

#Add the number of people inside the shuttle
#making the value able to setnull in and out value 
#Invalid input handling by checking the last stop in value and out value 
#Person getting out cant be more than the person who got inside the shuttle bus 





# Register the Shuttle model with the customized admin
# admin.site.register(Shuttle, ShuttleAdmin)

