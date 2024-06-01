from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from flask import session


def fetch_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def count_internal_ancre_external_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    internal_links = 0
    external_links = 0
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('#'):
            internal_links += 1
        elif urlparse(href).netloc == '':
            internal_links += 1
        else:
            external_links += 1
    return internal_links, external_links
    print(f'Nombre de liens de type ancre interne : {internal_links}')
    print(f'Nombre de liens de type ancre externe : {external_links}')

def check_h1(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.text.strip()
    else:
        return "Aucune balise <h1> trouvée."

def count_h2(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h2_count = 0
    for h2_tag in soup.find_all('h2'):
        h2_count += 1
    print(f'Nombre de balises <h2> : {h2_count}')
    return h2_count



def check_h2(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h2_tag = soup.find('h2')
    if h2_tag:
        return h2_tag.text.strip()
    else:
        return "Aucune balise <h2> trouvée."


def count_h3(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_count = 0
    for h3_tag in soup.find_all('h3'):
        h3_count += 1
    print(f'Nombre de balises <h3> : {h3_count}')
    return h3_count

def check_h3(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_tag = soup.find('h3')
    if h3_tag:
        return h3_tag.text.strip()
    else:
        return "Aucune balise <h3> trouvée."

def count_nav(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    nav_count = 0
    for nav_tag in soup.find_all('nav'):
        nav_count += 1
    print(f'Nombre de balises <nav> : {nav_count}')
    return nav_count

def check_alt(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    if images:
        for img in images:
            alt_text = img.get('alt')
            if alt_text:
                print("Contenu de l'attribut alt :", alt_text)
                return alt_text
            else:
                print("Aucun texte alternatif trouvé pour cette image.")
    else:
        print("Aucune balise <img> trouvée.")

def count_div_imbrications(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    max_depth = 3  # Nombre maximum d'imbrications de div autorisé
    div_count = 0
    avertissement = ""  # Initialisation de la variable d'avertissement

    def count_divs(node, depth):
        nonlocal div_count, avertissement
        if node.name == 'div':
            div_count += 1
            if depth > max_depth:
                avertissement = "Nombre d'imbrications de div trop élevé."

        # Appel récursif pour chaque enfant du nœud actuel
        for child in node.children:
            if child.name is not None:  # Vérifie si l'enfant est un élément balisé
                count_divs(child, depth + 1)

    # Commencez le comptage des imbrications à partir de la racine du document
    count_divs(soup, 0)
    print(f"Nombre total d'imbrications de div : {div_count}")
    print(f"{avertissement}")
    return div_count, avertissement  # Retourne le nombre total de div et l'avertissement, le cas échéant

def main(url):
    html_content = fetch_html_content(url)
    if html_content:
        result_h1 = check_h1(html_content)
        result_h2 = check_h2(html_content)
        result_h3 = check_h3(html_content)
        count_internal_ancre_external_links(html_content)
        total_div_count, warning = count_div_imbrications(html_content)  # Appel de la fonction count_div_imbrications
        count_h2(html_content)
        count_h3(html_content)
        count_nav(html_content)
        check_alt(html_content)
        print("Contenu de la balise <h1> :", result_h1)
        print("Contenu de la balise <h2> :", result_h2)
        print("Contenu de la balise <h3> :", result_h3)

        data = {
            "Contenu de la balise <h1> : ": result_h1,
            "Contenu de la balise <h2> : ": result_h2,
            "Contenu de la balise <h3> : " : result_h3,
            "Nombre de balises <h2> : " : count_h2(html_content),
            "Nombre de balises <h3> : " : count_h3(html_content),
            "Nombre de balises <nav> : " :   count_nav(html_content),
            "nombre de nav : ": count_nav(html_content),
            "Contenu de l'attribut alt : " : check_alt(html_content),
            "Nombre total d'imbrications de div : " : total_div_count,
            "Avertissement : ": warning,
            "Nombre de liens de type ancre interne et externes : ": count_internal_ancre_external_links(html_content)
        }

        return data
    else:
        print("Impossible de récupérer le contenu de l'URL.")

if __name__ == "__main__":
    main()
