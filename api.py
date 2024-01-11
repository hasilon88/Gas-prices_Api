from flask import Flask
from flask_cors import CORS, cross_origin
from gas_prices import get_gas_info

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def landingPage():
  return """
            Hello, to get gas prices and other info, please add the province and the city in the URL <br/>
            For example: /ontario/toronto
        """

@cross_origin()
@app.get('/<province>/<city>')
def get_info(province, city):
    return get_gas_info(province, city)
 
 
# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server
    app.run(debug=True)