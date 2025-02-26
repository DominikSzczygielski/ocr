from django.urls import path
from .views import *

urlpatterns = [
    path("", lista, name="lista"),
    path("wgraj/", wgraj_plik, name="wgraj_plik"),
    path("pdf/<int:page>/", wyswietl_pdf, name="wyswietl_pdf"),
    path("pdf/", wyswietl_pdf, name="wyswietl_pdf"),
    path("wordy/", wyswietl_word, name="wyswietl_word"),
    path("upload_selection/", upload_selection, name="upload_selection"),
    path("list/", lista, name="lista"),
    path("route/", route, name="route")
]

from django.urls import include, path

