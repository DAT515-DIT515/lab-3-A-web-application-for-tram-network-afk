import requests
from bs4 import BeautifulSoup
import json

TRAM_URL_FILE = 'tramstop_vasttrafik_url.json'

def extract_link_with_anchor_text(url, anchor_text):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if anchor_text.lower() in link.text.lower():
                return link['href']
        print(f"No link found with the anchor text '{
              anchor_text}' on the given website.")
        return None
    else:
        print(f"Failed to retrieve the webpage. Status code: {
              response.status_code}")
        return None



website_url = "https://www.vasttrafik.se/reseplanering/hallplatslista/"
url_base = ("https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid=")

dict = {} # yes this could have been done with a readTramNetwork.read_all() but importing files didnt work so we did it manually
all_stops = ['Östra Sjukhuset', 'Tingvallsvägen', 'Kaggeledstorget', 'Ättehögsgatan', 'Munkebäckstorget', 'Härlanda', 'Stockholmsgatan', 'Redbergsplatsen', 'Olskrokstorget', 'Svingeln', 'Ullevi Norra', 'Centralstationen', 'Brunnsparken', 'Stenpiren', 'Järntorget', 'Prinsgatan', 'Olivedalsgatan', 'Linnéplatsen', 'Botaniska Trädgården', 'Marklandsgatan', 'Axel Dahlströms Torg', 'Lantmilsgatan', 'Nymilsgatan', 'Musikvägen', 'Positivgatan', 'Frölunda Torg Spårvagn', 'Briljantgatan', 'Smaragdgatan', 'Opaltorget', 'Mölndals Innerstad', 'Mölndals sjukhus', 'Lackarebäck', 'Krokslätts Fabriker', 'Krokslätts torg', 'Lana', 'Varbergsgatan', 'Elisedal', 'Almedal', 'Liseberg Södra', 'Korsvägen', 'Scandinavium', 'Ullevi Södra', 'Domkyrkan', 'Grönsakstorget', 'Vasaplatsen', 'Vasa Viktoriagatan', 'Handelshögskolan', 'Brunnsgatan', 'Seminariegatan', 'Bokekullsgatan', 'Högsbogatan', 'Klintens Väg', 'Godhemsgatan', 'Mariaplan', 'Ostindiegatan', 'Vagnhallen Majorna', 'Jaegerdorffsplatsen', 'Chapmans Torg', 'Kaptensgatan', 'Stigbergstorget', 'Masthuggstorget', 'Hagakyrkan', 'Valand', 'Kungsportsplatsen', 'Solrosgatan',
             'Sanatoriegatan', 'Virginsgatan', 'Berzeliigatan', 'Gamlestads Torg', 'Hjällbo', 'Hammarkullen', 'Storås', 'Angered Centrum', 'Welandergatan', 'Töpelsgatan', 'Bögatan', 'Ekmanska', 'Bäckeliden', 'Sankt Sigfrids Plan', 'Liseberg Station', 'Lilla Bommen', 'Frihamnen', 'Hjalmar Brantingsplatsen', 'Vågmästareplatsen', 'Wieselgrensplatsen', 'Rambergsvallen', 'Gropegårdsgatan', 'Eketrägatan', 'Sälöfjordsgatan', 'Vårväderstorget', 'Mildvädersgatan', 'Önskevädersgatan', 'Friskväderstorget', 'Väderilsgatan', 'Temperaturgatan', 'Varmfrontsgatan', 'Aprilgatan', 'Allhelgonakyrkan', 'Kortedala Torg', 'Runstavsgatan', 'Nymånegatan', 'Beväringsgatan', 'Kviberg', 'Bellevue', 'SKF', 'Ejdergatan', 'Chalmers', 'Wavrinskys Plats', 'Medicinaregatan', 'Sahlgrenska Huvudentré', 'Nordstan', 'Komettorget', 'Rymdtorget Spårvagn', 'Teleskopgatan', 'Galileis Gata', 'Januarigatan', 'Kapellplatsen', 'Sannaplan', 'Sandarna', 'Kungssten', 'Doktor Sydows Gata', 'Doktor Fries Torg', 'Saltholmen', 'Roddföreningen', 'Långedrag', 'Hinsholmen', 'Käringberget', 'Tranered', 'Hagen', 'Nya Varvsallén', 'Ekedal', 'Majvallen', 'Fjällgatan']

for stop in all_stops:
    stop = stop + ','
    result_link = extract_link_with_anchor_text(website_url, stop)
    gid = result_link.split("/")[3]
    dict[stop] = url_base + gid
with open(TRAM_URL_FILE, 'w' ,encoding='utf8') as file:
    json.dump(dict, file, indent=2, ensure_ascii=False)
    
    #just run this file, and later move the created file wherever you need, me moved it to static.
