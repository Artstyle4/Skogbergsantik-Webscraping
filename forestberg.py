import requests, csv, os
import pandas as pd
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
#url som används för scrapingen
url = "https://www.blocket.se/annonser/hela_sverige?f=p&page="
#hitta platsen som scriptet körs ifrån
dir_path = os.path.dirname(os.path.realpath(__file__))

#hämtar ett Beautiful-Soupobjekt från urlen
def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup



#skriver om htmlkoden till text och skriver till .csvfilen
def get_ads():
    f = open(dir_path+'/Blocket.csv' , 'w')
    writer = csv.writer(f)
 
    #range anger antalet sidor
    for i in range(5):
        soup = parse_site(url+str(i+1))
       
    
    

        #hitta namn på objektet
        ad_name = [ad_name.text for ad_name in soup.find_all("span" , class_="bkaUbj")]
        #hitta pris på objektet
        ad_price = [ad_price.text for ad_price in soup.find_all("div" , class_="jVOeSj")]
        ##tar bort "kr" från prislistan för att enklare kunna visualisera priserna som ints
        ad_price = [ad_price.replace("kr","") for ad_price in ad_price]
        ##hitta url för det specifika objektet
        ad_url = [ad_url["href"] for ad_url in soup.find_all("a", class_="evOAPG")]
        ##lägg till blocket.se för fullständig länk
        ad_url = ["https://blocket.se" + ad_url for ad_url in ad_url]
        ##hitta datum för objektet
        ad_date = [ad_date.text for ad_date in soup.find_all("p" , class_="gEFkeH")]

    
        # ändrar blockets datum för 'Idag' och 'Igår' till korrekt datum. 
        today = date.today().strftime("%d %B %Y")
        yesterday = date.today() - timedelta(days=1)
        ad_date = [ad_date.replace("Idag", today) for ad_date in ad_date]
        ad_date = [ad_date.replace("Igår",yesterday.strftime("%d %B %Y")) for ad_date in ad_date]
        #hitta var objektet säljs någonstans
        ad_placecategory = [ad_placecategory.text for ad_placecategory in soup.find_all("a" , class_="hNTkPP")]
        
        ad_category = ad_placecategory[0:][::2]
        ad_place = ad_placecategory[1:][::2]

       
        ##ad_place = [i.isalpha() for i in ad_place]
        #sätter ihop alla variabler till en lista som sedan skrivs till en .csv
        ad_list = zip(ad_name,ad_category,ad_place, ad_price, ad_date, ad_url,)
        ad_list = list(filter(None, ad_list))
        print("Scrapear sida "+ str(i+1))  
        #skriv alla objekt till csv
        [writer.writerow(ad_list) for ad_list in ad_list]



    

    f.close()





get_ads()

#fixa headers till .csv-filen
headerList = ['Namn','Kategori','Plats','Pris','Datum', 'Länk']
file = pd.read_csv(dir_path+'/Blocket.csv')
file.to_csv(dir_path+'/Blocket.csv', header=headerList,index=False)





