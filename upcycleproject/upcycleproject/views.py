from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
from django.conf import settings
from google.cloud import vision
from upcycleproject.models import Client
from upcycleproject.models import ItemThrown, Category

credentials_path = os.path.join(settings.BASE_DIR, 'upcycleproject', 'credentials', 'upcyclecrewconfig.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

related_computer_strings = [
    'computer', 'netbook', 'notebook', 'laptop', 'personal computer',
    "computer monitor", "Peripheral", "Output device", "monitor", "computer screen"
]

related_hardware_strings = [
    "output device", "office equipment", "gadget", "machine", "peripheral", 
    "input device", "computer keyboard", "office equipment", "keyboard", "cable", 
    "wire", "electric blue", "electronics accessory", "electrical wiring", 
    "electrical supply", "azure", "machine", "hardware, fiber"
]

related_mobile_device_strings = [
    "mobile phone", "communication Device", "telephony", "mobile device", 
    "portable communications device", "portable", "cellular network", "telephone"
]

@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        cpf = request.POST.get('cpf') 
        if image and cpf:
            try:
                client = Client.objects.get(cpf=cpf)
                image_content = image.read()
                
                # Receive the response from the detect_labels function
                labels_response = detect_labels(image_content)
                
                # Initialize found_type as "NONE"
                found_type = "NONE"

                # Iterate over each label to find a match in any list
                for label in labels_response.get('labels', []):
                    description = label.get('description', '').lower()

                    # Check if the description matches any list
                    if description in [item.lower() for item in related_computer_strings]:
                        found_type = "computer"
                        break
                    elif description in [item.lower() for item in related_hardware_strings]:
                        found_type = "hardware"
                        break
                    elif description in [item.lower() for item in related_mobile_device_strings]:
                        found_type = "mobile_device"
                        break

                # Just print the found type
                print(found_type)
                print(cpf)
                item = ItemThrown.objects.create(category=found_type, client=client)
                item.save()

                # Return the labels_response as requested
                return JsonResponse(labels_response)
            except Client.DoesNotExist:
                return JsonResponse({'error': 'Client not found'}, status=404)
        else:
            return JsonResponse({'error': 'Image or CPF not provided'}, status=400)
   
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt    
def detect_labels(image_content):
    """Detect labels in the image using binary content."""
    client = vision.ImageAnnotatorClient()
    
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)

    labels = [{"description": label.description, "score": label.score} for label in response.label_annotations]
    
    if response.error.message:
        return {'error': response.error.message}

    return {'labels': labels}

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        cpf = data.get('cpf')
        email = data.get('email')

        if not cpf or not email:
            return JsonResponse({'error': 'CPF e email são obrigatórios.'}, status=400)

        client = Client.objects.create(cpf=cpf, email=email)
        
        return JsonResponse({'user': {'cpf': client.cpf, 'email': client.email}})
    
