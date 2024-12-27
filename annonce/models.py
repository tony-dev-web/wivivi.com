import uuid
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from datetime import datetime
from django.db import models
from django.utils.functional import cached_property
from django.urls.base import reverse

class RechercheFretModel(models.Model):
    recherche_fret_id = models.AutoField(primary_key=True)
    fret_id = models.CharField(max_length=100, unique=True )
    lang = models.CharField(max_length=2,null=True, blank=True)
    ia = models.CharField(max_length=2024,null=True, blank=True)
    ia_expediteur = models.CharField(max_length=1024,null=True, blank=True)
    ia_destinataire = models.CharField(max_length=1024,null=True, blank=True)
    stamptime = models.IntegerField(null=True, blank=True)
    vues = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.ia}'
    
    class Meta:
        verbose_name = 'recherche fret'
        indexes = [models.Index(fields=['ia'], name='annonce_rec_ia_8b1e6e_idx')]
        ordering = ["stamptime"]

class OptionFretModel(DjangoCassandraModel):
    option_fret_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    lang = columns.Text()
    fret_id = columns.Text()
    utilisateur_id = columns.Integer(index=True)
    option = columns.Text()
    
    def __str__(self):
        return f'{self.ia}'
    
    class Meta:
        get_pk_field = 'option_fret_id'
        verbose_name = 'Option'

class FretModel(DjangoCassandraModel):
    fret_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    utilisateur_id = columns.Integer(index=True)
    utilisateur = columns.Text()
    url = columns.Text()
    lang = columns.Text()
    vues = columns.Integer(default=0)
    titre = columns.Text()
    description = columns.Text()
    
    date_creation = columns.DateTime(default=datetime.now)
    timestamp_creation = columns.Integer()
    
    date_validation = columns.Text()
    timestamp_validation = columns.Integer()
    
    date_expediteur = columns.Text()
    heure_expediteur = columns.Text()
    utilisateur_expediteur = columns.Text()
    adresse_expediteur = columns.Text()
    ville_expediteur = columns.Text()
    code_postale_expediteur = columns.Text()
    departement_expediteur = columns.Text()
    region_expediteur = columns.Text()
    pays_expediteur = columns.Text()
    drapeau_expediteur = columns.Text()

    date_destinataire = columns.Text()
    heure_destinataire = columns.Text()
    utilisateur_destinataire = columns.Text()
    adresse_destinataire = columns.Text()
    ville_destinataire = columns.Text()
    code_postale_destinataire = columns.Text()
    departement_destinataire = columns.Text()
    region_destinataire = columns.Text()
    pays_destinataire = columns.Text()
    drapeau_destinataire = columns.Text()

    poids = columns.Integer()
    superficie = columns.Integer()
    volume = columns.Integer()
    kilometre = columns.Integer()
    hauteur = columns.Integer()
    largeur = columns.Integer()
    longueur = columns.Integer()
    valeur_marchandise = columns.Integer()
    
    categorie = columns.Text()
    type = columns.Text()
    
    nombre_palette = columns.Integer()
    dimension_palette = columns.Text()
    hauteur_palette = columns.Text()

    poids_champ = columns.Text(default='kg')
    superficie_champ = columns.Text(default='m2')
    volume_champ = columns.Text(default='m3')
    kilometre_champ = columns.Text(default='km')
    hauteur = columns.Text(default='m')
    largeur = columns.Text(default='m')
    longueur = columns.Text(default='m')
    valeur_marchandise_champ = columns.Text(default='eur')


    cout = columns.Text()
    prix = columns.Decimal()
    benefice = columns.Text()
    estimation = columns.Text()

    cout_champ = columns.Text()
    prix_champ = columns.Text()
    benefice_champ = columns.Text()
    estimation_champ = columns.Text()

    option =columns.Text()
    personne = columns.Text()
    email_fret = columns.Text()
    telephone_fret = columns.Text()
    messagerie = columns.Text()
    
    valide = columns.Integer()
    certifier = columns.Integer()
    status = columns.Text(default="Brouillon")

    def __str__(self):
        return f'{self.titre}'
    
    class Meta:
        get_pk_field = 'fret_id'
        verbose_name = 'Fret'

    @cached_property
    def url_frontend(self):
        return f"https://wivivi.com{reverse('fret_url', args=[self.url])}"

    @cached_property
    def url_formulaire_frontend(self):
        return f"https://wivivi.com{reverse('fret_formulaire_url', args=[self.fret_id])}"
    
    @cached_property
    def code_postale_ville_expediteur(self):
        return f"{ self.code_postale_expediteur } { self.ville_expediteur.capitalize() }"
    
    @cached_property
    def code_postale_ville_destinataire(self):
        return f"{ self.code_postale_destinataire } { self.ville_destinataire.capitalize() }"

class FavorisModel(DjangoCassandraModel):
    favoris_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur = columns.Text()
    fret_id = columns.Text()
    favoris = columns.Integer()
    date_creation = columns.DateTime(default=datetime.now)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        get_pk_field = 'favoris_id'
        verbose_name = 'Favoris'

class AvisClientModel(DjangoCassandraModel):
    avis_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    description = columns.Text()
    avis = columns.Integer()
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur = columns.Text()
    avis_valide = columns.Integer()
    date_creation = columns.DateTime(default=datetime.now)

    
    def __str__(self):
        return f'{self.description}'
    
    class Meta:
        get_pk_field = 'avis_id'
        verbose_name = 'avis'

class SignalementModel(DjangoCassandraModel):
    signalement_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    description = columns.Text()
    fret_id = columns.Text()
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur = columns.Text()
    signalement_valide = columns.Integer()
    date_creation = columns.DateTime(default=datetime.now)
    
    def __str__(self):
        return f'{self.description}'
    
    class Meta:
        get_pk_field = 'signalement_id'
        verbose_name = 'signalement'


class PropositionModel(DjangoCassandraModel):
    proposition_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    fret_id = columns.Text()
    utilisateur_id = columns.Integer(index=True)
    interlocuteur_id = columns.Integer()
    utilisateur = columns.Text()
    prix = columns.Integer()
    date_creation = columns.DateTime(default=datetime.now)
    condition = columns.Text()
    valide = columns.Integer()
    
    def __str__(self):
        return f'{self.description}'
    
    class Meta:
        get_pk_field = 'propostion_id'
        verbose_name = 'Proposition'