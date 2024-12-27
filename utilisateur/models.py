from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from datetime import datetime
import uuid
from django.db import models
from django.utils.functional import cached_property
from django.urls.base import reverse

#LigneTransportModel lyon -> paris

class LayoutModel(models.Model):
    layout_id = models.AutoField(primary_key=True)
    layout_nom = models.CharField(max_length=1024,null=True, blank=True)
    layout_domaine = models.CharField(max_length=1024,null=True, blank=True)
    layout_site_web = models.CharField(max_length=1024,null=True, blank=True)
    layout_site_web_url = models.CharField(max_length=1024,null=True, blank=True)
    layout_titre = models.CharField(max_length=1024,null=True, blank=True)
    layout_footer = models.CharField(max_length=1024,null=True, blank=True)
    description = models.TextField(max_length=1024,null=True, blank=True)
    image = models.CharField(max_length=1024,null=True, blank=True)
    lang = models.CharField(max_length=1024,null=True, blank=True)
    menu = models.CharField(max_length=32, null=True, blank=True)
    aide = models.CharField(max_length=32,null=True, blank=True)
    question = models.CharField(max_length=32,null=True, blank=True)
    depot_annonce = models.CharField(max_length=32,null=True, blank=True)
    annonce = models.CharField(max_length=32,null=True, blank=True)
    pays = models.CharField(max_length=32,null=True, blank=True)
    departement = models.CharField(max_length=32,null=True, blank=True)
    usage = models.CharField(max_length=32,null=True, blank=True)
    expediteur = models.CharField(max_length=32,null=True, blank=True)
    aucun_resultat = models.CharField(max_length=32,null=True, blank=True)
    aucun_resultat_pour = models.CharField(max_length=32,null=True, blank=True)
    resultat = models.CharField(max_length=32,null=True, blank=True)
    contact_expediteur = models.CharField(max_length=32,null=True, blank=True)
    contact_destinataire = models.CharField(max_length=32,null=True, blank=True)
    contact_professionnel = models.CharField(max_length=32,null=True, blank=True)
    contact_transporteur = models.CharField(max_length=32,null=True, blank=True)
    destinataire = models.CharField(max_length=32,null=True, blank=True)
    affretement = models.CharField(max_length=32,null=True, blank=True)
    modifier = models.CharField(max_length=32,null=True, blank=True)
    voir = models.CharField(max_length=32,null=True, blank=True)
    utilisateur = models.CharField(max_length=32,null=True, blank=True)
    utilisateur_url = models.CharField(max_length=32,null=True, blank=True)
    utilisateur_formulaire_url = models.CharField(max_length=32,null=True, blank=True)
    professionnel = models.CharField(max_length=32,null=True, blank=True)
    professionnel_url = models.CharField(max_length=32,null=True, blank=True)
    recherche = models.CharField(max_length=32,null=True, blank=True)
    recherche_fret = models.CharField(max_length=32,null=True, blank=True)
    recherche_url = models.CharField(max_length=32,null=True, blank=True)
    commissionnaire = models.CharField(max_length=32,null=True, blank=True)
    commissionnaire_url = models.CharField(max_length=32,null=True, blank=True)
    transporteur = models.CharField(max_length=32,null=True, blank=True)
    transporteur_url = models.CharField(max_length=32,null=True, blank=True)
    compte = models.CharField(max_length=32,null=True, blank=True)
    compte_url = models.CharField(max_length=32,null=True, blank=True)
    compte_urlo = models.CharField(max_length=32,null=True, blank=True)
    messagerie = models.CharField(max_length=32,null=True, blank=True)
    messagerie_url = models.CharField(max_length=32,null=True, blank=True)
    messagerie_urlo = models.CharField(max_length=32,null=True, blank=True)
    deconnexion = models.CharField(max_length=32,null=True, blank=True)
    deconnexion_url = models.CharField(max_length=32,null=True, blank=True)
    modifier_profil = models.CharField(max_length=1024,null=True, blank=True)
    profil = models.CharField(max_length=32,null=True, blank=True)
    profil_url = models.CharField(max_length=32,null=True, blank=True)
    mentions = models.CharField(max_length=32,null=True, blank=True)
    mentions_url = models.CharField(max_length=32,null=True, blank=True)
    connexion = models.CharField(max_length=32,null=True, blank=True)
    connexion_url = models.CharField(max_length=1024,null=True, blank=True)
    connexion_urlo = models.CharField(max_length=1024,null=True, blank=True)
    inscription = models.CharField(max_length=24,null=True, blank=True)
    inscription_url = models.CharField(max_length=1024,null=True, blank=True)
    inscription_urlo = models.CharField(max_length=1024,null=True, blank=True)
    paiement = models.CharField(max_length=32,null=True, blank=True)
    paiement_url = models.CharField(max_length=1024,null=True, blank=True)
    paiement_urlo = models.CharField(max_length=1024,null=True, blank=True)
    contact = models.CharField(max_length=24,null=True, blank=True)
    contact_url = models.CharField(max_length=1024,null=True, blank=True)
    contact_urlo = models.CharField(max_length=1024,null=True, blank=True)
    fret = models.CharField(max_length=24,null=True, blank=True)
    fret_url = models.CharField(max_length=1024,null=True, blank=True)
    fret_urlo = models.CharField(max_length=1024,null=True, blank=True)
    fret_fromulaire = models.CharField(max_length=24,null=True, blank=True)
    fret_formulaire_url = models.CharField(max_length=1024,null=True, blank=True)
    fret_formulaire_urlo = models.CharField(max_length=1024,null=True, blank=True)
    particulier = models.CharField(max_length=24,null=True, blank=True)
    accueil = models.CharField(max_length=24,null=True, blank=True)
    conducteur = models.CharField(max_length=24,null=True, blank=True)
    classement = models.CharField(max_length=24,null=True, blank=True)
    transport = models.CharField(max_length=24,null=True, blank=True)
    livraison = models.CharField(max_length=24,null=True, blank=True)
    colis = models.CharField(max_length=24,null=True, blank=True)
    ligne_reguliere = models.CharField(max_length=24,null=True, blank=True)
    ligne = models.CharField(max_length=24,null=True, blank=True)
    ajouter_ligne = models.CharField(max_length=24,null=True, blank=True)
    ligne_formulaire_url = models.CharField(max_length=24,null=True, blank=True)
    vues = models.CharField(max_length=24,null=True, blank=True)

    brea1_index = models.CharField(max_length=24,null=True, blank=True)
    brea2_pays = models.CharField(max_length=24,null=True, blank=True)
    brea2_compte = models.CharField(max_length=24,null=True, blank=True)

    
    def __str__(self):
        return self.lang

    class Meta:
        verbose_name = 'layout'
        indexes = [models.Index(fields=['lang'], name='utilisateur_lang_8bd61a_idx')]



