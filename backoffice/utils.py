from backoffice.models import RapportModel, MessagerieModel, MiseRelationModel
from utilisateur.models import LayoutModel, UtilisateurModel
from annonce.models import PropositionModel
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import redirect
from django.contrib.auth import authenticate , login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.sessions.exceptions import SessionInterrupted

PreconnectUtils = '<https://wivivi.com/static/assets/css/style.css>; rel="preconnect",<https://wivivi.com/static/assets/js/alpine.min.js>; rel="preconnect"'

def UtilisateurUtils(request):
    if request.user.is_authenticated :
        return UtilisateurModel.objects.get(utilisateur_id=request.user.id)

def EmailUtils(request, emailing, sujeting, messaging):
    with get_connection(host='smtp.protonmail.ch', port=587, username='coucou@wivivi.com', password='QLCC86TXYVRTDUUV', use_tls=True, use_ssl=False) as connection:  
        EmailMessage(sujeting , messaging, 'coucou@wivivi.com' , [ emailing ], connection=connection).send()
    
def LayoutUtils(lang=None):
    return LayoutModel.objects.get(lang=lang)

def RechercheUtils(request):
    r = request.GET.get('r')
    if r:
        return redirect(f'/r/?r={r}')

def ErreurUtils(er1:str, er2:int, er3:int):
    return RapportModel.objects.create( erreur=str(er1), rapport=int(er2), utilisateur_id=int(er3))

def ConnexionSuiteUtils(request):
    formulaire_email = request.POST['email']
    formulaire_motpasse = request.POST['password']
    
    user = authenticate(username=formulaire_email,password=formulaire_motpasse)
    if user is None:
        ErreurUtils('connexion-erreur-authentification', 0, 0)
        messages.info(request, 'Erreur de connexion')
        return redirect('/connexion/')
    else:
        login(request, user)
                
        #uti1 = UtilisateurModel.objects.get(email=formulaire_email)
        #uti1.session_id = request.session.session_key
        #uti1.save()
  
        try:
            request.session.save()
        except:
            raise SessionInterrupted("erreur cookie") from e
        
        #sujet_email= 'Connexion à Wivivi'
        #message_email = 'Connexion effectuer avec succès'
        #EmailUtils(request, emailing=formulaire_email, messaging=message_email, sujeting=sujet_email )  
        ErreurUtils( 'connexion-ok', 1, request.user.id )
        #response.set_cookie('sessionid', request.session.session_key,max_age=1209600, domain='wivivi.com',path='/',secure=True, httponly=True,samesite=None,)
        return HttpResponseRedirect("/compte/")

def AuthentificationUtils(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect('/')

drapeaux = { 'france': '/static/drp/fr.svg',
    'belgique': '/static/drp/be.svg',
    'royaume unie': '/static/drp/uk.svg',
    'allemagne': '/static/drp/de.svg',
    'italie': '/static/drp/it.svg',
    'espagne': '/static/drp/es.svg',
    'pays bas': '/static/drp/ne.svg',
    'portugal': '/static/drp/pr.svg',
    'suisse': '/static/drp/su.svg',
    'autriche': '/static/drp/au.svg',
    'pologne': '/static/drp/pl.svg',
    'roumanie': '/static/drp/ro.svg',
    'slovaquie': '/static/drp/sk.svg',
    'slovenie': '/static/drp/si.svg',
    'croatie': '/static/drp/hr.svg',
    'hongrie': '/static/drp/ho.svg',
    'serbie': '/static/drp/rs.svg',
    'grece': '/static/drp/gr.svg',
    'suede': '/static/drp/se.svg',
    'norvege': '/static/drp/no.svg',
    'bulgarie': '/static/drp/bu.svg',
    'danemark': '/static/drp/dk.svg',
    'finlande': '/static/drp/fi.svg',
    'tchecoslovaquie': '/static/drp/cs.svg',
    'Iirlande': '/static/drp/ir.svg',
    'estonie': '/static/drp/ee.svg',
    'lettonie': '/static/drp/lv.svg',
    'lituanie': '/static/drp/lt.svg',
    'reunion': '/static/drp/re.svg',
    'martinique': '/static/drp/mq.svg'}

def DrapeauDesUtils(fret1):
    return drapeaux.get(fret1.pays_destinataire, None)

def DrapeauExpUtils(fret1):
    return drapeaux.get(fret1.pays_expediteur, None)

def RankingUtils():
    return

def VuesUtils(request, ui) -> None:
    if not request.user_agent.is_bot:
        ui.vues += 1
        return ui.save()
    


def MiseRelationPostUtils(request, ui): 
    if request.user.is_authenticated:
        uti1 = UtilisateurModel.objects.get(utilisateur_id=request.user.id)
        if request.GET.get('proposition', None) :
                proposition_message = request.POST['proposition_message']
                proposition_prix = request.POST['proposition_message']
                PropositionModel.objects.create(utilisateur_id=uti.utilisateur_id, fret_id=ui.fret_id, message=proposition_message, prix=proposition_prix)
                ErreurUtils('fret-annonce-proposition-ok', 1, uti.utilisateur_id)
                
                if uti1.credit <= 1 :
                    uti1.credit -= 1
                    uti1.save()
                    return MiseRelationModel.objects.create(utilisateur_id=uti.utilisateur_id, interlocuteur_id=ui.utilisateur_id, utilisateur=uti.utilisateur)

        else:
                messagerie_message = request.POST['messagerie_message']
                MessagerieModel.objects.create(utilisateur_id_1=request.user.id, message=messagerie_message)
                ErreurUtils('fret-annonce-messagerie-ok', 1, uti.utilisateur_id)
                if uti1.credit <= 1 :
                    uti1.credit -= 1
                    uti1.save()
                
                    return MiseRelationModel.objects.create(utilisateur_id=uti.utilisateur_id, interlocuteur_id=ui.utilisateur_id, utilisateur=uti.utilisateur)

#attente
region_liste = { 'sarthe': 'Pays de Loire',
    'mayenne': 'Pays de Loire',
    'maine et loire': 'Pays de Loire',
    'loire atlantique': 'Pays de Loire',
    'morbihan': 'Bretagne',
    'finistere': 'Bretagne',
    'cote d armor': 'Bretagne',
    'ille et vilaine': 'Bretagne',
    'manche': 'Normandie',
    'calvados': 'Normandie',
    'eure': 'Normandie',
    'seine maritime': 'Normandie',
    'orne': 'Normandie',
    'slovenie': '/static/drp/si.svg',
    'croatie': '/static/drp/hr.svg',
    'hongrie': '/static/drp/ho.svg',
    'serbie': '/static/drp/rs.svg',
    'grece': '/static/drp/gr.svg',
    'suede': '/static/drp/se.svg',
    'norvege': '/static/drp/no.svg',
    'bulgarie': '/static/drp/bu.svg',
    'danemark': '/static/drp/dk.svg',
    'finlande': '/static/drp/fi.svg',
    'tchecoslovaquie': '/static/drp/cs.svg',
    'Iirlande': '/static/drp/ir.svg',
    'estonie': '/static/drp/ee.svg',
    'lettonie': '/static/drp/lv.svg',
    'lituanie': '/static/drp/lt.svg',
    'reunion': '/static/drp/re.svg',
    'martinique': '/static/drp/mq.svg'}


pays_liste = { 'france': 'fr'}
               