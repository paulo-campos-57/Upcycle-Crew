from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings
from google.cloud import vision

credentials_path = os.path.join(settings.BASE_DIR, 'upcycleproject', 'credentials', 'upcyclecrewconfig.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Lê o conteúdo da imagem como binário
            image_content = image.read()

            # Passa o conteúdo binário para a função de detecção de rótulos
            return detect_labels(image_content)
        else:
            return JsonResponse({'error': 'No image provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def detect_labels(image_content):
    """Detecta rótulos na imagem usando o conteúdo binário."""
    client = vision.ImageAnnotatorClient()
    
    # Cria um objeto de imagem com o conteúdo binário
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)

    # Extrai os rótulos detectados
    labels = [{"description": label.description, "score": label.score} for label in response.label_annotations]
    
    if response.error.message:
        return JsonResponse({'error': response.error.message}, status=500)

    return JsonResponse({'labels': labels})

