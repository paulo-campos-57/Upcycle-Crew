from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import IntegrityError

def create_default_clients(sender, **kwargs):
    from .models import Client

    clients = [
        {'cpf': '11933512431', 'email': 'user1@example.com'},
        {'cpf': '70467564493', 'email': 'user2@example.com'},
        {'cpf': '70367237423', 'email': 'user3@example.com'}
    ]

    for client_data in clients:
        if not Client.objects.filter(cpf=client_data['cpf']).exists():
            try:
                Client.objects.create(**client_data)
                print(f"Usuário criado com CPF {client_data['cpf']} e email {client_data['email']}")
            except IntegrityError:
                print(f"Erro ao criar usuário com CPF {client_data['cpf']}")

class UpcycleProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'upcycleproject'

    def ready(self):
        post_migrate.connect(create_default_clients, sender=self)
