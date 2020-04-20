# Currency Exchange RESTful API
###### REST API developed for QMUL (Queen Mary University of London) ECECS781P CLOUD COMPUTING(2019/20) Mini-Project

This RESTful Application Program Interface (API) is developed using Python and Flask. It provides a simple REST API with **real-time, historical exchange rates and currency details for 168 world currencies**, delivering currency pairs in universally usable JSON format. 

## Mini Project aims and objectives
Overall this mini project successfully implements following features:
1. Dynamically generated REST-based service interface.
2. Interaction with external REST services to complement its functionality. [currencylayer](https://currencylayer.com/)
3. Use of on an external Cloud database for persisting information. [country-currency](https://tinyurl.com/sbj72fc)
4. Cassandra ring scaling for cloud scalability, deployment in a container environment. 
5. Supports HTTP request: GET, POST, DELETE requests.

## Getting Started
### Introduction
Following pages are avilable for RESTful API
1. HOMEPAGE
```hostname:portnumber``` 

2. COUNTRY-CURRENCY INFORMATION
```hostname:portnumber/unit```

3. ENQUIRY CURRENCY CODE FROM COUNTRY NAME eg: Finland, Philippines
```hostname:portnumber/unit/Finland```
```hostname:portnumber/unit/Philippines```

4. GET LIVE MARKET EXCHANGE RATE (EXTERNAL)
```hostname:portnumber/livemarket```

5. GET HISTORICAL EXCHANGE RATE (EXTERNAL)
```hostname:portnumber/historicalexchange```

404 Pages for unknown queries.

### How to set-up for using Terminal (Linux)
1. Download / clone the Github files.
2. Open Terminal in Linux.
3. Create a directory.
```
mkdir your-directory && cd your-directory
```
4. Installation of python package installer (pip)
```
sudo apt update
sudo apt install python3pip
```
5. Installation of docker container for cloud deployment.
```
sudo apt install docker.io
```
6. Setting up a single node Cassandra inside a docker container.
Pulling for Cassandra docker image
```
sudo docker pull cassandra:latest
```
7. Run a Cassandra instance within a docker
```
sudo docker run --name cassandra-test -p 9042:9042 -d cassandra:latest
```
8. Calling dataset into the instance. 
country_currency.csv is hosted in my Git repository.
```
wget -O country_currency.csv https://tinyurl.com/sbj72fc
```
9. Check the first few lines and last few lines of downloaded CSV.
```
head country_currency.csv
tail country_currency.csv
```
10. Copy the dataset into container.
```
sudo docker cp country_currency.csv cassandra-test:/home/country_currency.csv
```
11. Interacting Cassandra via its native command line shell cliet 'cqlsh' using CQL (Cassandra Quert Language)
```
sudo docker exec -it cassandra-test cqlsh
```
12. Create keyspace for the data to be inserted into.
```
CREATE KEYSPACE country_currency WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
```
13. Specifying the name and type of column in keyspace
```
CREATE TABLE country_currency.stats (Number int, Country text PRIMARY KEY, Countrycode text, Currency text);
```
14. Copying the data from csv into the database.
```
COPY country_currency.stats(Number,Country,Countrycode,Currency)
FROM '/home/country_currency.csv'
WITH DELIMITER=',' AND HEADER=TRUE;
```
### Connecting Flask to Cassandra 
15. Open a new terminal with the same directory
```
cd your-directory
```
16. Create requirements.txt file and press F2 to save and exit. (Download from github)
```
nano requirements.txt
```
17. Create docker file and press F2 to save and exit.(Download from github)
```
nano Dockerfile
```
18. Create app.py file press F2 to save and exit.(Download from github)
```
nano app.py
```
The IP address is an example. Find the IP address of your container with following:
```
sudo docker inspect cassandra-test
```
19. Build the image
```
sudo docker build . --tag=cassandrarest:v1
```
20. Run the service
```
sudo docker run -p 80:80 cassandrarest:v1
```
### Sending Http request
1. Open a new terminal and change to current directory.
```
cd your-directory
```
To send POST Request
```
curl -i -H "Content-Type: application/json" -X POST -d '{"number":your-choice,"country":"your-choice","countrycode":"your-choice","currency":"your-choice"}' yourIP/unit
```

To send DELETE Request
```
curl -i -H "Content-Type: application/json" -X DELETE -d '{"country":"your-choice"}' yourIP/unit
```

## Resource:
1. [External API: Currency Layer](https://currencylayer.com/)
