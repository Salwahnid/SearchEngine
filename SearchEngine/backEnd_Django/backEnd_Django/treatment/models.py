# backEnd_Django/models.py
from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255)  # Nom du fichier
    content = models.TextField()  # Contenu textuel du fichier, extrait à partir du PDF ou autre
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de dernière mise à jour

    def __str__(self):
        return self.name
