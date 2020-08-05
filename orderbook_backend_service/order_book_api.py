import os
import json
import decimal
import pandas as pd
from datetime import datetime
from constants import *  # Importing all constants as they are all used

DF = pd.DataFrame(data = [], columns=list(ORDER.keys()))


class OrderBook:

    def __init__(self, message_format="json"):
        self.order          = ORDER
        self.order_book     = self.get_orderbook()
        self.response       = PROCESS_RESPONSE
        self.message_format = message_format

    def validate_order(self):
        """
        Validation of order instructions
        :param order: dictionary of order instructions
        :return: validated order. if any issues, error raised
        """

        if not self.order.get('order_id'):  # Order id is mandatory
            raise (ERROR_MSG.format('Order Id'))
        if not self.order.get('order_id').isalnum():  # Order id has to be alpha numeric
            raise Exception(ERROR_MSG.format('Order Id  Format. Expected only alpha numeric'))
        if self.order.get('action') == 'add' and not self.order.get('side'):  # For add, side is mandatory
            raise Exception(ERROR_MSG.format('Sell Indicator'))
        if self.order.get('action') == 'add' and (not self.order.get('price') or self.order.get('price') <= 0):  # Price precision check
            raise Exception(ERROR_MSG.format('Price'))
        if self.order.get('action') == 'add' and str(self.order.get('price'))[::-1].find('.') != PRECISION:  # Price precision check
            raise Exception(ERROR_MSG.format('Price Format'))
        if self.order.get('action') in ['add', 'update'] and int(self.order.get('quantity')) <= 0:  # quantity validation
            raise Exception(ERROR_MSG.format('Quantity'))
        if self.order.get('action') == 'add' and not int(self.order.get('quantity')):  # Size validation
            raise Exception(ERROR_MSG.format('Ticker'))


    def order_instruction(self, order_message):
        """
        Parse the instruction into become order dict
        :param instruction: string format of instruction
        :return ORDER: order dictionary
        """
        try:
            if self.message_format == "delimited":
                _message = [val.strip() for val in order_message.split('|')]
                self.order['timestamp'] = datetime.utcfromtimestamp(int(_message[0])).strftime('%Y-%m-%d %H:%M:%S')
                self.order['order_id']  = _message[1]
                self.order['action']    = ACTIONS.get(_message[2])
                self.order['ticker']    = _message[3] if ORDER.get('action') == 'add' else None
                self.order['side']      = SIDE[_message[4]] if ORDER.get('action') == 'add' else None
                self.order['price']     = decimal.Decimal(_message[5]) if ORDER.get('action') == 'add' else None
                self.order['quantity']  = _message[6] if self.order.get('action') == 'add' else (_message[3] \
                                            if self.order.get('action') == 'update' else None)
            elif self.message_format == "json":
                _message = json.loads(order_message)
                self.order['timestamp'] = datetime.utcfromtimestamp(int(_message['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
                self.order['order_id'] = _message['order_id']
                self.order['action'] = ACTIONS.get(_message['action'])
                self.order['ticker'] = _message.get('ticker')
                self.order['side'] = SIDE[_message.get('side')]
                self.order['price'] = decimal.Decimal(_message.get('price')) if _message.get('price')  else None
                self.order['quantity'] = _message.get('quantity')
            self.validate_order()
        except Exception as ex:
            self.response["error_msg"] = str(ex)
            self.response["status"] = "fail"

    def presist_orderbook(self):
        self.order_book['price'] = self.order_book['price'].astype('str')
        self.order_book.to_hdf(ORDER_BOOK_DB, 'order_book', append=False)
        self.order = None # Clear order once persisted

    @staticmethod
    def get_orderbook():
        return pd.read_hdf(ORDER_BOOK_DB, 'order_book') if os.path.exists(ORDER_BOOK_DB) else DF

    def process_order(self, order_message):
        """
        Process order messages : Instructions
        :param instruction:
        :return:
        """
        try:
            self.order = ORDER
            self.order_instruction(order_message)
            order_id_exists = True if self.order['order_id'] in  self.order_book.order_id.values else False

            if self.order.get('action') == "add":  # Add
                if order_id_exists:  # Check if order id exists
                    raise Exception(ERROR_MSG.format("Order ID. Order ID already exists"))
                self.order_book = self.order_book.append(self.order, ignore_index=True)
            else:
                if not order_id_exists:  # Check if order id exists
                    raise Exception(ERROR_MSG.format("Order ID. Order ID doesnt exists to amend"))

                if self.order.get('action') == "update":  # update
                    self.order_book.loc[ self.order_book['order_id'] == self.order['order_id'], ['action', 'quantity', 'timestamp']] = \
                        self.order['action'], self.order['quantity'], self.order['timestamp']
                elif self.order['action'] == "cancel":  # cancel
                    self.order_book.loc[ self.order_book['order_id'] == self.order['order_id'], ['action', 'timestamp']] = \
                        self.order['action'], self.order['timestamp']
            self.presist_orderbook()
        except Exception as ex:
            self.response["error_msg"] = str(ex)
            self.response["status"] = "fail"
            raise Exception("Order Processing Error. Error Message: {msg}.".format(msg=str(ex)))
        finally:
            if not self.response["error_msg"]:
                self.response["status"] = "success"

    @staticmethod
    def getBestBidAndAsk():
        """
        getBid Best Bid and Ask Prices from oder book
        :return: Dictiionay containing bestbid and bestask
        """
        df_orderbook = OrderBook.get_orderbook()

        df_bid = df_orderbook[(df_orderbook.action != ACTIONS.get('c')) & (df_orderbook.side == SIDE.get('S'))]
        df_bid.astype({'price': 'float32'})
        _best_bid = min(df_bid.price.values)

        df_ask = df_orderbook[(df_orderbook.action != ACTIONS.get('c')) & (df_orderbook.side == SIDE.get('B'))]
        df_ask.astype({'price': 'float32'})
        _best_ask = max(df_ask.price.values)

        return {"best_bid": _best_bid, "best_ask": _best_ask}


if __name__== "__main__":

    if os.path.exists(ORDER_BOOK_DB):
        os.remove(ORDER_BOOK_DB)  # Clean up for testing

    order_book   = OrderBook(message_format="delimited")
    instructions = ['1568390201|abbb11|a|AAPL|B|209.00000|100',
                    '1568390202|abbb12|a|AAPL|S|210.00000|10',
                    '1568390204|abbb11|u|10',
                    '1568390203|abbb12|u|101',
                    '1568390243|abbb12|c',
                    '1568390243|abbb13|a|AAPL|B|209.00000|100',
                    '1568390244|abbb13|u|101',
                    '1568390245|abbb13|c',
                    '1568390243|abbb14|a|AAPL|B|300.00000|150',
                    '1568390243|abbb15|a|AAPL|S|299.00000|120']
    for instruction in instructions:
        try:
            response = order_book.process_order(instruction)
        except Exception as ex:
            print(str(ex))
        print(order_book.response)
