
<h1>Scraping <a href="https://currencyapi.net" target="_blank">currencyapi.net</a></h1>
<h2>Project is created with:<h2>
<ul>
    <li>
        <a href="https://www.python.org" target="_blank">Python</a>
    </li>
    <li>
        <a href="https://www.docker.com" target="_blank">Docker</a>
    </li>
</ul>

### used Python Libraries 

- <a href="https://pypi.org/project/requests/" target="_blank">Requests</a> for a send request and get response from <a href="https://currencyapi.net" target="_blank">currencyapi.net</a>
- <a href="https://docs.python.org/3/library/json.html" target="_blank">JSON</a> for a parse response text
- <a href="https://pypi.org/project/psycopg2/" target="_blank">Psycopg2</a> for a inserting data to postgresql server.

### Documentation

- Request to <a href="https://currencyapi.net" target="_blank">currencyapi.net</a> then get response
```
url = "https://currencyapi.net/api/v1/rates?key=0TgDimtVZOPraN2QIF9Eppae0uLDVyv4hD9B&base=USD&output=JSON"
response = requests.request("GET", url)
```
- Parsing JSON from a response
```
json=json.loads(response.text)
rates=json["rates"]
keys=rates.keys()
values=rates.values()
```
- For loop for a insert JSON data to Postgresql 
```
for keys in rates:
        print(f"Birim {keys} Değer {rates[keys]} Zaman {time}")
        sql="""insert into public.currency_api (date,currency_code,rate) values ('""" + str(time) + """','"""+str(keys)+"""','"""+str(rates[keys])+"""') """
        cursor.execute(sql)
        connection.commit()
```
- Create a Dockerfile & Requirements.txt file for Dockerize Python Scrap App
```
FROM python:latest

WORKDIR /usr/src/app .

COPY requirements.txt .
COPY currency_api.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","./currency_api.py"]
```
- Create a Table for Inserting Data
```
CREATE TABLE IF NOT EXISTS currency_api (
    date timestamp without time zone,
    currency_code text,
	rate double precision
);
```
- Create a PostgreSQL Official Docker Image & Docker-compose.yaml
```
version: '3.7'
services:
    postgres:
        image: postgres:latest
        container_name: postgredb
        restart: always
        environment:
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=postgres
        ports:
          - '5432:5432'
        volumes: 
          - ./postgres-data:/var/lib/postgresql/data
          - ./create_currency_table.sql:/docker-entrypoint-initdb.d/create_currency_table.sql
        networks:
          - net  
    currency:
        image: currency
        container_name: currency
        networks: 
          - net
networks:
  net:
```
