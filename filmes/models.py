from django.db import models
from django.conf import settings
from django.utils.text import slugify
from random import randint
from django.db.models.signals import post_delete, pre_save

SLUG_LIST = []

# Create your models here.
class Filme(models.Model):
    titulo = models.CharField(primary_key=True, help_text='Digite o titulo do filme', 
                              max_length=50, null=False, blank=False)
    nacionalidade = models.CharField(help_text='Digite a nacionalidade do filme', 
                              max_length=50, null=False, blank=False)
    ano = models.CharField(help_text='Digite o ano de lancamento do filme', 
                              max_length=50, null=False, blank=False)
    sinopse = models.TextField(help_text='Digite a sinopse do filme', 
                              max_length=5000, null=True, blank=True)
    diretor = models.CharField(help_text='Digite o nome do diretor', 
                              max_length=50, null=False, blank=False)
    nota = models.CharField(help_text='Digite a nota que avalia o filme', 
                              max_length=50, null=True, blank=True)
    review = models.TextField(help_text='Digite um breve review do filme', 
                              max_length=5000, null=True, blank=True)
    visto = models.BooleanField(default=False)
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    slug = models.SlugField(blank=True, unique=True)
    
    class Meta:
        ordering = ['titulo']
        managed = True
    
    def __str__(self):

        return self.titulo
    
def pre_save_filme_receiever(sender,instance, *args, **kwargs):

    if not instance.slug:
        slug_random = 0
        while slug_random not in SLUG_LIST:
            slug_random = randint(0,1000)
            SLUG_LIST.append(slug_random)
            
        instance.slug = slugify(instance.usuario.username + "-" + str(slug_random))

pre_save.connect(pre_save_filme_receiever, sender=Filme)