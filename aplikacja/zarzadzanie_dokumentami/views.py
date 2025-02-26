import uuid
import re
import mammoth
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .forms import WgrajPlik
from pdf2image import convert_from_path, pdfinfo_from_path
import base64
import os
from io import BytesIO
from .models import Pliki
from .foos import ocr
import hashlib

def wgraj_plik(request):
    if request.method == "POST":
        form = WgrajPlik(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]

            form.save()


            ext = os.path.splitext(uploaded_file.name)[1]
            new_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join("storage/uploads/new_files/", new_filename)

            # **Wstrzymanie kodu do momentu całkowitego zapisania pliku**
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            request.session['plik'] = new_filename

            if (re.search(r"(\.pdf)$", new_filename, re.IGNORECASE)):

                return redirect("/aplikacja/pdf/")
            elif (re.search(r"(\.(doc|docx))$", new_filename, re.IGNORECASE)):
                return redirect("/aplikacja/wordy/")
            else:
                return redirect("/aplikacja/")
    else:
        form = WgrajPlik()
        return render(request, "dodaj.html", {"form": form})

def wyswietl_pdf(request, page=None):
   ### pdf_nazwa = get_object_or_404(Pliki,<TODO>)
    pdf_nazwa = request.session['plik']

    images = convert_from_path(f'./storage/uploads/new_files/{pdf_nazwa}')
    pdf_info = pdfinfo_from_path(f'./storage/uploads/new_files/{pdf_nazwa}')
    if page==None:
        page = 1
    num_pages = pdf_info["Pages"]
    if page > num_pages:
        page = num_pages

    buffered = BytesIO()
    images[page-1].save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    with open("test_base64.txt", "w") as f:
        f.write(img_str[:200])
    return render(request, "pdf_render.html", {"obraz": img_str,"strona":page})

def wyswietl_word(request):
    if request.method == "POST":
        pass

    word_nazwa = r'testword.docx'

    dokument_skonwertowany = mammoth.convert_to_html(f'./storage/uploads/new_files/{word_nazwa}')


    return render(request, "wordy.html", {"dokument": dokument_skonwertowany.value})

def index(request):
    return render(request, "upload.html")
def upload_selection(request):

    if request.method == "POST" and request.FILES.get("cropped_image"):
        uploaded_file = request.FILES["cropped_image"]

        # Tworzymy katalog jeśli nie istnieje
        save_path = os.path.join(settings.MEDIA_ROOT, "cropped_images")
        os.makedirs(save_path, exist_ok=True)

        # Zapisujemy plik
        file_path = os.path.join("cropped_images", uploaded_file.name)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)


        with open(full_path, "wb") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        czytnik = ocr.rozpoznaj_teskt(full_path)
        return JsonResponse({"tekst": czytnik})

    return JsonResponse({"error": "Błąd przesyłania"}, status=400)