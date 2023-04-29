from getIntentId import getIntentId
from getProdResponse import getProdResponse
from flask import Flask
from flask_cors import CORS
import logging
import ssl

app = Flask(__name__)
CORS(app)


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('key/39b22c7467e72f9e.crt', 'key/hyreo.key')

logger = logging.getLogger(__name__)

app.add_url_rule('/intent', view_func=getIntentId.get_intent_id, methods=['GET'])
app.add_url_rule('/get_prod_response', view_func=getProdResponse.get_prod_response, methods=['GET'])


@app.route("/")
def index():
    response = Flask.response_class()
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':

    app.run('0.0.0.0', '5001', debug=True, ssl_context=context)
