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
from django.core.mail import EmailMessage, get_connection

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
def receive_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        cpf = request.POST.get('cpf') 
        if image and cpf:
            try:
                client = Client.objects.get(cpf=cpf)
                image_content = image.read()
                
                labels_response = detect_labels(image_content)
                
                found_type = "NONE"

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

                print(found_type)
                print(cpf)
                item = ItemThrown.objects.create(category=found_type, client=client)
                item.save()
                client.livelo_points += livelo_update_points
                client.save()
                send_email(item.client.email)
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

def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        cpf = data.get('cpf')
        email = data.get('email')

        if not cpf or not email:
            return JsonResponse({'error': 'CPF e email são obrigatórios.'}, status=400)

        client = Client.objects.create(cpf=cpf, email=email)
        
        return JsonResponse({'user': {'cpf': client.cpf, 'email': client.email}})
    
def send_email(email):
    subject = "Hello from Django SMTP"
    recipient_list = [email]
    from_email = "onboarding@resend.dev"
    message = f"<strong>Parabéns pela ajuda! Sua colaboração cria um mundo melhor! Você acaba de receber uma recompensa de</strong>"

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    email.content_subtype = "html" 
    
    try:
        print("cai aqui")
        email.send()  
    except Exception as e:
        print("Erro no envio de e-mail:", str(e))
    