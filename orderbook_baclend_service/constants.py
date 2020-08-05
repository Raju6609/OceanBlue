ORDER_BOOK_DB = "order_book_db.h5"

PROCESS_RESPONSE = { "status" : None , "error_msg": None }
ERROR_MSG = 'Invalid {}. Please correct and resend'
PRECISION = 5
ACTIONS   = {'a': 'add', 'u': 'update', 'c': 'cancel'}
SIDE      = {'B': 'buy', 'S': 'ask'}
ORDER     = {
                'order_id'      : None,
                'action'        : None,
                'ticker'        : None,
                'side'          : None,
                'price'         : None,
                'quantity'      : None,
                'timestamp'     : None
}



