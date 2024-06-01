import requests
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logging.basicConfig(level=logging.INFO)
def get_page_speed_insights(url, api_key):
    # URL de l'API PageSpeed Insights
    api_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}&strategy=mobile'

    # classes for project
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # Faire une demande à l'API
    response = requests.get(api_url)
    data = response.json()

    # Vérifier si la demande a réussi
    if response.status_code == 200 and 'lighthouseResult' in data:
        audits = data['lighthouseResult']['audits']

        first_paint = audits.get('first-contentful-paint', {}).get('displayValue', 'N/A')
        largest_contentful_paint = audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A')
        onload_time = audits.get('onload', {}).get('displayValue', 'N/A')
        time_to_interactive = audits.get('interactive', {}).get('displayValue', 'N/A')

        return {
            'First Paint': first_paint,
            'Largest Contentful Paint': largest_contentful_paint,
            'Onload Time': onload_time,
            'Time to Interactive': time_to_interactive
        }
    else:
        return None


# URL de la page à analyser
url = 'https://www.xeilos.fr/'
# Clé API PageSpeed Insights
api_key = 'AIzaSyBHi93uFVrk8tQ-na69HhH3oJiuRP7q2DA'

# Récupérer les métriques de PageSpeed Insights
metrics = get_page_speed_insights(url, api_key)
if metrics:
    print("First Paint:", metrics['First Paint'])
    print("Largest Contentful Paint:", metrics['Largest Contentful Paint'])
    print("Onload Time:", metrics['Onload Time'])
    print("Time to Interactive:", metrics['Time to Interactive'])
else:
    print("Erreur lors de la récupération des métriques.")

