import requests
import json
import re
from pprint import pprint

# Create index
res_index = requests.get("https://127.0.0.1:9200", verify = False)
res_index = str(res_index)
if re.search('error', res_index) : 
    raise SystemExit("Elastic Search connexion error") 
else : 
    res_bano = requests.get("https://127.0.0.1:9200/bano", verify = False)
    if re.search('error', str(res_bano)) :
        # cration de l'index
        mapping = {
            "mapping" : {
                "adresses" : {
                    "properties" : {
                        "name" : {"type" : "string" },
                        "postcode" : {"type" : "string" },
                        "city" : {"type" : "string" },
                        "context" : {"type" : "string" },
                        "point" : {"type" : "list" }
                    }
                }
            }
        }
        requests.put("https://127.0.0.1:9200/bano", json=mapping, verify = False)
        



# scrap de l'API - 21 

response = requests.get("https://api-adresse.data.gouv.fr/search/?q=c%C3%B4te-d%27Or", verify = False)

json_dict = json.loads(response.text)
pprint(json_dict)

max_index = 0
for index, feature in enumerate(json_dict["features"]) :
    if re.search('^21', feature["properties"]["context"]):
        # Mettre la feature en forme pour l'envoyer dans elasticsearch
        first_part = json.dumps({"create" : {"_index" : "bano", "_type" : "adresses", "_id" : index }})
        second_part = json.dumps({"name" : feature["properties"]["name"], "postcode" : feature["properties"]["postcode"], "city" : feature["properties"]["city"], "context" : feature["properties"]["context"], "point" : feature["geometry"]["coordinates"]})
        sum_part = first_part + second_part

        requests.put("https://localhost:9200/_bulk", json=sum_part, verify = False)
        max_index = index

res_test_bano = requests.get("https://127.0.0.1:9200/bano", verify = False)
print(res_test_bano)
print(f"{max_index} documents enregistrés.")
print("Le premier document est  : ")
res_test = requests.get("https://127.0.0.1:9200/bano/_search", verify = False)
print(res_test)
