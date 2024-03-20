from django.shortcuts import render, redirect # pour une redirection ou affichage du html
from django.contrib.auth import authenticate, login, logout # connecter et déconnecter
from django.contrib import messages # pour afficher des messages d'erreur ou success
from custom_user.models import User # tables des utilisateurs
from django.contrib.auth.forms import UserCreationForm # pour créer un formulaire dynamiquement
from .forms import SignUpForm, temoignageForm, ContactForm # on importe notre formulaire
from django import forms # forms permet de valider des formulaires django
from django.contrib.auth.decorators import login_required
from .models import TemoignesModel
from django.template import loader
from django.core.mail import send_mail # To send mails
from django.shortcuts import get_object_or_404

from django.db import transaction
from functools import partial
# vue pour la page d'accueil
def index(request):
    context = {}
    return render(request, "index.html", context)

# vue pour la page de contact
def contact(request):
    formulaire = ContactForm()
    if request.method == "POST": 
        formulaire = ContactForm(request.POST)
        if formulaire.is_valid(): 
            subject = formulaire.cleaned_data["subject"]
            message = formulaire.cleaned_data["message"]
            sender = formulaire.cleaned_data["sender"]
            name = formulaire.cleaned_data["name"]
            recipients = ["for.unicaen@gmail.com"]
            html_message = loader.render_to_string(
                'email.html',
                {
                    'email'  : sender,
                    'subject': subject,
                    'message': message,
                    'name'    : name
                }
            )
            send_mail(subject, message, None, recipients,fail_silently=True,html_message=html_message)
            messages.success(request, "Votre mail a été bien envoyé !")
            return redirect("contact")
        else:
            messages.error(request, "Veuillez bien remplir le formulaire !")
            return render(request, "contact.html", {"form": formulaire})
    return render(request, "contact.html", {"form": formulaire})

# vue pour la page des témoignages de la victime
@login_required
def temoignages(request):
    current_user = request.user #on récupère l'user courrant
    listeTemoignages = TemoignesModel.objects.filter(victime_id=current_user.id)#on récupère les témoignages de cette personne
    return render(request, "temoignages.html", {'temoignage_data':listeTemoignages})#on fait la page en lui envoyant la liste des temoignages

@login_required
def suppressionDeTemoignage(request, id):
    obj = get_object_or_404(TemoignesModel,id=id)
    obj.delete()
    messages.success(request, "Votre témoignage a été supprimé !")
    return redirect("témoignages")

def envoieDeMailAuxVictime(nomAgresseur):
    # victime__email est la même chose que victime.email 
    victimes = TemoignesModel.objects.filter(agresseur=nomAgresseur).values_list("victime__email", flat=True)
    if len(victimes) >= 2 :
        victimes = set(victimes)
        subject = "Mail envoyé à toutes les victimes"
        html_message = loader.render_to_string(
            'emailTemoins.html',
            { "victimes" : victimes }
        )
        send_mail(subject, "message", None, list(victimes),fail_silently=True,html_message=html_message)

# vue pour le formulaire de témoignage
@login_required
def temoigner(request):
    formulaire = temoignageForm()
    if request.method == "POST": 
        formulaire = temoignageForm(request.POST)
        if formulaire.is_valid(): 
            listing = formulaire.save(commit=False) # n'enregistre pas encore dans la base de données
            listing.victime = request.user
            listing.save()
            #print(listing.agresseur)
            transaction.on_commit(partial(envoieDeMailAuxVictime, nomAgresseur=listing.agresseur))
            messages.success(request, "Votre témoin est bien enregistré")
            return redirect("témoigner")
        else:
            messages.error(request, "Veuillez bien remplir le formulaire !")
            return render(request, "temoigner.html", {"form": formulaire})
    return render(request, "temoigner.html", {"form": formulaire})

# Vue pour la page d'inscription
def inscription(request):
    formulaire = SignUpForm() # on crée un formulaire django vide
    if request.method == "POST": # si l'utlisateur viens de soumettre le formulaire
        formulaire = SignUpForm(request.POST) # on recopier les données du formulaire pour créer un fromulaire django
        if formulaire.is_valid(): # si le formulaire est valide
            formulaire.save() # on enregistre les données dans la base de données
            email = formulaire.cleaned_data['email'] # on recupère l'identifiant
            password = formulaire.cleaned_data['password1'] # on recupère le modt de passe
            # on connecte l'utilisateur
            user = authenticate(email=email, password=password)
            login(request, user=user)
            messages.success(request, "Votre compte viens d'être créé")
            return redirect('index')
        else:
            messages.error(request, "Veuillez bien remplir le formulaire !")
            return render(request, "inscription.html", context={'form' : formulaire})
    else: # sinon on affiche un formulaire vide
        return render(request, "inscription.html", context={'form' : formulaire})

# Vue pour la page de connextion
def connexion(request):
    if request.method == "POST": # si l'utilisateur à envoyer le formulaire
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, email=username, password=password)

        if user is not None: # si on a reussi à identifier l'utilisateur
            login(request, user)
            messages.success(request, "Vous êtes connecté")
            return redirect('index')
        else:
            messages.error(request,("Identifiant ou mot de passe est incorrect"))
            return redirect('connexion')
    else: # si l'utilisateur n'a rien envoyé
        return render(request, "connexion.html")

# Vue pour la page de déconnextion
@login_required
def deconnexion(request):
    logout(request)
    messages.success(request,("Vous êtes déconnecté !!"))
    return redirect('index')
