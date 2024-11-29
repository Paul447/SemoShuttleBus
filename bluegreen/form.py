# forms.py
from django import forms
from .models import BlueShuttle, LastStopBlueOccupancy

class BlueShuttleForm(forms.ModelForm):
    class Meta:
        model = BlueShuttle
        fields = ['stop_name', 'number_of_passangers_in', 'number_of_passangers_out',]

    # You can add custom validation or widgets here
    def clean_number_of_passangers_out(self):
        number_of_passangers_out = self.cleaned_data.get('number_of_passangers_out')
        stop_occcupancy_value, _ = LastStopBlueOccupancy.objects.get_or_create(id=1)
        
        if number_of_passangers_out > stop_occcupancy_value.blue_occupancy:
            raise forms.ValidationError("Passengers departing must be fewer than passengers in the shuttle.")
        return number_of_passangers_out
