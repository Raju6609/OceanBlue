import pytest
import os
from order_book_api import OrderBook, DF
from constants import ORDER_BOOK_DB

if os.path.exists(ORDER_BOOK_DB):
    os.remove(ORDER_BOOK_DB)

def test_process_order():

    #Order 1
    df_order_book = DF
    # Add
    order_book = OrderBook(message_format="delimited")
    order_book.process_order('1568390204|abbb11|a|AAPL|B|209.00000|100')
    assert len(OrderBook().get_orderbook()) == 1

    #Update
    order_book.process_order('1568390204|abbb11|u|10')
    assert len(OrderBook().get_orderbook()) == 1

    #Canel
    order_book.process_order('1568390204|abbb11|c')
    assert len(OrderBook().get_orderbook()) == 1

    #Live trade Status is not cancel
    df_order_book = OrderBook().get_orderbook()
    df_live = df_order_book[(df_order_book.action != "cancel") & (df_order_book.ticker == 'AAPL')]
    assert len(df_live) == 0

def test_getBestBidAndAsk():

    # Evaluated Best BID and ASK function call

    df_order_book = DF
    order_book = OrderBook(message_format="delimited")
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
            order_book.process_order(instruction)
        except Exception as ex:
            print(str(ex))

    assert str(OrderBook().getBestBidAndAsk()['best_bid']) == '299.00000'
    assert OrderBook().getBestBidAndAsk()['best_ask'] == '300.00000'


