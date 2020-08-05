import json
import flask
from flask import request, jsonify
from order_book_api import OrderBook
from flask_cors import CORS

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/processorder', methods=['post'])
def process_order():
    """
    This endpoint recieved requests for Add/Update/Cancel requests as post body
    application-json is inpur
    :return: {isProcessed: True/False, error_msg: True/False}
    """
    order_message   = request.get_json()
    orderbook       = OrderBook(message_format="json")
    orderbook.order_instruction(order_message)
    return jsonify( orderbook.process_order())



@app.route('/orderbook', methods=['GET'])
def get_orderbook():
    df = OrderBook().get_orderbook()
    df.reset_index(drop=True, inplace=True)
    df = df.to_dict(orient="index").values()
    return json.dumps(list(df))



@app.route('/getbestbidask', methods=['GET'])
def get_bestbidask():
    return jsonify(OrderBook().getBestBidAndAsk())



if __name__ == '__main__':
    app.run()
