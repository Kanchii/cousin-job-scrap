import time
from functools import wraps

def timeit(method):
    @wraps(method)
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{method.__name__} took {elapsed_time:.4f} seconds to execute")
        return result
    return timed

def state_ids() -> dict[str,str]:
    return {'Acre': '12', 'Alagoas': '27', 'Amapa': '16', 'Amazonas': '13', 'Bahia': '29', 'Ceara': '23', 'Distrito Federal': '53', 'Espirito Santo': '32', 'Goias': '52', 'Maranhao': '21', 'Mato Grosso': '51', 'Mato Grosso do Sul': '50', 'Minas Gerais': '31', 'Para': '15', 'Paraiba': '25', 'Parana': '41', 'Pernambuco': '26', 'Piaui': '22', 'Rio de Janeiro': '33', 'Rio Grande do Norte': '24', 'Rio Grande do Sul': '43', 'Rondonia': '11', 'Roraima': '14', 'Santa Catarina': '42', 'Sao Paulo': '35', 'Sergipe': '28', 'Tocantins': '17'}