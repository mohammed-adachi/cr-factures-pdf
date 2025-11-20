import os
from pathlib import Path
from preOCR import OCRProcessor  # Votre classe OCR
# --- AJOUT ICI : On importe votre nouveau module de parsing ---
from extract_reges import extract_receipt_data 

def main():
    # --- CONFIGURATION ---
    # Remplacez ceci par le chemin de votre fichier PDF
    pdf_input = "./4.pdf" 
    
    # Langue ('en' est recommandé pour le ticket Zion Market)
    langue = "en" 
    # ---------------------

    # Vérifier si le fichier existe
    if not os.path.exists(pdf_input):
        print(f"Erreur : Le fichier '{pdf_input}' est introuvable.")
        return

    print(f"Traitement du fichier : {pdf_input}...")

    # 1. Initialisation de l'OCR
    try:
        processor = OCRProcessor(dpi=300, lang=langue)
        print("Moteur OCR initialisé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de l'OCR : {e}")
        return

    # 2. Conversion PDF -> Images
    try:
        images = processor.pdf_to_images(Path(pdf_input))
        print(f"Le document contient {len(images)} page(s).")
    except Exception as e:
        print(f"Erreur lors de la lecture du PDF : {e}")
        return

    # 3. Boucle sur chaque page pour extraire le texte
    resultat_global_text = ""
    
    for i, img in enumerate(images):
        print(f"--> Analyse de la page {i + 1} en cours...")
        
        # Appel de la fonction run_ocr de votre classe
        text, scores, boxes = processor.run_ocr(img)
        
        # Calcul de la confiance moyenne
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # --- AFFICHAGE OCR BRUT ---
        print(f"\n=== PAGE {i + 1} (Texte Brut / Confiance: {avg_score:.2f}) ===")
        print(text)
        print("=" * 40)
        
        # --- NOUVEAU : EXTRACTION DES DONNÉES (PARSING) ---
        print(f"--> Extraction des informations structurées pour la page {i+1}...")
        
        # On appelle la fonction qui est dans receipt_parser.py
        data = extract_receipt_data(text)
        
        print("\n┌──────────────── RESULTATS EXTRAITS ────────────────┐")
        print(f"│ 🏪 Magasin       : {data.get('merchant')}")
        print(f"│ 📅 Date          : {data.get('date')}")
        print(f"│ 🕒 Heure         : {data.get('time')}")
        print(f"│ 💰 Total         : {data.get('total')}")
        print(f"│ 💳 Carte         : {data.get('card_type')}")
        print(f"│ 🔢 Fin de carte  : {data.get('card_last4')}")
        print("└────────────────────────────────────────────────────┘\n")

        # Ajout au résultat global texte pour sauvegarde
        resultat_global_text += f"PAGE {i+1}\n{text}\n\n"

    # 4. Sauvegarde du résultat brut dans un fichier texte
    output_file = "resultat_ocr.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(resultat_global_text)

    print("-" * 30)
    print(f"Terminé ! Le texte brut a été sauvegardé dans '{output_file}'.")

if __name__ == "__main__":
    main()