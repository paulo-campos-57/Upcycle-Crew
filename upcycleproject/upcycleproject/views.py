from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
from django.conf import settings
from google.cloud import vision
from upcycleproject.models import Client
from upcycleproject.models import ItemThrown, Category, Unit
from django.core.mail import EmailMessage, get_connection
from django.core.mail import send_mail
import re


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
    "electrical supply", "azure", "machine", "hardware, fiber", "computer hardware", "electronic engineering",

]

related_mobile_device_strings = [
    "mobile phone", "communication Device", "telephony", "mobile device", 
    "portable communications device", "portable", "cellular network", "telephone"
]

@csrf_exempt
def receive_image(request, unit_id):
    print('eu caí na função')
    if request.method == 'POST':
        image = request.FILES.get('image')
        cpf = request.POST.get('cpf') 
        print("Content-Type:", request.META.get('CONTENT_TYPE'))
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        print('recebi esse unit_id:', unit_id)

        if image and cpf:
            print('ola')
            cpf = re.sub(r'\D', '', cpf)
            try:
                print('passei de bloco 0')
                client = Client.objects.get(cpf=cpf)
                print('passei de bloco 0.5')
                unit_id = int(unit_id)
                unit = Unit.objects.get(id=unit_id)
                print('passei de bloco 1')

                image_content = image.read()
                labels_response = detect_labels(image_content)
                found_type = "NONE"
                livelo_update_points = 0
                print('passei de bloco 2')


                for label in labels_response.get('labels', []):
                    description = label.get('description', '').lower()

                    if description in [item.lower() for item in related_computer_strings]:
                        found_type = "computer"
                        livelo_update_points = 20     
                        break
                    elif description in [item.lower() for item in related_hardware_strings]:
                        found_type = "hardware"
                        livelo_update_points = 30
                        break
                    elif description in [item.lower() for item in related_mobile_device_strings]:
                        found_type = "mobile_device"
                        livelo_update_points = 10
                        break
                
                # if found_type == "NONE":
                #     print('cai aqui')
                #     return JsonResponse({'error': 'Item is not an electronic'}, status=404)

                if unit.weight < livelo_update_points:
                    return JsonResponse({'error': 'Unit does not have enough space'}, status=400)
                
                # Processar o item
                item_weight = livelo_update_points
                ItemThrown.objects.create(category=found_type, client=client, unit=unit)
                unit.weight -= item_weight
                print('passei de bloco 3')
                unit.save()
                client.livelo_points += livelo_update_points
                client.save()
                send_email(client.email, livelo_update_points)
                return JsonResponse(labels_response)
            except (Client.DoesNotExist, Unit.DoesNotExist):
                return JsonResponse({'error': 'Client or Unit not found'}, status=404)
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
    

def send_email(email, points):
    subject = "Parabéns pela sua contribuição!"
    recipient_list = [email]
    from_email = settings.EMAIL_HOST_USER  # Ensure this email is authorized to send emails via your SMTP server
    message = f"<strong>Parabéns pela ajuda! Sua colaboração cria um mundo melhor! Você acaba de receber uma recompensa de {points} pontos!</strong>"

    try:
        send_mail(
            subject=subject,
            message='',  # Plain text message (can be empty if only sending HTML)
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=message
        )
    except Exception as e:
        print("Erro no envio de e-mail:", str(e))

@csrf_exempt    
def create_unit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Create a new Unit object with the provided data
        unit = Unit.objects.create(
            city=data.get('city'),
            neighbourhood=data.get('neighbourhood'),
            street=data.get('street'),
            number=data.get('number'),
            postal_code=data.get('postal_code'),
            weight=100
        )
        
        return JsonResponse({  
            'city': unit.city,
            'neighborhood': unit.neighbourhood,
            'street': unit.street,
            'number': unit.number,
            'id': unit.id,
            'postal_code': unit.postal_code
        }, status=201)
