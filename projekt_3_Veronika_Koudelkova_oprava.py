"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Veronika Koudelkova
email: koudelkova.veronika87@gmail.com
discord: Veronika K.#4490
"""
import requests
from bs4 import BeautifulSoup
import csv
import traceback

# ARGUMENTS: arg_1 == url_1, arg_2 = output_file

url_1 = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202"           # ENTER THE RIGHT URL OF "KLATOVY" REGION, as data type str()

output_file = "VYSLEDKY_KLATOVY.csv"                                                    # ENTER THE NAME OF THE OUTPUT FILE WITH EXTENSION .csv, data type str()


def MAIN_FUNCTION(url: str, output_file: str) -> str:
    """
    Main function for the launching the programm
    """                                            
   
    if url == "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202":

        server_answer = requests.get(url)

        soup = BeautifulSoup(server_answer.text, 'html.parser')

        table_tag = soup.find("div", {"id": "core"})
        all_tr = table_tag.find_all("tr")

        ELECTION_RESULTS = scraping_of_election_results(all_tr)

        try:
            csv_file = open(output_file, mode="w", encoding="cp1250")
            head = ELECTION_RESULTS[0].keys()

        except FileExistsError:
            return traceback.format_exc()
        except IndexError:
            return traceback.format_exc()
        else:
            zapis = csv.DictWriter(csv_file, fieldnames=head)
            zapis.writeheader()
            zapis.writerows(ELECTION_RESULTS)
            return "Saved"
        finally:
            csv_file.close()

    else:
        return "Invalid arguments: Terminating the programm"




def scraping_of_election_results(tr_tags: "bs4.element.ResultSet") -> list:

    """
    Scraping of RESULTS for each municipality. Return list with dictionaries, each dictionary contain code, location and the election returns.
    """


    RESULTS = list()            # final results, list with dictionaries that contains code, location and the election returns
    RESULTS_1 = list()          # list with successive appending of the municipalities with their all election returns, that originate from the iteration of the list "RESULTS_2"   
    
    
    for tr in tr_tags[2:]:

        #print(tr)
        td_on_the_row = tr.find_all("td", headers= lambda h: 't1sa' in h or 't2sa' in h or 't3sa' in h)
        #print("td_on_the_row:", td_on_the_row)
    
        
        for td in td_on_the_row[1:]:

            RESULTS_2 = scraping_of_td_tags(td, td_on_the_row, tr)
        
            
        # ITERATION OF RESULTS_2, appends to RESULTS_1
        for result_2 in RESULTS_2:
            #print("result:", result)
            RESULTS_1.append(result_2)                        
             
        #print("RESULTS_1:", RESULTS_1)
        #print(len(RESULTS_1))

        # ITERATION OF RESULTS_1, append to RESULTS - final results
        RESULTS = [result for result in RESULTS_1 if len(RESULTS_1) == 98]              # the number 98 represents the number of records in the last list 
        #print(RESULTS)
    
        # RETURN OF NON-EMPTY LIST
        if (bool(RESULTS)) == True:                        

            return RESULTS

def generation_of_url_each_municipality(tr:"bs4.element.Tag") -> str:
    """
    Generation of URL for each municipality.
    """
    url_election_returns = tr.find("a")                                                                 
    url = str(url_election_returns)
    url_election_link = "https://volby.cz/pls/ps2017nss/" + url[9:69].replace("&amp;", "&")             
    #print("URL ELECTION LINK:", url_election_link)

    return url_election_link 

def scraping_tags_for_each_municipality(url_election_link: str) -> "bs4.element.ResultSet": 
    """ 
    Scraping of all "tr" for each municiaplity.
    """
    
    server_answer_municipality = requests.get(url_election_link)
    soup_municipality = BeautifulSoup(server_answer_municipality.text, 'html.parser' )
    table_tag_municipality = soup_municipality.find("div", {"id": "core"})
    #print(table_tag_municipality)
    #print(type(table_tag_municipality))
    all_tr_municipality = table_tag_municipality.find_all("tr")

    return all_tr_municipality


                      
def scraping_of_td_tags_each_municipality(td_on_the_row_mun_: "bs4.element.ResultSet") -> dict:
    """
    Scraping the number of registered voters, the number of returned envelopes and the number of valid votes cast
    """

    for td in td_on_the_row_mun_:
        #print("TD:", td)
        string = str(td)
        #print("string:", string)
        #print(type(string))

        if "sa2" in string:
            name = "registered"
        elif "sa3" in string:
            name = "envelopes"
        elif "sa6" in string:
            name = "valid"

        value = td.get_text()
        if "\xa0" in value:
            number = value.replace("\xa0", "")
            name_1 = {name: number}
        else:
            name_1 = {name: value}          # -> dict

        return name_1
    
    
def scraping_of_party_and_vote(td_on_the_row_mun_: "bs4.element.ResultSet") -> str:
    """
    Scraping of results for each party in each municipality
    """

    for td in td_on_the_row_mun_:
        election_returns = td.get_text()
        if election_returns is not None:
            return election_returns
        

def scraping_of_td_each_mun(all_tr_municipality: "bs4.element.ResultSet") -> list:
    """
    Scraping and matching "td" to each specific results for each municipality.
    """
    results_each_municipality = list()

    for tr_mun in all_tr_municipality[1:]:
        td_on_the_row_mun_registered = tr_mun.find_all("td", {"data-rel": "L1"}, headers= lambda c: 'sa2' in c)
        #print("td_on_the_row_mun_registered:", td_on_the_row_mun_registered)
        td_on_the_row_mun_envelopes = tr_mun.find_all("td",{"data-rel": "L1"}, headers= lambda c: 'sa3' in c)
        td_on_the_row_mun_valid = tr_mun.find_all("td", {"data-rel": "L1"}, headers= lambda c: 'sa6' in c)      
        td_on_the_row_mun_party = (tr_mun.find_all("td", headers= lambda a: 't1sb2' in a or 't2sb2' in a))
        #print("td_on_the_row_mun_party:", td_on_the_row_mun_party)
        td_on_the_row_mun_vote = tr_mun.find_all("td", headers = lambda b: 't1sb3' in b or 't2sb3' in b)
                
        election_results_registered = scraping_of_td_tags_each_municipality(td_on_the_row_mun_registered)
        election_results_envelopes = scraping_of_td_tags_each_municipality(td_on_the_row_mun_envelopes)
        election_results_valid = scraping_of_td_tags_each_municipality(td_on_the_row_mun_valid)
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

    return results_each_municipality


def filtering(results_each_municipality: list) -> list:
    """ 
    Filtering of results for each municipality - deleting of "None" values.
    """
    filtered_results_each_municipality_1 = list(filter(None, results_each_municipality))
    #print("FILTERED 1:", filtered_results_each_municipality_1)

    filtered_results_each_municipality_2 = list()

    for result in filtered_results_each_municipality_1[:]:
        for key, value in result.items():
            if value is not None:
                filtered_results_each_municipality_2.append(result)

    return filtered_results_each_municipality_2


def merging_of_dictionaries(filtered_results_each_municipality_2: list, code_and_location: dict) -> list:
    """
    Merging of dictionaries into one dictionary with results for each municpality and its election returns,
    return list "RESULTS_2" - list with dictionaries - each dictionary contains code, location and the election returns
    """
    RESULTS_2 = list()
    MERGED_DICTIONARIES = dict()

    for i in range(0, len(filtered_results_each_municipality_2)):
        code_and_location.update(filtered_results_each_municipality_2[i])
        MERGED_DICTIONARIES.update(code_and_location)               
            
    #print("MERGED DICT:", MERGED_DICTIONARIES)
    RESULTS_2.append(MERGED_DICTIONARIES)
    #print("RESULTS_2:", RESULTS_2)

    return RESULTS_2

def scraping_of_td_tags(td: "bs4.element.Tag", td_on_the_row: "bs4.element.ResultSet", tr: "bs4.element.Tag") -> list:
    code_and_location = {
        "CODE": td_on_the_row[0].get_text(),
                "LOCATION": td_on_the_row[1].get_text(),
        } 
        #print("CODE AND LOCATION:", code_and_location)

    url_election_link = generation_of_url_each_municipality(tr)

    all_tr_municipality = scraping_tags_for_each_municipality(url_election_link)
    
    results_each_municipality = scraping_of_td_each_mun(all_tr_municipality)
        
    filtered_results_each_municipality_2 = filtering(results_each_municipality)                         # DELETING OF "NONE" VALUES

    RESULTS_2 = merging_of_dictionaries(filtered_results_each_municipality_2, code_and_location)        # LIST WITH MERGED DICTIONARIES       
    #print("RESULTS_2:", RESULTS_2)

    return RESULTS_2


vysledky = MAIN_FUNCTION(url_1, output_file)
print(vysledky)



