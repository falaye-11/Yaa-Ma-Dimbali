# Script de test pour valider l'intégration avec le modèle vision NVIDIA
# (utilisé pour prouver la faisabilité technique du projet)
# Dans l'application finale, l'image proviendrait dynamiquement du scan
# effectué par l'utilisateur, plutôt que d'un fichier fixe local.

import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import base64
import json
import re

# --- Config ---
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
api_key = "nvapi-ta-cle-ici "  # remplace uniquement sur ton fichier local

# --- Charger et encoder l'image ---
with open("img.jpeg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

prompt_text = """Tu es un assistant qui analyse des photos d'ordonnances médicales ou de devis de pharmacie.

Analyse cette image et extrais les informations suivantes :
- Le nombre de médicaments prescrits (un chiffre uniquement, ne liste pas leurs noms)
- Le montant total en FCFA, UNIQUEMENT s'il est explicitement écrit sur l'image (sinon laisse ce champ vide)
- La région ou ville, si mentionnée
- L'âge du patient, si mentionné
- Le nom ou type de l'établissement (hôpital public, clinique privée, centre de santé...), si mentionné
- La date de l'ordonnance, si mentionnée

Réponds UNIQUEMENT au format JSON suivant, sans aucun texte avant ou après, sans phrase d'introduction ni d'explication :
{
  "nombre_medicaments": 3,
  "montant": null,
  "region": "Rufisque",
  "age_patient": null,
  "etablissement": null,
  "date_ordonnance": null,
  "lisible": true
}

N'invente jamais une valeur qui n'est pas réellement visible sur l'image : laisse le champ à null dans ce cas.
Si l'image n'est pas une ordonnance/un devis ou si le texte est totalement illisible, réponds avec "lisible": false et laisse les autres champs à null."""

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

payload = {
    "model": "meta/llama-3.2-11b-vision-instruct",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }
    ],
    "frequency_penalty": 0,
    "max_tokens": 512,
    "presence_penalty": 0,
    "stream": False,
    "temperature": 0.2,
    "top_p": 1
}

response = requests.post(invoke_url, headers=headers, json=payload)
result = response.json()

# Si l'API renvoie une erreur, on l'affiche clairement plutôt que de planter
if "choices" not in result:
    print("Erreur renvoyée par l'API :")
    print(result)
    sys.exit(1)

content = result["choices"][0]["message"]["content"]

# Le modèle ajoute parfois du texte autour du JSON malgré la consigne :
# on extrait uniquement le bloc JSON, où qu'il soit dans la réponse.
match = re.search(r'\{.*\}', content, re.DOTALL)

if match:
    donnees = json.loads(match.group())
    print("Résultat brut extrait par l'IA :")
    print(donnees)
    print()

    # --- Anonymisation : transformation en catégories génériques ---
    # Ces catégories sont celles qu'on affiche publiquement aux donateurs,
    # jamais les valeurs brutes ci-dessus.

    def categoriser_etablissement(nom):
        if not nom:
            return None
        nom = nom.lower()
        if any(mot in nom for mot in ["hopital", "hôpital", "chu", "chr", "chn", "chd", "centre hospitalier"]):
            return "Hôpital public"
        if "clinique" in nom:
            return "Clinique privée"
        if any(mot in nom for mot in ["centre de sante", "centre de santé", "poste de sante", "poste de santé", "dispensaire"]):
            return "Centre de santé"
        return "Établissement médical"

    def categoriser_age(age):
        if age is None:
            return None
        age = int(age)
        if age <= 12:
            return "Enfant (0-12 ans)"
        if age <= 54:
            return "Jeune / Adulte (13-54 ans)"
        return "Personnes âgées (55 ans et plus)"

    donnees_publiques = {
        "nombre_medicaments": donnees.get("nombre_medicaments"),
        "montant": donnees.get("montant"),
        "region": donnees.get("region"),
        "tranche_age": categoriser_age(donnees.get("age_patient")),
        "type_etablissement": categoriser_etablissement(donnees.get("etablissement")),
        "date_ordonnance": donnees.get("date_ordonnance"),
    }

    print("Ce qui serait affiché publiquement aux donateurs (anonymisé) :")
    print(donnees_publiques)
else:
    print("Pas de JSON trouvé dans la réponse. Réponse brute du modèle :")
    print(content)