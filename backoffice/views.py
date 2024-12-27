#view backoffice
import stripe
from backoffice.models import ContactModel, PageModel, PaiementModel, MessageModel, MessagerieModel, DepartementModel, RegionModel
from utilisateur.models import UtilisateurModel
from annonce.models import RechercheFretModel, FretModel
from backoffice.utils import EmailUtils, LayoutUtils, RechercheUtils, ErreurUtils, PreconnectUtils
from django.shortcuts import get_object_or_404,redirect, render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
#from utilisateur.views import connexion 
from django.template import loader
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib import messages
from itertools import chain

#def autocompletesearch(request):
    #qs = request.GET.get('term','')
    #aa = sorted(chain(AnnonceModel.obj.autocomplete(qs), VehiculeModel.obj.autocomplete(qs), ProductModel.obj.autocomplete(qs)), key=lambda instance: instance.id, reverse=True)
   # return HttpResponse(json.dumps([s.title for s in aa ]), 'application/json')
   
#from django.core.cache import cache
#from django.views.decorators.cache import cache_page


#@cache_page(60 * 15)
def IndexGet(request,lang=None) -> HttpResponse:
    lang = lang or 'fr'
    url_page = 'https://wivivi.com/'
    RechercheUtils(request)
    
    #cache_key = f'index_get_{request.user.is_authenticated}'
    #ui = cache.get(cache_key)
    #if ui is None:
    ui = get_object_or_404(PageModel, page='europe')
    #cache.set(cache_key, ui, 60 * 15) # Cache l'objet pendant 15 minutes

    if any(key in request.GET for key in ['ref', 'trk']):
        return HttpResponseRedirect(url_page)

    response = render(request, ui.template , context={'ui':ui, 'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Link'] = f'<{url_page}>;rel="canonical", {PreconnectUtils}'
    response['Content-Language'] = lang
    #response.headers['Cache-Control'] = 'public, max-age=10800' 
    return response


def CompteGet(request,lang=None) -> HttpResponse:
    lang = lang or 'fr'
    
    ui = get_object_or_404(UtilisateurModel, utilisateur_id=request.user.id, valide=1 )
    up1 = MessagerieModel.objects.filter(utilisateur_id=request.user.id)
    up2 = FretModel.objects.filter(utilisateur_id=request.user.id)
    up3 = ContactModel.objects.filter(utilisateur_id=request.user.id)
    up4 = PaiementModel.objects.filter(utilisateur_id=request.user.id)

    response = render(request, "a3-compte.html", context={'up1':up1, 'up2':up2, 'up3':up3, 'up4':up4, 'ui':ui, 'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Content-Language'] = lang
    #response.headers['Cache-Control'] = 'public, max-age=10800' 
    return response

def PageGet(request, url_n1, lang=None) -> HttpResponse:
    lang = lang or 'fr'
    RechercheUtils(request)
    ui = get_object_or_404(PageModel, url_n1=url_n1)
    
    up1 = None
    if url_n1 in ['transporteur', 'professionnel']:
        up1 = UtilisateurModel.objects.filter(groupe=ui.groupe, valide=1, certifier=1).order_by('-ranking_score')
    elif url_n1 in ['frets']:
        up1 = FretModel.objects.filter(valide=1).order_by()[:10]
    elif url_n1 in ['fr']:
        up1 = RegionModel.objects.filter(lang=lang)
    
    response = render(request, ui.template , context={'up1':up1, 'ui':ui, 'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Link'] = f'<{ui.url_frontend}>;rel="canonical", {PreconnectUtils}'
    response['Content-Language'] = lang 
    return response

def RechercheGet(request,lang=None) -> HttpResponse:
    lang = lang or 'fr'
    ui = get_object_or_404(PageModel, page='recherche')
    rr = request.GET.get('r','')
    up11 = RechercheFretModel.objects.filter(Q(ia_expediteur__search=rr) | Q(ia_expediteur__icontains=rr)).values_list('recherche_fret_id',flat=True)[:10]
    up1 = FretModel.objects.filter(fret_id__in=list(up11)).order_by('-stamptime')
    up22 = RechercheFretModel.objects.filter(Q(ia_destinataire__search=rr) | Q(ia_destinataire__icontains=rr)).values_list('recherche_fret_id',flat=True)[:10]
    up2 =  FretModel.objects.filter(fret_id__in=list(up22)).order_by('-stamptime')

    response = render(request, ui.template, context={'ui':ui, 'r':rr, 'up1':up1, 'up2':up2, 'bodys':LayoutUtils(lang)}, content_type='text/html')
    response['Link'] = PreconnectUtils
    response['Content-Language'] = lang
    #response.headers['Cache-Control'] = 'public, max-age=10800' 
    return response


class ContactView(View):
    url_page = '/contact/'
    http_method_names = ["get", "post"]
    def get(self,request, lang=None):
        lang = lang or 'fr'
        ui = get_object_or_404(PageModel, page='contact')
        response =  HttpResponse(loader.get_template(ui.template).render({'ui':ui, 'bodys':LayoutUtils(lang)}, request))
        response['Link'] = f'<https://wivivi.com{self.url_page}>;rel="canonical", {PreconnectUtils}'
        response['Content-Language'] = lang
        return response 

    def post(self, request, lang=None):
        lang = lang or 'fr'
        
        if request.method != "POST" or not request.POST['sujet'] or not request.POST['question']:
            return HttpResponseRedirect(self.url_page)
    
        contact1 = ContactModel.objects.create(email=request.POST['email'])
        contact1.sujet = request.POST['sujet']
        contact1.question = request.POST['question']
        contact1.telephone = request.Post['telephone']
        contact1.telephone = request.Post['connu']
        contact1.save()
        
        sujet_email = 'Question à Wivivi'
        message_email = 'Demande de contact effectuer avec succès, réponse sous 24 heures'
        EmailUtils(request, emailing=contact1.email, messaging=message_email, sujeting=sujet_email ) 
        ErreurUtils('contact-formulaire-ok', 1, request.user.id)
        messages.info(request, message_email)
        return HttpResponseRedirect(self.url_page)

class MessagerieView(View):
    
    http_method_names = ["get", "post"]
    def get(self,request, lang=None):
        lang = lang or 'fr'

        ui =  get_object_or_404(UtilisateurModel, utilisateur_id=request.user.id )
        up1 = MessagerieModel.objects.filter(utilisateur_id=ui.utilisateur_id)
        
        try:
            up2 = MessagerieModel.objects.filter(interlocuteur_id=up1.interlocuteur_id) or None
        except : 
            up2 = None

        return HttpResponse(loader.get_template( "a3-messagerie.html").render({'ui':ui, 'up1':up1, 'up2': up2,'bodys':LayoutUtils(lang)}, request))
        
    def post(self, request, lang=None):
        lang = lang or 'fr'
        
        if request.method != "POST" :
            ErreurUtils('erreur-message-post', 0, request.user.id)
            return HttpResponseRedirect('/compte/')

        ui = MessagerieModel.objects.get()

        message1 = MessageModel.objects.create(message=request.POST['message'])
        message1.utilisateur_id_groupe = f'{ui.utilisateur_id }-{ ui.interlocuteur_id}'
        message1.save()
        
        #sujet_email = 'Question à Wivivi'
        #message_email = 'Demande de contact effectuer avec succès, réponse sous 24 heures'
        #EmailUtils(request, emailing=contact1.email, messaging=message_email, sujeting=sujet_email ) 
        #ErreurUtils('contact-formulaire-ok', 1, request.user.id)
        #messages.info(request, 'Demande de contact effectuer avec succès, réponse sous 24 heures')
        return HttpResponseRedirect(f'/mmessagerie/')

def SitemapGet(request):
    up1 = list(chain(UtilisateurModel.objects.filter(certifier=1, groupe__in=['transporteur', 'commissionnaire', 'professionnel']), RegionModel.objects.filter(),DepartementModel.objects.filter(), PageModel.objects.filter(noindex=0), FretModel.objects.filter(valide=1)))
    return render(request, "sitemap-web.xml",{'up1':up1}, content_type='text/xml')

def RobotGet(request):
    return render(request, "robots.txt", content_type='text/plain')