class LigneTransportModel(DjangoCassandraModel):
    ligne_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    utilisateur_id = columns.Integer(index=True)
    ville_depart = columns.Text()
    pays_depart = columns.Text()
    ville_arriver = columns.Text()
    pays_arriver = columns.Text()
    categorie = columns.Text()
    lang = columns.Text()

    def __str__(self):
        return f'{self.utilisateur_id} {self.ville_depart} {self.ville_arriver}'
    
    class Meta:
        #get_pk_field = 'utilisateur_id'
        verbose_name = 'Ligne'



class UtilisateurModel(DjangoCassandraModel):
    utilisateur_id = columns.Integer(primary_key=True)
    url = columns.Text()
    utilisateur = columns.Text()
    vues = columns.Integer(default=0)
    dirigeant = columns.Text()
    lang = columns.Text()
    titre = columns.Text()
    titre_ville = columns.Text()
    description = columns.Text()
    groupe = columns.Text()
    categorie = columns.Text()
    #date_creation = columns.DateTime(default=datetime.now)
    date = columns.Text(default=datetime.now().strftime("%d-%m-%Y %H:%M"))
    valide = columns.Integer(default=1)
    certifier = columns.Integer(default=0)
    session = columns.Text()
    email = columns.Text()
    credit = columns.Integer(default=0)
    adresse  = columns.Text()
    ville = columns.Text()
    departement = columns.Text()
    region = columns.Text()
    pays = columns.Text()
    code_postale = columns.Text()
    site_web = columns.Text()
    domaine = columns.Text()
    telephone = columns.Text()
    logo = columns.Text()
    kbis = columns.Text()
    siren = columns.Text()
    annee = columns.Integer(default=0)
    ranking = columns.Integer(default=0)
    ranking_score = columns.Integer(default=0)
    superficie = columns.Integer(default=0)
    nombre_camion = columns.Integer(default=0)
    nombre_employer = columns.Integer(default=0)

    def __str__(self):
        return self.utilisateur
    
    class Meta:
        get_pk_field = 'utilisateur_id'
        verbose_name = 'Utilisateur'
    
    @cached_property
    def url_frontend(self):
        return f"https://wivivi.com{reverse('utilisateur_url', args=[self.groupe, self.url])}"

    @cached_property
    def titre2(self):
        return f"{ self.titre } { self.ville.capitalize() }"
    
    @cached_property
    def code_postale_ville(self):
        return f"{ self.code_postale } { self.ville.capitalize() }"
        
class PreferenceRechercheModel(DjangoCassandraModel):
    preference_recherche_id = columns.Text(primary_key=True, default=uuid.uuid4().hex)
    utilisateur_id = columns.Integer(index=True)
    departement = columns.Text()
    pays = columns.Text()
    option = columns.Text()
    categorie_camion = columns.Text()
    groupe = columns.Text()
    date_creation = columns.DateTime(default=datetime.now)
    utilisateur_session = columns.Text()

    def __str__(self):
        return self.nom
    
    class Meta:
        get_pk_field = 'utilisateur_id'
        verbose_name = 'Utilisateur'


class AdresseModel(DjangoCassandraModel):
    adresse_id = columns.Integer(primary_key=True)
    utilisateur = columns.Text()
    email = columns.Text()
    telephone = columns.Text()
    site_web = columns.Text()
    domaine = columns.Text()
    adresse  = columns.Text()
    ville = columns.Text()
    code_postale = columns.Text()
    logo = columns.Text()
    siren = columns.Text()
    
    def __str__(self):
        return self.utilisateur
    
    class Meta:
        get_pk_field = 'adresse_id'
        verbose_name = 'Adresse'

class EntrepotModel(DjangoCassandraModel):
    entrepot_id = columns.Integer(primary_key=True)
    utilisateur_id = columns.Integer(index=True)
    utilisateur = columns.Text()
    titre = columns.Text()
    description = columns.Text()
    email = columns.Text()
    telephone = columns.Text()
    adresse  = columns.Text()
    ville = columns.Text()
    code_postale = columns.Text()
    departement = columns.Text()
    region = columns.Text()
    pays = columns.Text()
    contact = columns.Text()
    siren = columns.Text()
    superficie = columns.Integer(default=0)

    
    def __str__(self):
        return f'{self.utilisateur} {self.ville}'
    
    class Meta:
        get_pk_field = 'entrepot_id'
        verbose_name = 'entrepot'