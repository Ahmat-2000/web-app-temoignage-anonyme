from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("connexion/", views.connexion, name="connexion"),
    path("inscription/", views.inscription, name="inscription"),
    path("témoigner/", views.temoigner, name="témoigner"),
    path("témoignages/", views.temoignages, name="témoignages"),
    path("témoignages/<int:id>", views.suppressionDeTemoignage, name="suppressionDeTemoignage"),
    path("contact/", views.contact, name="contact"),
    path("deconnexion/", views.deconnexion, name="deconnexion")
]
