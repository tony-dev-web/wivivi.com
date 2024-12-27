# utilisateur view
import uuid, os
from utilisateur.models import UtilisateurModel, AdresseModel, LigneTransportModel
from backoffice.models import PageModel
from django.shortcuts import get_object_or_404,redirect, render
from django.views import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from backoffice.utils import EmailUtils, LayoutUtils, RechercheUtils, ErreurUtils,ConnexionSuiteUtils, MiseRelationPostUtils, PreconnectUtils, VuesUtils
from urllib.parse import urlparse
from django import forms

class ConnexionView(View):
    url_page = '/connexion/'
    url_page_ok = '/compte/'

    http_method_names = ["get", "post"]
    def get(self,request, lang=None):
        lang = lang or 'fr'
        ui = get_object_or_404(PageModel, page='connexion')

        response = HttpResponse(loader.get_template(ui.template).render({'ui':ui, 'bodys':LayoutUtils(lang)}, request))
        response['Link'] = f'<https://wivivi.com{self.url_page}>;rel="canonical", {PreconnectUtils}'
        response['Content-Language'] = lang
        #response.headers['Cache-Control'] = 'public, max-age=10800' 
        return response
    
    def post(self,request, lang=None):
        if request.method != "POST":
            ErreurUtils('connexion-erreur-post', 0, 0)
            return HttpResponseRedirect(self.url_page)

        if UtilisateurModel.objects.filter(email=request.POST['email']).exists():
            redirection_succes = f"/connexion/suite/?email={request.POST['email']}"
        else :
            redirection_succes = f"/inscription/?email={request.POST['email']}"

        return HttpResponseRedirect(redirection_succes)
        
