###### REST API developed for QMUL (Queen Mary University of London) ECECS781P CLOUD COMPUTING(2019/20) Mini-Project

This RESTful Application Program Interface (API) is developed using Python and Flask. It provides a simple REST API with **real-time, historical exchange rates and currency details for 168 world currencies**, delivering currency pairs in universally usable JSON format. 

### Mini Project aims and objectives
Overall this mini project successfully implements following features:
1. Dynamically generated REST-based service interface.
2. Interaction with external REST services to complement its functionality. [currencylayer](https://currencylayer.com/)
3. Use of on an external Cloud database for persisting information. [country-currency](https://tinyurl.com/sbj72fc)
4. Cassandra ring scaling for cloud scalability, deployment in a container environment.  
5. Supports HTTP request: GET, POST, DELETE requests.

### How to set-up for using Terminal (Linux)
1. Open terminal in Linux.
2. Create a directory.
```
mkdir your-directory && cd your-directory
```
3. Installation of python package installer (pip)
```
sudo apt update
sudo apt install docker io
```

### Resources:
1. [Currency Layer](https://currencylayer.com/)
