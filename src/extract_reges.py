import re
from typing import List, Dict, Any

# ----------------- 1. Nouveaux Patterns (Adaptés aux tickets de caisse) -------------------
PATTERNS = {
    # Cherche une date au format MM/DD/YYYY ou DD-MM-YYYY
    "date": re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"),
    
    # Cherche l'heure (ex: 18:40:47)
    "time": re.compile(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b"),
    
    # Cherche le montant total spécifique aux tickets US/CB (SALE AMOUNT, TOTAL, USD)
    "total_amount": re.compile(
        r"(?:SALE AMOUNT|TOTAL|AMOUNT|USD)[:\s]*\$?\s*(?P<amount>[\d\.,]+)", 
        re.IGNORECASE
    ),
    
    # Cherche les 4 derniers chiffres de la carte (XXXXXXXXXXXX4195)
    "card_number": re.compile(r"[X\*\-\s]{4,}(?P<last4>\d{4})\b", re.IGNORECASE),
    
    # Cherche le type de carte (VISA, MASTERCARD, AMEX)
    "card_type": re.compile(r"\b(VISA|MASTERCARD|AMEX|DISCOVER|DEBIT)\b", re.IGNORECASE),
    
    # Cherche le nom du commerce (souvent en haut)
    # On ne peut pas faire de regex parfaite pour le nom, on prendra les premières lignes.
}

# ----------------- 2. Normalisation des chiffres --------------------
def normalize_decimal(s: str) -> float:
    """Convertit un string monétaire en float (ex: '7.07' -> 7.07)."""
    if not s: return 0.0
    # Nettoyage basique
    s = s.replace("$", "").replace(" ", "")
    # Correction OCR classique (l/I -> 1, O -> 0)
    s = re.sub(r"(?<=\d)[lI](?=\d|\.)", "1", s)
    s = re.sub(r"O", "0", s)
    
    try:
        return float(s)
    except ValueError:
        return 0.0

# ----------------- 3. Extracteurs Simplifiés ------------------

def extract_merchant_name(text: str) -> str:
    """Prend la première ligne non vide comme nom du magasin."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        # Souvent la ligne 1 est le nom ("ZION MARKET - SD")
        # Parfois il y a "Welcome to" avant, on pourrait le nettoyer.
        return lines[0]
    return "Inconnu"

def extract_receipt_data(text: str) -> Dict[str, Any]:
    """Extrait les données principales du ticket."""
    data = {
        "merchant": extract_merchant_name(text),
        "date": None,
        "time": None,
        "total": 0.0,
        "card_type": None,
        "card_last4": None
    }
    
    # Extraction Date
    m_date = PATTERNS["date"].search(text)
    if m_date:
        data["date"] = m_date.group(1)
        
    # Extraction Heure
    m_time = PATTERNS["time"].search(text)
    if m_time:
        data["time"] = m_time.group(1)
        
    # Extraction Total
    # On cherche "SALE AMOUNT" ou "TOTAL"
    m_total = PATTERNS["total_amount"].search(text)
    if m_total:
        data["total"] = normalize_decimal(m_total.group("amount"))
    else:
        # Fallback: Si on ne trouve pas le mot "TOTAL", on cherche le plus gros montant en bas du ticket
        # C'est risqué mais utile pour les tickets mal imprimés.
        amounts = re.findall(r"\$\s*(\d+\.\d{2})", text)
        if amounts:
            # On suppose que le max est le total
            floats = [float(a) for a in amounts]
            data["total"] = max(floats)

    # Extraction Infos Carte
    m_card = PATTERNS["card_number"].search(text)
    if m_card:
        data["card_last4"] = m_card.group("last4")
        
    m_type = PATTERNS["card_type"].search(text)
    if m_type:
        data["card_type"] = m_type.group(1).upper()

    return data