class UtilisateurView(View):
    http_method_names = ["get", "post"]
    
    def get(self, request, groupe,  url, lang=None):
        lang = lang or 'fr'
        RechercheUtils(request)
        ui = get_object_or_404(UtilisateurModel, groupe=groupe, url=url, certifier=1, valide=1) 
        VuesUtils(request, ui)
        rank = int(UtilisateurModel.objects.filter(groupe=ui.groupe, ranking_score__gt=int(ui.ranking_score)).order_by('-ranking_score').count()) + 1
        up1 = LigneTransportModel.objects.filter(utilisateur_id=ui.utilisateur_id)
        
        uti = None
        if request.user.is_authenticated:
            uti = UtilisateurModel.objects.get(utilisateur_id=request.user.id)
            
        response = render(request, "a1-utilisateur-profil.html", context={'uti':uti, 'ui':ui,'up1':up1, 'rank':rank, 'bodys':LayoutUtils(lang)}, content_type='text/html')
        response['Link'] = f'<{ui.url_frontend}>;rel="canonical", {PreconnectUtils}'
        response['Content-Language'] = lang
        #response.headers['Cache-Control'] = 'public, max-age=10800' 
        return response
    
    def post(self,request,groupe, url, lang=None):
        lang = lang or 'fr'
        ui = get_object_or_404(UtilisateurModel, groupe=groupe, url=url, certifier=1,  valide=1)
        
        #if request.user.is_authenticated:
            #UtilisateurModel.object.get(utilisateur_id=request.user.id)
        
        if request.method != "POST":
            ErreurUtils('erreur-fret-annonce-post', 0, request.user.id)
            return HttpResponseRedirect(ui.url_frontend)
        
        MiseRelationPostUtils(request,ui)
        return HttpResponseRedirect(ui.url_frontend)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class UtilisateurFormulaireView(View):
    url_page = '/utilisateur/formulaire/'
    http_method_names = ["get", "post"]
    def get(self,request, lang=None):
        lang = lang or 'fr'
        
        if not request.user.is_authenticated :
            return redirect('/')
        
        ui = get_object_or_404(UtilisateurModel, utilisateur_id=request.user.id)
        page1 = PageModel.objects.get(page='utilisateur-formulaire')
        
        response = HttpResponse(loader.get_template(page1.template).render({'page':page1 ,'ui':ui , 'bodys':LayoutUtils(lang)}, request))
        response['Link'] = PreconnectUtils
        response['Content-Language'] = lang
        return response
    
    
    def post(self,request, lang=None):
        lang = lang or 'fr'
        
        form = UploadFileForm(request.POST, request.FILES)
        if request.method != "POST":
            ErreurUtils('erreur-utilisateur-formulaire-post', 0, request.user.id)
            return HttpResponseRedirect(self.url_page)
        
        tra1 = UtilisateurModel.objects.get(utilisateur_id=request.user.id)
        tra1.description = request.POST['description']
        tra1.dirigeant = request.POST['dirigeant']
        tra1.lang = lang
        tra1.titre = tra1.utilisateur
        tra1.superficie = request.POST['superficie']
        tra1.nombre_employer = int(request.POST['nombre_employer'])
        
        if request.POST['siren']:
            tra1.siren = request.POST['siren'][:9]
        
        tra1.adresse  = request.POST['adresse'].lower()
        tra1.ville = request.POST['ville'].lower()
        tra1.code_postale = request.POST['code_postale']
        tra1.departement = request.POST['departement'].lower()
        
        if request.POST['site_web']:
            tra1.site_web = request.POST['site_web']
            tra1.domaine = urlparse(str(tra1.site_web)).netloc
        
        if request.POST['telephone']:
            tra1.telephone = int(request.POST['telephone'])
        
        tra1.annee = int(request.POST['annee_creation'])

        tra1.url = slugify(f'{tra1.utilisateur}-{tra1.ville}-{tra1.utilisateur_id}')
        #ranking = 
        

        if form.is_valid():
            if request.FILES['logo']:
                gg1 = f'img/{ tra1.groupe }/logo-{tra1.url}'
                os.makedirs(gg1, exist_ok=True) 
                #tra1.profil_image  = f'/{gg1}/{tra1.profil_slug}.avif'
                tra1.logo  = f'/{gg1}/{tra1.url}-{str(uuid.uuid4().hex)}.avif'
                gg3 = f'.{tra1.logo }'
                with open(gg3 ,'wb+') as ff:
                    ff.write(request.FILES['logo'].read())
                    ff.close()
            
            if request.FILES['kbis']:
                gg2 = f'img/{ tra1.groupe }/kbis-{tra1.url}'
                os.makedirs(gg2, exist_ok=True) 
                #tra1.profil_image  = f'/{gg1}/{tra1.profil_slug}.avif'
                tra1.kbis  = f'/{gg2}/{tra1.url}-{str(uuid.uuid4().hex)}.avif'
                gg4 = f'.{tra1.kbis }'
                with open(gg4 ,'wb+') as ff:
                    ff.write(request.FILES['kbis'].read())
                    ff.close()

            #image_exif = Image.open(gg3).getexif()
            #for tag, value in zip([33432,42039], ['Wivivi','Copyright 2024 Wivivi']):
               # image_exif[tag] = value

            #ImageOps.exif_transpose(Image.open(gg3)).rotate(0, fillcolor=(0, 0, 0), expand=True).resize((130,130), Image.Resampling.LANCZOS).save(gg3, format="AVIF", optimize=True, quality=85, exif=image_exif)
        
        tra1.ranking_score = int(tra1.nombre_employer)
        if request.POST['groupe'] == 'transporteur':
            tra1.nombre_camion = int(request.POST['nombre_camion'])
            tra1.ranking_score = int(tra1.nombre_employer) + int(tra1.nombre_camion)

        tra1.save()

        if AdresseModel.objects.filter(utilisateur=tra1.utilisateur).exists():
            adr1 = AdresseModel.objects.create(utilisateur=tra1.utilisateur)
            adr1.adresse  = tra1.adresse
            adr1.ville = tra1.ville
            adr1.code_postale = tra1.code_postale
            adr1.telephone = tra1.telephone
            adr1.email = tra1.email
            adr1.save()

        ErreurUtils('utilisateur-formulaire-ok', 1, request.user.id)
        messages.info(request,'Profil mise à jour avec succès')
        return HttpResponseRedirect(self.url_page)



class LigneTransportView(View):
    url_page = '/utilisateur/ligne/'
    http_method_names = ["get", "post"]
    
    def get(self,request, lang=None):
        lang = lang or 'fr'
        
        if not request.user.is_authenticated :
            return redirect('/')

        ui = get_object_or_404(PageModel, page='ligne-formulaire')
        
        response = HttpResponse(loader.get_template(ui.template).render({'ui':ui , 'bodys':LayoutUtils(lang)}, request))
        response['Link'] = PreconnectUtils
        response['Content-Language'] = lang
        return response
    
    
    def post(self,request, lang=None):
        lang = lang or 'fr'
        
        if request.method != "POST":
            ErreurUtils('erreur-ligne-post', 0, request.user.id)
            return HttpResponseRedirect(self.url_page)
        
        lign1 = LigneTransportModel.objects.create(ligne_id=uuid.uuid4().hex , utilisateur_id=request.user.id, ville_depart=request.POST['ville_depart'], ville_arriver=request.POST['ville_arriver'])
        lign1.categorie = request.POST['categorie']
        lign1.pays_depart = request.POST['pays_depart']
        lign1.pays_arriver = request.POST['pays_arriver']
        lign1.lang = lang
        lign1.save()

        ErreurUtils('utilisateur-ligne-ok', 1, request.user.id)
        messages.info(request,'Ligne mise à jour avec succès')
        return HttpResponseRedirect(self.url_page)
