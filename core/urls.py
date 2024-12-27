
from django.urls import path
from backoffice.views import IndexGet, RechercheGet, ContactView, CompteGet, PaiementView, PaiementReponseGet, PageGet, MessagerieView, SitemapGet, RobotGet
from utilisateur.views import ConnexionView, UtilisateurFormulaireView, UtilisateurView, LigneTransportView
from annonce.views import FretDepartementGet, FretRegionGet,  FretAnnonceView, FretFormulaireView, FretFormulaireTypeView
from core.decorators import login_connect, login_non_connect

urlpatterns = [
    path('', IndexGet),
    path('robots.txt', RobotGet),
    path('sitemap-web.xml', SitemapGet),
    path('utilisateur/formulaire/',login_connect(UtilisateurFormulaireView.as_view())),
    path('utilisateur/ligne/', LigneTransportView.as_view()),
    path('frets/formulaire/', FretFormulaireView.as_view()),
    path('frets/formulaire/<str:fret_id>',login_connect(FretFormulaireTypeView.as_view()), name='fret_formulaire_url'),
    path('connexion/', login_non_connect(ConnexionView.as_view())),
    path('mot-passe/', MotdepasseView.as_view()),
    path('contact/', ContactView.as_view()),
    path('compte/', login_connect(CompteGet)),
    path('messagerie/', login_connect(MessagerieView.as_view())),
    path('frets/<str:url>', FretAnnonceView.as_view(), name='fret_url'),
    #path('msessagerie/<str:utilisateur_id_groupe>', MessagerieView.as_view()),
    path('<str:url_n1>/', PageGet, name='page_url'),
    path('<str:groupe>/<str:url>', UtilisateurView.as_view(), name='utilisateur_url'),
    path('<str:lang>/<str:url>/', FretDepartementGet, name="departement_url"),
    path('<str:lang>/region/<str:url>/', FretRegionGet, name="region_url"),
    path('r/', RechercheGet)]
