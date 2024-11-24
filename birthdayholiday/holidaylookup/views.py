from django.shortcuts import render
from django.http import JsonResponse
from .forms import IDCheckForm
from .models import PublicHoliday,SAIDRecord
import requests
import datetime


# Create your views here.

def decorded_SAID(id_number):
    # Extract relevant parts of the ID
    current_year = datetime.datetime.now().year
    century = 1900 if int(id_number[:2]) > current_year % 100 else 2000
    birth_year = century + int(id_number[:2])
    birth_date = datetime.date(birth_year, int(id_number[2:4]), int(id_number[4:6]))
    gender = "Male" if int(id_number[6:10]) >= 5000 else "Female"
    is_sa_citizen = id_number[10] == "0"
    return birth_date, gender, is_sa_citizen

def check_holiday(request):
    if request.method == 'POST':
        form = IDCheckForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']

            #Decord the SAID
            date_of_birth , gender , is_sa_citizen = decorded_SAID(id_number)

            #Update or Create record in SAIDRecord

            print("Now creating SAID Record")

            record, created = SAIDRecord.objects.get_or_create(id_number=id_number, defaults={
                "date_of_birth": date_of_birth,
                "gender": gender,
                "is_sa_citizen": is_sa_citizen,
            })

            record.search_count += 1
            record.save()

            print("Successfully created SAID Record")

            url = "https://calendarific.com/api/v2/holidays"
            params = {
                    "api_key": "6wHLo8RgHynaQ19v00GW2YtPYp8uXVUJ",
                    "country": "ZA",
                    "year": date_of_birth.year,
                    "type": "national",
                }

            try:
                response = requests.get(url,params=params)
                response.raise_for_status()
                data = response.json()

                print(data["response"]) 

                # Filter holidays matching date_of_birth
                holidays = [
                    holiday for holiday in data["response"]["holidays"]
                    if holiday.get("date", {}).get("iso") == date_of_birth.isoformat()
                ]

                if not holidays:
                    print(f"No holidays found for date: {date_of_birth.isoformat()}")

                #Store the holidays in PublicHoliday model
                for holiday in holidays:
                    holiday_type = holiday.get("type", [])
                    type_value = holiday_type[0] if isinstance(holiday_type, list) and holiday_type else "unknown"
                    PublicHoliday.objects.create(
                        said_record=record,
                        name=holiday["name"],
                        description=holiday.get("description",""),
                        date=holiday["date"]["iso"],
                        type=type_value,
                    )

                # Prepare details for rendering
                details = {
                    "id_number": record.id_number,
                    "date_of_birth": record.date_of_birth,
                    "gender": record.gender,
                    "citizenship": "South African Citizen" if record.is_sa_citizen else "Permanent Resident",
                    "search_count": record.search_count,
                }

                return render(request, "holidaylookup/check_holiday.html", {
                    "form": form,
                    "details": details,
                    "holidays": holidays,
                })

            except requests.exceptions.RequestException as e:
                return JsonResponse({"error":f"Failed to fetch holidays: {str(e)}"}, status=500)
        else:
            return render(request,"holidaylookup/check_holiday.html" , {"form": form})
    else:
        form = IDCheckForm()
        return render(request,"holidaylookup/check_holiday.html" , {"form": form})
               
