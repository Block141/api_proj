from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_make_id(make_name):
    response = requests.get(
        "https://www.carboninterface.com/api/v1/vehicle_makes",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}", "Content-Type": "application/json"}
    )
    if response.status_code == 200:
        makes_data = response.json()
        for make in makes_data:
            if make['data']['attributes']['name'] == make_name:
                make_id = make['data']['id']
                print(f'make_id: {make_id}')
                return make['data']['id']
    return None

def get_model_id(make_id, model_name):
    response = requests.get(
        f"https://www.carboninterface.com/api/v1/vehicle_makes/{make_id}/vehicle_models",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}", "Content-Type": "application/json"}
    )
    if response.status_code == 200:
        models_data = response.json()
        for model in models_data:
            if model['data']['attributes']['name'] == model_name:
                model_id = model['data']['id']
                print(f'model_id: {model_id}')
                return model['data']['id']
    return None

def get_estimate_form(request):
    return render(request, 'estimate_form.html')

def get_estimate_result(request):
    if request.method == 'POST':
        distance = request.POST['distance']
        year = request.POST['year']
        make = request.POST['make']
        model = request.POST['model']

        make_id = get_make_id(make)
        print(f'Make ID: {make}')
        
        if not make_id:
            return render(request, 'error.html', {'message': 'Invalid make name'})

        model_id = get_model_id(make_id, model)
        if not model_id:
            return render(request, 'error.html', {'message': 'Invalid model name'})
        
        response = requests.post(
            "https://www.carboninterface.com/api/v1/estimates",
            headers={"Authorization": f"Bearer {os.getenv('API_KEY')}", "Content-Type": "application/json"},
            json={
                "type": "vehicle",
                "distance_unit": "mi",
                "distance_value": distance,
                "vehicle_model_id": model_id
            }
        )

        if response.status_code == 200 or response.status_code == 201:
            estimate_data = response.json()
            return render(request, 'estimate_result.html', {'estimate_data': estimate_data})
        else:
            estimate_data = response.json()['data']['attributes']

    return render(request, 'error.html', {'message': 'An error occurred while fetching the estimate data'})