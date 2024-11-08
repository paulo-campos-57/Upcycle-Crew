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
img_path = os.path.join(settings.BASE_DIR, 'upcycleproject', 'static', 'upcycleproject', 'img')
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
                
                if found_type == "NONE":
                    print('cai aqui')
                    return JsonResponse({'error': 'Item is not an electronic'}, status=404)

                if unit.weight < livelo_update_points:
                    send_email_bb(client.email)
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
                
                return JsonResponse({'found_type': found_type})
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
    

def send_email_bb(email):
    subject = "Parabéns pela sua contribuição!"
    recipient_list = [email]
    from_email = settings.EMAIL_HOST_USER  # Certifique-se de que este email está autorizado a enviar emails pelo seu servidor SMTP

    # HTML do email, com URL pública para a logo
    message = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email de Notificação</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
          background-color: #f4f4f4;
        }
        .email-container {
          width: 100%;
          max-width: 600px;
          background-color: #ffffff;
          border: 1px solid #ddd;
          margin: auto;
        }
        .header {
          background-color: #1653fc;
          color: #FFDD00;
          padding: 20px;
          text-align: center;
        }
        .content {
          padding: 20px;
          text-align: left;
        }
        .highlight {
          background-color: #FFDD00;
          color: #1653fc;
          padding: 15px;
          margin: 20px 0;
          text-align: center;
          font-weight: bold;
        }
        .footer {
          background-color: #616264;
          color: #ffffff;
          padding: 10px;
          text-align: center;
          font-size: 12px;
        }
      </style>
    </head>
    <body>
      <table class="email-container" align="center" cellpadding="0" cellspacing="0">
        <tr>
          <td class="header">
            <h2 style="margin: 10px 0;">Lixeira Atingiu a Capacidade Máxima</h2>
          </td>
        </tr>
        <tr>
          <td class="content">
            <h1 style="font-size: 24px; color: #1653fc; margin-bottom: 10px;">Atenção: Coleta Necessária</h1>
            <p>Olá,</p>
            <p>Informamos que a unidade de descarte do ponto de coleta <strong>Ponto de Coleta X</strong> atingiu a capacidade máxima de <strong>100kg</strong> de descartes eletrônicos. Por favor, programe o envio de um caminhão para recolher o material.</p>
            <div class="highlight">
              Lixeira cheia com 100kg - Coleta necessária!
            </div>
          </td>
        </tr>
        <tr>
          <td class="footer">
            <p>Empresa de Gestão de Resíduos Eletrônicos</p>
            <p>Endereço: Rua Exemplo, 123, Cidade</p>
            <p>Telefone: (11) 1234-5678</p>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    try:
        send_mail(
            subject=subject,
            message='',  # Mensagem em texto plano (pode ser vazia se estiver enviando apenas HTML)
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=message
        )
    except Exception as e:
        print("Erro no envio de e-mail:", str(e))


def send_email(email, points):
    subject = "Obrigado por descartar com consciência!"
    recipient_list = [email]
    from_email = settings.EMAIL_HOST_USER  # Certifique-se de que este email está autorizado a enviar emails pelo seu servidor SMTP

    # HTML do email, com URL pública para a logo
    message = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email de Notificação</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 0; padding: 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin: auto;">
              
              <!-- Header Section -->
              <tr>
                <td align="center" style="background-color: #1653fc; color: #FFDD00; padding: 20px; text-align: center;">
                  <h2 style="margin: 10px 0; font-size: 24px; color: #FFDD00;">Obrigado por descartar com consciência!</h2>
                </td>
              </tr>
              
              <!-- Content Section -->
              <tr>
                <td style="padding: 20px; text-align: center;">
                  <h1 style="font-size: 24px; color: #1653fc; margin: 0 0 10px 0;">Parabéns por contribuir com um futuro mais sustentável!</h1>
                  <p style="font-size: 18px; color: #666666; line-height: 1.6; margin: 5px 0;">Por sua atitude, queremos te recompensar</p>
                  <div style="color: #1653fc; background-color: #FFDD00; padding: 15px; margin: 20px 0; border-radius: 5px; text-align: center; font-size: 20px; font-weight: bold;">
                    Você acaba de ganhar {points} pontos Livelo!
                  </div>
                </td>
              </tr>
              
              <!-- Footer Section -->
              <tr>
                <td align="center" style="background-color: #616264; color: #ffffff; padding: 10px; text-align: center; font-size: 12px;">
                  <p style="margin: 0;">Empresa de Gestão de Resíduos Eletrônicos</p>
                  <p style="margin: 0;">Endereço: Rua Exemplo, 123, Cidade</p>
                  <p style="margin: 0;">Telefone: (11) 1234-5678</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    try:
        send_mail(
            subject=subject,
            message='',  # Mensagem em texto plano (pode ser vazia se estiver enviando apenas HTML)
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
