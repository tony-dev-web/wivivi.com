#annonce views
#import requests, uuid, os, pillow_avif, stripe, itertools, datetime
import datetime, time
from django.template.defaultfilters import slugify
from backoffice.models import DepartementModel, PageModel, RegionModel
from annonce.models import FretModel, RechercheFretModel
from django.shortcuts import render
from django.http import HttpResponse  
from backoffice.utils import EmailUtils, LayoutUtils, RechercheUtils, ErreurUtils, DrapeauDesUtils, DrapeauExpUtils, MiseRelationPostUtils, PreconnectUtils, VuesUtils
from django.views import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from utilisateur.models import UtilisateurModel
from django.contrib import messages




class FretFormulaireView(View):
    url_page = '/frets/formulaire/'
    http_method_names = ["get", "post"]
    def get(self,request, lang=None):
        lang = lang or 'fr'
        ui = get_object_or_404(PageModel, page='fret-formulaire')
        response =  HttpResponse(loader.get_template(ui.template).render({'ui':ui,'bodys':LayoutUtils(lang)}, request))
        response['Link'] = f'<https://wivivi.com/frets/formulaire/>;rel="canonical", {PreconnectUtils}'
        response['Content-Language'] = lang
        #response.headers['Cache-Control'] = 'public, max-age=10800' 
        return response

    def post(self,request, lang=None):
        lang = lang or 'fr'

        
        if not request.user.is_authenticated:
            if UtilisateurModel.objects.filter(email=request.POST['email']).exists():
                redirection_succes = "/connexion/suite/"
            else :
                redirection_succes = "/inscription/"

            return HttpResponseRedirect(redirection_succes)

        if request.method != "POST":
            ErreurUtils('erreur-fret-formulaire-post', 0, request.user.id)
            return HttpResponseRedirect(self.url_page)

        if request.POST['categorie'] != None or request.POST['type'] != None:
            messages.info(request, 'Vous devez sélectionner les deux categories')
            return HttpResponseRedirect(self.url_page)
        
        fret1 = FretModel.objects.create(categorie=request.POST['categorie'], type=request.POST['type'], utilisateur_id=request.user.id)
        fret1.save()

        ErreurUtils('fret-formulaire-ok', 1, request.user.id)
        EmailUtils(request, emailing=fret1.email_fret , messaging='nouvelle annonce sur Wivivi', sujeting='Vous venez de posté une nouvelle annonce de fret' ) 
        return HttpResponseRedirect(fret1.url_formulaire_frontend)

