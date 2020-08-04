# OceanBlue
OceanBlue is project code for OrderBook application


**Order Book - Application**

This Order book application enables to process Sell and Buy orders and system maintains a file based DB which allocumate
the new and modifed or cancelled orders.

This application has two main parts

Part I. **Back end - Python-Flask based REST API based application**
   
   1. localhost:port/orderbook
      Get list of orders in the database in presenetd in JSON format

   2. localhost:port/processorder
      Process any single order of any time add/update/cance;.
      Message format can be in JSON or pipe Delimited

   3. localhost:port/getbestbidask
      Get best ASK/BID prices in dictionary format.

    Others included test cases for OrderBook backend API


Part II. **Front end - Angular based single/dialog box based UI**

    1. List of orders from OrderBook
    Calls python RestAPI and get data using HttpClient and shows up in table

    2  Modify Orders (Not Working)
    Modifiy prder by submitting to UI

    2  Get Bid Ask price from RestAPI
    Get best Bid Ask price and display usng dialog box




