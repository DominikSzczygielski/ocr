#### BREW TESSERACT!!!!

from PIL import Image
import pytesseract

# 🔹 Jeśli używasz Windowsa, ustaw ścieżkę do Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def rozpoznaj_teskt(sciezka_do_pliku):
    try:
        # Otwórz obraz
        image = Image.open(sciezka_do_pliku)
        custom_config = "--psm 6 --oem 3"
        # Konwersja obrazu na tekst
        text = pytesseract.image_to_string(image, lang="pol", config=custom_config)
        print(text)
        return text
    except Exception as e:
        return f"Błąd: {e}"

# 🔹 Przykładowe użycie


