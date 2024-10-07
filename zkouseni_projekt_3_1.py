"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Veronika Koudelkova
email: koudelkova.veronika87@gmail.com
discord: Veronika K.#4490
"""
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv
import traceback


url_1 = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202"

output_file = "output_file_results.csv"

server_answer = requests.get(url_1)

soup = BeautifulSoup(server_answer.text, 'html.parser')
#print(soup)


table_tag = soup.find("div", {"id": "inner"})
#print(type(table_tag))
all_tr = table_tag.find_all("tr")

#print(type(all_tr[2:]))
#print(all_tr)


def scraping_of_election_results(tr_tags) -> list:

    
    RESULTS_1 = []


    for tr in tr_tags[2:-1]:

        RESULTS_2 = []


        #print(tr)
        td_on_the_row = tr.find_all("td", headers= lambda h: 't1sa' in h or 't2sa' in h or 't3sa' in h)
    
        
        for td in td_on_the_row[1:]:


            code_and_location = {
                "CODE": td_on_the_row[0].get_text(),
                "LOCATION": td_on_the_row[1].get_text(),
            } 
            print("CODE AND LOCATION:", code_and_location)


            url_election_returns = tr.find("a")                                                                 
            url = str(url_election_returns)
            url_election_link = "https://volby.cz/pls/ps2017nss/" + url[9:69].replace("&amp;", "&")             
            #print("URL ELECTION LINK:", url_election_link)
        
    
            server_answer_municipality = requests.get(url_election_link)
            soup_municipality = BeautifulSoup(server_answer_municipality.text, 'html.parser' )
            table_tag_municipality = soup_municipality.find("div", {"id": "content"})
            #print(table_tag_municipality)
            #print(type(table_tag_municipality))
            all_tr_municipality = table_tag_municipality.find_all("tr")


    
            results_each_municipality = list()
        
    
            for tr_mun in all_tr_municipality[1:32]:
                td_on_the_row_mun_registered = tr_mun.find_all("td", {"data-rel": "L1"}, headers= lambda c: 'sa2' in c)
                #print("td_on_the_row_mun_registered:", td_on_the_row_mun_registered)
                td_on_the_row_mun_envelopes = tr_mun.find_all("td",{"data-rel": "L1"}, headers= lambda c: 'sa3' in c)
                td_on_the_row_mun_valid = tr_mun.find_all("td", {"data-rel": "L1"}, headers= lambda c: 'sa6' in c)      
                td_on_the_row_mun_party = (tr_mun.find_all("td", headers= lambda a: 't1sb2' in a or 't2sb2' in a))
                #print("td_on_the_row_mun_party:", td_on_the_row_mun_party)
                td_on_the_row_mun_vote = tr_mun.find_all("td", headers = lambda b: 't1sb3' in b or 't2sb3' in b)
                
                election_results_registered = scraping_of_td_tags(td_on_the_row_mun_registered)
                election_results_envelopes = scraping_of_td_tags(td_on_the_row_mun_envelopes)
                election_results_valid = scraping_of_td_tags(td_on_the_row_mun_valid)
                election_results_party = scraping_of_party_and_vote(td_on_the_row_mun_party)
                election_results_vote = scraping_of_party_and_vote(td_on_the_row_mun_vote)

                #print("election results registered:", election_results_registered)
                #print("election_results_envelopes:", election_results_envelopes)
                #print("election_results_party:", election_results_party)
                #print("election_results_vote:", election_results_vote)


                results_each_municipality.append(election_results_registered)
                results_each_municipality.append(election_results_envelopes)
                results_each_municipality.append(election_results_valid)
                results_each_municipality.append({election_results_party: election_results_vote})
                

            # FILTROVANI VYSLEDKY, ODSTRANENI HODNOT NONE
            filtered_results_each_municipality_1 = list(filter(None, results_each_municipality))
            #print("FILTERED 1:", filtered_results_each_municipality_1)
            filtered_results_each_municipality_2 = []
            for result in filtered_results_each_municipality_1[:]:
                for key, value in result.items():
                    if value is not None:
                        filtered_results_each_municipality_2.append(result)
                
            #print("FILTERED 2:", filtered_results_each_municipality_2)
                
                
            # SLOUCENI DO JEDNOHO SLOVNIKU

            MERGED_DICTIONARIES = dict()

            for i in range(0, len(filtered_results_each_municipality_2)):
                code_and_location.update(filtered_results_each_municipality_2[i])
                MERGED_DICTIONARIES.update(code_and_location)
            
            #print("MERGED DICT:", MERGED_DICTIONARIES)
            RESULTS_2.append(MERGED_DICTIONARIES)
            #print("RESULTS_2:", RESULTS_2)

            break
            
        
        for result in RESULTS_2:
            print("result:", result)
            RESULTS_1.append(result)
    
            print("RESULTS_1:", RESULTS_1)      # POKUD POSUNU return JESTE O JEDEN TABULATOR, VRACI SE MI VYSLEDKY JEN PRO BEHAROV..
                                                    # POKUD VSAK NECHAM return ZDE, DOSTANU CHYBU AttributeError
                                    
    

    

def scraping_of_td_tags(td_on_the_row_mun_: "bs4.element.ResultSet") -> dict:


    for td in td_on_the_row_mun_:
        #print("TD:", td)
        string = str(td)
        #print("string:", string)
        #print(type(string))

        if "sa2" in string:
            nazev = "registered"
        elif "sa3" in string:
            nazev = "envelopes"
        elif "sa6" in string:
            nazev = "valid"

        hodnota = td.get_text()
        if "\xa0" in hodnota:
            cislo = hodnota.replace("\xa0", "")
            nazev_1 = {nazev: cislo}
        else:
            nazev_1 = {nazev: hodnota}          # -> dict

        return nazev_1
    
def scraping_of_party_and_vote(td_on_the_row_mun_: "bs4.element.ResultSet") -> str:

    for td in td_on_the_row_mun_:
        election_returns = td.get_text()
        if election_returns is not None:
            return election_returns

        
RESULTS_KLATOVY = scraping_of_election_results(all_tr)
print("RESULTS KLATOVY:", RESULTS_KLATOVY)

    


          
def zapis_data(data: dict, jmeno_souboru: str) -> str:
    """
    Zkus zapsat udaje z par. 'data' do souboru formatu .csv.
    """
    try:
        csv_soubor = open(jmeno_souboru, mode="w", encoding="cp1250")
        sloupce = data.keys()
        
    except FileExistsError:
        return traceback.format_exc()
    except IndexError:
        return traceback.format_exc()
    else:
        zapis = csv.DictWriter(csv_soubor, fieldnames=sloupce)
        zapis.writeheader()
        zapis.writerows(data)
        return "Saved"
    finally:
        csv_soubor.close()



def main_function(url: str) -> list:                                             # musim pridat jeste output_file.csv

    server_answer = requests.get(url)

    soup = BeautifulSoup(server_answer.text, 'html.parser')
    #print(soup)

    table_tag = soup.find("div", {"id": "inner"})
    #print(type(table_tag))
    all_tr = table_tag.find_all("tr")

    #print(type(all_tr[2:]))
    #print(all_tr)
    try:
        election_returns = scraping_of_election_results(all_tr)
    except AttributeError:
        return traceback
    else:
        print(election_returns)



#vysledky = main_function(url_1)
#print("VYSLEDKY:", vysledky)


