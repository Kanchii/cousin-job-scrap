from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
import requests
from utils import timeit, state_ids

import os

class Siope:
    def __init__(self):
        self.base_url = "https://www.fnde.gov.br/siope/recibosTransmissao.do?tipoDeRecibo=1&cod_uf=42"
        self.states = os.listdir("./Database")

    def __get_state_ids(self):
        return state_ids()

    def __get_city_ids(self, state_id: str):
        response = requests.get(f"{self.base_url}&cod_uf_mun={state_id}")

        # Parse the HTML content
        soup = bs(response.content, 'html.parser')

        # Find all option elements within the select tag
        cities = soup.select('select[name="municipios"] option')
        city_ids = dict()
        for city in cities:
            value = city['value']
            text = city.get_text(strip=True)
            city_ids[text] = value
        
        return city_ids

    def __get_city_last_homologation(self, city):
        state_id = self.state_ids[self.current_state]
        city_id = self.city_ids[city]
        response = requests.get(f"{self.base_url}&cod_uf_mun={state_id}&municipios={city_id}&consultar=Consultar")

        # Parse the HTML content
        soup = bs(response.content, 'html.parser')
        # Find all <tr> elements with class "rowA"
        tr_elements = soup.find_all('tr', class_='rowA')

        # Get the first occurrence (if any)
        first_occurrence = tr_elements[0] if tr_elements else None
        if(first_occurrence is None):
            print("Não encontrado nenhuma homologação!")
            return None

        td_elements = first_occurrence.find_all('td')
        print(f'[{self.current_state}] {city} - DONE')
        return {'city': city, 'last_homolog': td_elements[0].get_text(strip=True) if td_elements else None }
    
    def __get_cities_from_states(self, state: str):
        with open(f"./Database/{state}", "r", encoding="UTF-8") as f:
            cities = [x.replace("\n", "") for x in f.readlines()]
            return cities
        
    def __write_result(self, state: str, cities_last_homologation: dict):
        with open(f"./Siope/{state}.csv", "w", encoding="UTF-8") as f:
            f.write("Cidade,Homologado\n")
            for (city, last_homologation) in cities_last_homologation.items():
                f.write(f"{city},{last_homologation}\n")

    @timeit
    def run(self):
        self.state_ids = self.__get_state_ids()

        for state in self.states:
            self.current_state = state
            cities = self.__get_cities_from_states(state)
                
            self.city_ids = self.__get_city_ids(self.state_ids[state])
            cities_last_homologation = dict()
            with ThreadPoolExecutor(max_workers=64) as executor:
                last_homologations_by_city = list(executor.map(self.__get_city_last_homologation, cities))
            for idx, obj in enumerate(last_homologations_by_city):
                cities_last_homologation[obj['city']] = obj['last_homolog'] if obj['last_homolog'] else "-"
            
            self.__write_result(state, cities_last_homologation)

if __name__ == "__main__":
    Siope().run()