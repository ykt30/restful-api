# Implementing GET on database (WORK)
from flask import Flask, json, jsonify, request
import requests
import requests_cache
from cassandra.cluster import Cluster

# Cassandra configuration Docker connection
# 172.17.0.2 is the IP
# 'sudo docker inspect cassandra-test' to check your IP address for container
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()

# Initialising the app and the configuration.
app = Flask(__name__)

# Cache configuration
requests_cache.install_cache('forex_api_cache', backend='sqlite', expire_after=36000)

# Show homepage
@app.route('/')
def homepage():
    name = request.args.get("name","World")
    return '<h1>Hello, {}! Welcome to Live Currency and Historical Currency RESTful API'.format(name)

# GET database
@app.route('/unit', methods=['GET'])
def database():
    rows = session.execute("""Select * From country_currency.stats""")
    result = []
    for r in rows:
        result.append({"number":r.number,"country":r.country,"countrycode":r.countrycode,"currency":r.currency})
    return jsonify(result)

# POST database
@app.route('/unit', methods=['POST'])
def create ():
    session.execute("""INSERT INTO country_currency.stats(number, country, countrycode, currency) VALUES ( {},'{}','{}','{}')""".format(int(request.json['number']),request.json['country'],request.json['countrycode'],request.json['currency']))
    return jsonify({'message' : 'created: /unit/{}'.format(request.json['number'])}), 201

# DELETE database
@app.route('/unit', methods=['DELETE'])
def delete():
    session.execute("""DELETE FROM country_currency.stats WHERE number={}""".format(int(request.json['number'])))
    return jsonify({'message' : 'deleted: /unit/{}'.format(request.json['number'])}), 200

# CASSANDRA: Enquiry Currency Code ISO 4217 from Country Name
@app.route('/unit/<country>')
def profile1(country):
    rows = session.execute( """Select * From country_currency.stats where country = '{}'""".format(country))
    for country_currency in rows:
        return '<h1>{} ({}) currency code is {}!'.format(country,country_currency.countrycode,country_currency.currency)
    return '<h1> That country does not exist!'

# EXTERNAL API- GET Live Market exchange by currencylayer.com
@app.route('/livemarket', methods=['GET'])
def livemarket():
    livemarket_url_template = 'http://api.currencylayer.com/live?access_key={key}'
    my_key = 'd84a9c705051d6290ef19896f6dfff8f'
    livemarket_url = livemarket_url_template.format(key=my_key)
    resp = requests.get(livemarket_url)
    if resp.ok:
        return jsonify(resp.json()), 200
    else:
        print  (resp.reason), 404

# ETERNAL API- GET Historical Exchange data by currencylayer.com
@app.route('/historicalexchange', methods=['GET'])
def historical():
    historical_url_template = 'http://api.currencylayer.com/historical?access_key={key}&date={date}'
    my_key = 'd84a9c705051d6290ef19896f6dfff8f'
    my_date = '2020-04-01'
    historical_url = historical_url_template.format(key=my_key, date=my_date)
    resp = requests.get(historical_url)
    if resp.ok:
        return jsonify(resp.json()), 200
    else:
        print  (resp.reason), 404

# Create 404
@app.errorhandler(404)
def page_not_found(e):
    return "<h1> 404 </h1> <p> The resource could not be found. </p>", 404

# Run program
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
