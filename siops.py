from utils import timeit, state_ids
import os

from requests import request
from bs4 import BeautifulSoup

class Siops:
    def __init__(self):
        self.base_url = "http://siops.datasus.gov.br/carga_sitentrega3.php?ckb_01=N"
        self.states = os.listdir("./Database")
        self.state_ids = state_ids()
    
    @timeit
    def run(self):
        for state in self.states:
            state_id = self.state_ids[state]
            response = request('get', f'{self.base_url}&cmbUF={state_id}&cmbAno=2023')
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find_all('tr')
            print(table)
            break

if __name__ == "__main__":
    Siops().run()