class FretFormulaireTypeView(View):
    
    url_page = '/frets/formulaire/'
    http_method_names = ["get", "post"]
    
    def get(self,request, fret_id, lang=None):
        lang = lang or 'fr'
        
        ui = get_object_or_404(FretModel, fret_id=fret_id)
        
        return HttpResponse(loader.get_template( "a3-fret-formulaire-camion.html").render({'ui':ui,  'min_date': str(datetime.datetime.now()), 'max_date':str(datetime.datetime.now() + datetime.timedelta(days=365)), 'bodys':LayoutUtils(lang)}, request))
    
    def post(self,request,fret_id, lang=None):
        lang = lang or 'fr'
        
        if request.method != "POST":
            ErreurUtils('erreur-fret-formulaire-post',0,request.user.id)
            return HttpResponseRedirect(f'{self.url_page}/{fret_id}')

        uti1 = UtilisateurModel.objects.get(utilisateur_id=request.user.id)

        fret1 = FretModel.objects.get(fret_id=fret_id)
        fret1.description = request.POST['description']

        #fret1.date_validation = request.POST['date_validation']
        date_creation = datetime.datetime.strptime(str(fret1.date_creation), '%Y-%m-%d %H:%M:%S.%f')
        fret1.timestamp_creation = int(time.mktime(date_creation.timetuple()))
        
        timestamp_validation = datetime.datetime.strptime(str(request.POST['date_validation']), '%Y-%m-%d')
        fret1.date_validation = str(timestamp_validation.date())
        fret1.timestamp_validation = int(time.mktime(timestamp_validation.timetuple()))

        fret1.utilisateur = uti1.utilisateur
        #heure = request.POST['']
        #stamptime =request.POST['']
        fret1.date_expediteur = str(datetime.datetime.strptime(str(request.POST['date_expediteur']), '%Y-%m-%d').date())
        #fret1.heure_expediteur = request.POST['']
        fret1.utilisateur_expediteur = request.POST['utilisateur_expediteur']
        fret1.adresse_expediteur = request.POST['adresse_expediteur']
        fret1.ville_expediteur = request.POST['ville_expediteur']
        fret1.code_postale_expediteur = request.POST['code_postale_expediteur']
        fret1.departement_expediteur = request.POST['departement_expediteur']
        fret1.pays_expediteur = request.POST['pays_expediteur']
        fret1.drapeau_expediteur = str(DrapeauExpUtils(fret1))

        fret1.date_destinataire = str(datetime.datetime.strptime(str(request.POST['date_destinataire']), '%Y-%m-%d').date())
        fret1.utilisateur_destinataire = request.POST['utilisateur_destinataire']
        fret1.adresse_destinataire = request.POST['adresse_destinataire']
        fret1.ville_destinataire = request.POST['ville_destinataire']
        fret1.code_postale_destinataire = request.POST['code_postale_destinataire']
        fret1.departement_destinataire = request.POST['departement_destinataire']
        fret1.pays_destinataire = request.POST['pays_destinataire']
        fret1.drapeau_destinataire = str(DrapeauDesUtils(fret1))

        fret1.poids = request.POST['poids']
        fret1.kilometre = request.POST['kilometre']
        fret1.valeur_marchandise = request.POST['valeur_marchandise']
        fret1.poids_champ = 'kg'
        fret1.kilometre_champ = 'km'
        fret1.valeur_marchandise_champ = 'eur' 
        
        fret1.email_fret = request.POST['email_fret']
        fret1.telephone_fret = request.POST['telephone_fret']
        
        fret1.url = slugify(f'{fret1.ville_expediteur}-{fret1.ville_destinataire}-{fret1.fret_id}')
        fret1.lang = lang
        fret1.titre =  f'Affretement entre {fret1.ville_expediteur} et {fret1.ville_destinataire}'

        if fret1.type == 'palette':
            fret1.nombre_palette = request.POST['nombre_palette']
            fret1.hauteur_palette = request.POST['hauteur_palette']
            fret1.dimension_palette = request.POST['dimension_palette']
        
        elif fret1.type == 'volume':
            fret1.hauteur = request.POST['hauteur']
            fret1.longueur = request.POST['longueur']
            fret1.largeur = request.POST['largeur']
            fret1.superficie = request.POST['superficie']
            fret1.volume = request.POST['volume']
            fret1.superficie_champ = 'm2'
            fret1.volume_champ = 'm3'
        
        if not RechercheFretModel.objects.filter(fret_id=fret1.fret_id).exists():
            fret2 = RechercheFretModel.objects.create(fret_id=fret1.fret_id)
            fret2.lang = lang
            fret2.ia = list(f'{fret1.ville_expediteur}, {fret1.ville_destinataire}, {fret1.utilisateur_expediteur}')
            fret2.stamptime = int(fret1.timestamp_validation)
            fret2.save()

        if fret1.ville_destinataire != None and fret1.ville_expediteur != None:
            fret1.status = 'publique'
            fret1.valide = 1
            ErreurUtils('fret-formulaire-ok', 1, request.user.id)
            EmailUtils(request, emailing=fret1.email_fret , messaging='nouvelle annonce sur Wivivi', sujeting='Vous venez de posté une nouvelle annonce de fret' )

        fret1.save()
        messages.info(request, 'Annonce de fret soumis avec succes')
         
        return HttpResponseRedirect(fret1.url_formulaire_frontend)

