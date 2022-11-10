import requests
import json
from datetime import datetime
import psycopg2 as conn
url = "https://currencyapi.net/api/v1/rates?key=0TgDimtVZOPraN2QIF9Eppae0uLDVyv4hD9B&base=USD&output=JSON"
response = requests.request("GET", url)
json=json.loads(response.text)
time=datetime.fromtimestamp(json["updated"]).strftime('%Y-%m-%d %H:%M:%S')
rates=json["rates"]
keys=rates.keys()
values=rates.values()
connection = conn.connect(user="postgres",password="postgres",host="postgredb",port="5432",database="postgres")
cursor = connection.cursor()
for keys in rates:
        print(f"Birim {keys} Değer {rates[keys]} Zaman {time}")
        sql="""insert into public.currency_api (date,currency_code,rate) values ('""" + str(time) + """','"""+str(keys)+"""','"""+str(rates[keys])+"""') """
        cursor.execute(sql)
        connection.commit()