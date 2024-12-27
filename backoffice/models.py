from django.db import models
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from datetime import datetime
import uuid
from django.utils.functional import cached_property
from django.urls.base import reverse

class RapportModel(DjangoCassandraModel):
    rapport_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    utilisateur_id = columns.Integer(index=True)
    erreur = columns.Text()
    rapport = columns.Integer()
    date_creation = columns.DateTime(default=datetime.now)

    def __str__(self):
        return self.erreur
    
    class Meta:
        get_pk_field = 'rapport_id'
        verbose_name = 'Rappport'

class MessagerieModel(DjangoCassandraModel):
    messagerie_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    vues = columns.Integer(default=0)
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur_utilisateur = columns.Text()
    interlocuteur_utilisateur = columns.Text()
    utilisateur_id_groupe = columns.Text()
    utilisateur_groupe_utilisateur = columns.Text()
    message_premier = columns.Text()
    message_liste = columns.Text()
    utilisateur_liste = columns.Text()
    date = columns.DateTime(default=datetime.now)
    temps = columns.DateTime(default=datetime.now)

    def __str__(self):
        return f'{self.utilisateur_1_utilisateur} {self.utilisateur_2_utilisateur}'
    
    class Meta:
        get_pk_field = 'messagerie_id'
        verbose_name = 'Messagerie'

class MessageModel(DjangoCassandraModel):
    message_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    utilisateur_id_groupe = columns.Text()
    interlocuteur_id = columns.Integer()
    message = columns.Text()
    date = columns.DateTime(default=datetime.now)

    def __str__(self):
        return self.message
    
    class Meta:
        get_pk_field = 'message_id'
        verbose_name = 'Message'

class DepartementModel(models.Model):
    departement_id = models.AutoField(primary_key=True)
    departement = models.CharField(max_length=1024,null=True, blank=True)
    departement_unicode = models.CharField(max_length=1024,null=True, blank=True)
    titre = models.CharField(max_length=1024,null=True, blank=True)
    lang = models.CharField(max_length=1024,null=True, blank=True)
    description = models.TextField(max_length=1024,null=True, blank=True)
    pays = models.CharField(max_length=1024,null=True, blank=True)
    region = models.CharField(max_length=1024,null=True, blank=True)
    prefecture = models.CharField(max_length=1024,null=True, blank=True)
    image = models.CharField(max_length=1024,null=True, blank=True)
    url = models.CharField(max_length=1024,null=True, blank=True)
    vues = models.IntegerField(default=0, null=True, blank=True)
    noindex = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.departement} {self.lang}'

    class Meta:
        verbose_name = 'departement'
        indexes = [models.Index(fields=['departement'], name='backoffice__departe_e3b317_idx')]

    @cached_property
    def url_frontend(self):
        return f"https://wivivi.com{reverse('departement_url', args=[self.lang, self.url])}"



class RegionModel(models.Model):
    region_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=1024,null=True, blank=True)
    departement_liste = models.CharField(max_length=1024,null=True, blank=True)
    titre = models.CharField(max_length=1024,null=True, blank=True)
    lang = models.CharField(max_length=1024,null=True, blank=True)
    description = models.TextField(max_length=1024,null=True, blank=True)
    pays = models.CharField(max_length=1024,null=True, blank=True)
    image = models.CharField(max_length=1024,null=True, blank=True)
    url = models.CharField(max_length=1024,null=True, blank=True)
    vues = models.IntegerField(default=0, null=True, blank=True)
    noindex = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.region}'

    class Meta:
        verbose_name = 'region'
        indexes = [models.Index(fields=['region'], name='backoffice__region_48fcd2_idx')]
     
    @cached_property
    def url_frontend(self):
        return f"https://wivivi.com{reverse('region_url', args=[self.lang, self.url])}"


class PageModel(models.Model):
    page_id = models.AutoField(primary_key=True)
    page = models.CharField(max_length=1024,null=True, blank=True)
    titre = models.CharField(max_length=1024,null=True, blank=True)
    lang = models.CharField(max_length=1024,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=3024,null=True, blank=True)
    groupe = models.CharField(max_length=1024,null=True, blank=True)
    h1 = models.CharField(max_length=1024,null=True, blank=True)
    h2 = models.CharField(max_length=1024,null=True, blank=True)
    template = models.CharField(max_length=1024,null=True, blank=True)
    texte1 = models.TextField(null=True, blank=True)
    texte2 = models.TextField(max_length=20000,null=True, blank=True)
    boutton = models.CharField(max_length=60,null=True, blank=True)
    ancre1 = models.CharField(max_length=60,null=True, blank=True)
    ancre2 = models.CharField(max_length=60,null=True, blank=True)
    url_n1 = models.CharField(max_length=4024,null=True, blank=True)
    vues = models.IntegerField(default=0, null=True, blank=True)
    noindex = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.page} {self.lang}'

    class Meta:
        verbose_name = 'page'
        indexes = [models.Index(fields=['page'], name='backoffice__page_36aee4_idx')]

    @cached_property
    def url_frontend(self):
        return f"https://wivivi.com{reverse('page_url', args=[ self.url_n1])}"

class MiseRelationModel(DjangoCassandraModel):
    mise_relation_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur = columns.Text()
    session_id = columns.Text()
    lang = columns.Text()
    date_creation = columns.DateTime(default=datetime.now)

    def __str__(self):
        return f'{self.mise_relation_id} {self.utilisateur_id}'
    
    class Meta:
        get_pk_field = 'mise_relation_id'
        #indexes = [models.Index(fields=['utilisateur_id','interlocuteur_id'])]
        verbose_name = 'Mise relation'

class PaiementModel(DjangoCassandraModel):
    paiement_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    utilisateur_id = columns.Integer(index=True)
    utilisateur = columns.Text()
    session_id = columns.Text()
    lang = columns.Text()
    email = columns.Text()
    telephone = columns.Text()
    date_creation = columns.DateTime(default=datetime.now)
    paiement_valide = columns.Integer(default=0)
    prix = columns.Decimal(default=0)
    devise = columns.Text(default='Eur')

    
    def __str__(self):
        return f'{self.paiement_id}'
    
    class Meta:
        get_pk_field = 'paiement_id'
        #indexes = [models.Index(fields=['utilisateur_id'])]
        verbose_name = 'Paiement'

class ContactModel(DjangoCassandraModel):
    contact_id = columns.Text(primary_key=True, default=uuid.uuid4().hex )
    utilisateur_id = columns.Integer(index=True)
    utilisateur = columns.Text()
    sujet = columns.Text()
    question = columns.Text()
    lang = columns.Text()
    email = columns.Text()
    telephone = columns.Text()
    date_creation = columns.DateTime(default=datetime.now)
    contact_valide = columns.Integer()

    def __str__(self):
        return f'{self.question}'
    
    class Meta:
        get_pk_field = 'contact_id'
        #indexes = [models.Index(fields=['utilisateur_id'])]
        verbose_name = 'Contact'