def FretDepartementGet(request, url, lang=None) -> HttpResponse:
    lang = lang or 'fr'
    RechercheUtils(request)

    ui = get_object_or_404(DepartementModel, url=url)
    VuesUtils(request, ui)

    up1 = FretModel.objects.filter(departement_expediteur=ui.departement)[:10]
    up2 = FretModel.objects.filter(departement_destinataire=ui.departement)[:10]
    up3 = DepartementModel.objects.filter(region=ui.region).exclude(url=ui.url)
    up4 = RegionModel.objects.get(region=ui.region)
    up5 = UtilisateurModel.objects.filter(groupe='transporteur', departement=ui.departement,  certifier=1).order_by('ranking_score')[:5]
    
    ui.description = f'{ui.titre}, { ", ".join([xx.titre for xx in up5[:2]]) }, Plateforme de fret mettant en relation les transporteurs en { ui.departement }, professionnels de la logistique en région { ui.region }, industriels et artisans pour faciliter la coopération dans la distribution'
    #ui.description = ui.description or f'Plateforme mettant en relation les transporteurs en { ui.departement }, professionnels de la logistique en région { ui.region }, industriels et artisans pour faciliter la coopération dans la distribution'
    
    response = render(request, "a1-fret-departement.html", context={'ui':ui, 'up1':up1, 'up2':up2, 'up3':up3,'up4':up4, 'up5':up5,'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Link'] = f'<{ui.url_frontend}>;rel="canonical", {PreconnectUtils}'
    response['Content-Language'] = lang
    #response.headers['Cache-Control'] = 'public, max-age=10800' 
    return response

def FretRegionGet(request, url, lang=None) -> HttpResponse:
    lang = lang or 'fr'
    RechercheUtils(request)
    ui = get_object_or_404(RegionModel, url=url)
    VuesUtils(request, ui)
   
    
    #up1 = FretModel.objects.filter(departement_expediteur=ui.departement)[:10]
    #up2 = FretModel.objects.filter(departement_destinataire=ui.departement)[:10]
    up3 = UtilisateurModel.objects.filter(groupe='transporteur', region=ui.region,  certifier=1).order_by('ranking_score')[:5]
    
    #ui.description = ui.description or f'Plateforme mettant en relation les transporteurs en { ui.region }, professionnels de la logistique, industriels et artisans pour faciliter la coopération dans la distribution'
    ui.description = f'{ui.titre}, { ", ".join([xx.titre for xx in up3[:2]]) }, Bourse de fret routier en region { ui.region }'
    
    response = render(request, "a1-fret-region.html", context={'ui':ui,'up3':up3,  'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Link'] = f'<{ui.url_frontend}>;rel="canonical", {PreconnectUtils}'
    response['Content-Language'] = lang
    #response.headers['Cache-Control'] = 'public, max-age=10800' 
    return response



class FretAnnonceView(View):
    http_method_names = ["get", "post"]
    def get(self,request,url, lang=None):
        lang = lang or 'fr'
        RechercheUtils(request)
        ui = get_object_or_404(FretModel, url=url)
        ui.description = ui.description or f'Besoin de relier {ui.ville_expediteur} à { ui.ville_destinataire} pour éviter les retours à vide de votre flote de camion'
        uti = None
        if request.user.is_authenticated:
            uti = UtilisateurModel.objects.get(utilisateur_id=request.user.id)

        response = HttpResponse(loader.get_template( "a1-fret-annonce.html").render({'uti':uti, 'ui':ui, 'bodys':LayoutUtils(lang)}, request))

        response['Link'] = f'<{ui.url_frontend}>;rel="canonical", {PreconnectUtils}'
        response['Content-Language'] = lang
        #response.headers['Cache-Control'] = 'public, max-age=10800' 
        return response
    
    def post(self,request,url, lang=None):
        lang = lang or 'fr'
        
        ui = get_object_or_404(FretModel, url=url)
        #if request.user.is_authenticated:
            #UtilisateurModel.object.get(utilisateur_id=request.user.id)
        
        if request.method != "POST":
            ErreurUtils('erreur-fret-annonce-post', 0, request.user.id)
            return HttpResponseRedirect(ui.url_frontend)
        
        MiseRelationPostUtils(request,ui)

        return HttpResponseRedirect(ui.url_frontend)