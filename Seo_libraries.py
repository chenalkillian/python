# page_analysis_library.py

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime  # Ajout de l'import pour le timestamp

def test_internal_and_external_links_for_404(url):
    internal_links_results = {}
    external_links_results = {}

    html_content = get_html_content(url)
    internal_links = get_internal_links(html_content, url)
    external_links = get_external_links(html_content, url)

    # Test des 10 premiers liens internes pour les erreurs 404
    for link in internal_links[:10]:
        try:
            response = requests.head(link)
            if response.status_code == 404:
                internal_links_results[link] = "Erreur 404"
            else:
                internal_links_results[link] = "OK"
        except requests.exceptions.RequestException as e:
            internal_links_results[link] = str(e)

    # Test des 10 premiers liens externes pour les erreurs 404
    for link in external_links[:10]:
        try:
            response = requests.head(link)
            if response.status_code == 404:
                external_links_results[link] = "Erreur 404"
            else:
                external_links_results[link] = "OK"
        except requests.exceptions.RequestException as e:
            external_links_results[link] = str(e)

    return internal_links_results, external_links_results

def get_links_from_page(url):
    links = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
    return links


def get_html_content(url):
    response = requests.get(url)
    return response.text

def check_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text
    else:
        return "Aucune balise <title> trouvée."

def count_internal_external_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    internal_links = 0
    external_links = 0
    for link in soup.find_all('a', href=True):
        link_url = urljoin(base_url, link['href'])
        if urlparse(link_url).netloc == urlparse(base_url).netloc:
            internal_links += 1
        else:
            external_links += 1
    return internal_links, external_links

def test_links_for_404(links):
    results = {}
    for link in links[:10]:  # Tester uniquement les 10 premiers liens
        try:
            response = requests.head(link)
            if response.status_code == 404:
                results[link] = "Le lien renvoie une erreur 404."
            else:
                results[link] = "OK"
        except requests.exceptions.RequestException as e:
            results[link] = f"Une erreur s'est produite lors de la requête : {str(e)}"
        return results


def check_h1(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.text
    else:
        return "Aucune balise <h1> trouvée."

def check_header_main_footer(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    header_exists = bool(soup.find('header'))
    main_exists = bool(soup.find('main'))
    footer_exists = bool(soup.find('footer'))
    return header_exists, main_exists, footer_exists

def generate_pdf(rapport):
    # Création du nom de fichier PDF avec un timestamp pour le différencier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_file = f"page_analysis_{timestamp}.pdf"

    # Création du canvas PDF
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Définition de la police et de la taille de police
    c.setFont("Helvetica", 10)

    # Position verticale initiale
    y_position = 750

    # Espacement vertical entre les lignes
    vertical_spacing = 10

    # Parcourir chaque élément du rapport et les ajouter au PDF
    for key, value in rapport.items():
        y_position -= vertical_spacing

        # Convertir les valeurs booléennes en chaînes de caractères pour l'affichage
        if isinstance(value, bool):
            value = "Oui" if value else "Non"

        # Diviser le texte en plusieurs lignes si nécessaire
        lines = [f"{key}: {value}"]
        max_line_length = 70  # Longueur maximale d'une ligne
        if len(lines[0]) > max_line_length:
            lines = [lines[0][i:i + max_line_length] for i in range(0, len(lines[0]), max_line_length)]

        # Dessiner chaque ligne sur le PDF
        for line in lines:
            c.drawString(50, y_position, line)
            y_position -= vertical_spacing

    # Enregistrer le PDF et fermer le canvas
    c.save()
    print(f"Le fichier PDF '{pdf_file}' a été généré avec succès.")





    def main():
        # Définir l'URL à analyser (remplacez 'votre_url' par l'URL réelle)
        url = 'https://fr.vikidia.org/'

        # Appeler la fonction pour tester les liens internes et externes pour les erreurs 404
        internal_links_results, external_links_results = test_internal_and_external_links_for_404(url)

        # Appeler d'autres fonctions pour collecter des informations sur la page
        html_content = get_html_content(url)
        title = check_title(html_content)
        h1_content = check_h1(html_content)
        header_exists, main_exists, footer_exists = check_header_main_footer(html_content)

        # Générer le rapport
        rapport = {
            'URL': url,
            'Titre': title,
            'Header exists': header_exists,
            'Main exists': main_exists,
            'Footer exists': footer_exists,
            'Contenu de la balise <h1>': h1_content,
            'Liens internes': internal_links_results,
            'Liens externes': external_links_results,
            'Liens externes, Liens internes': count_internal_external_links(html_content, url)
        }

        # Générer le fichier PDF
        generate_pdf(rapport)

    if __name__ == "__main__":
        main("https://fr.gymshark.com/")
