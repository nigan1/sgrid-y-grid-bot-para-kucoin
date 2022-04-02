from kucoin.client import Client
import config
import time
import sys 
import decimal


client=Client(config.API_KEY,config.API_SECRET_KEY,config.API_PASSPHRASE)

par=client.get_ticker(config.SYMBOL)
print("Precio del par {}:{}".format(config.SYMBOL,par["price"]))


order_book=client.get_order_book(par)
order_book_bids=order_book['bids'][0]
decimales_moneda=decimal.Decimal(order_book_bids[1])

buy_orders=[]
sell_orders=[]

print("#####                                              INFO                                                ####")

invest=config.INVEST_SIZE*config.NUM_SELL_GRID_LINES

#compra inicial
compra_inicial=client.create_market_order(config.SYMBOL,"BUY",size=None,funds=invest,client_oid=None,remark=None,stp=None,trade_type=None)
compra_inicialInfo=client.get_order(compra_inicial["orderId"])

print("se ha realizado una compra de "+str(compra_inicialInfo['dealSize'])+" en el par de "+str(config.SYMBOL))



print("#####                                         ORDENES DE VENTA                                         ####")
#colocar ordenes de venta
for orden in range(config.NUM_SELL_GRID_LINES):
        precio=float(par["price"])+(config.GRID_SIZE*(orden+1))
        orden_size=config.INVEST_SIZE/precio
        orden_size_round=round(orden_size, decimales_moneda)
        orden=client.create_limit_order(config.SYMBOL,"SELL",precio,orden_size_round)
        sell_orders.append(orden["orderId"])
        print("Orden de VENTA colocada en {},tamaño de la orden {}".format(precio, orden_size_round))



print("#####                                        ORDENES DE COMPRA                                         ####")
#colocar ordenes de compra
for orden in range(config.NUM_BUY_GRID_LINES):
        precio=float(par["price"])-(config.GRID_SIZE*(orden+1))
        orden_size=config.INVEST_SIZE/precio
        orden_size_round=round(orden_size, decimales_moneda)
        orden=client.create_limit_order(config.SYMBOL,"BUY",precio,orden_size_round)
        buy_orders.append(orden["orderId"])
        print("Orden de COMPRA colocada en {},tamaño de la orden {}".format(precio, orden_size_round))

print("#####                                        OPERACIONES DEL BOT                                         ####")

while True:
        
        for buy_order in buy_orders:
                try:
                        orderDetail=client.get_order(buy_order)
                except:
                        continue
                
                if orderDetail["isActive"]==False:
                        print("orden de compra ejecutada en {}".format(orderDetail["price"]))
                        new_price=float(orderDetail["price"])+config.GRID_SIZE
                        new_orden_size=config.INVEST_SIZE/new_price
                        new_orden_size_round=round(new_orden_size, decimales_moneda)
                        new_sell_order=client.create_limit_order(config.SYMBOL,"SELL",new_price,new_orden_size_round)
                        print("nueva orden de venta posicionada en {},tamaño de la orden {}".format(new_price,new_orden_size_round))
                        sell_orders.append(new_sell_order["orderId"])
                        buy_orders.remove(orderDetail["id"])

                time.sleep(config.CHECK_ORDERS_FREQUENCY)

        for sell_order in sell_orders:
                try:
                        orderDetail=client.get_order(sell_order)
                except:
                        continue
                
                if orderDetail["isActive"]==False:
                        print("orden de venta ejecutada en {}".format(orderDetail["price"]))
                        new_price=float(orderDetail["price"])-config.GRID_SIZE
                        new_orden_size=config.INVEST_SIZE/new_price
                        new_orden_size_round=round(new_orden_size, decimales_moneda)
                        new_sell_order=client.create_limit_order(config.SYMBOL,"BUY",new_price,new_orden_size_round)
                        print("nueva orden de compra posicionada en {},tamaño de la orden {}".format(new_price,new_orden_size_round))
                        buy_orders.append(new_sell_order["orderId"])
                        sell_orders.remove(orderDetail["id"])

                time.sleep(config.CHECK_ORDERS_FREQUENCY)

        if len(sell_orders) == 0: 
                sys.exit("tomando ganancias, todas las ordenes de ventas ejecutadas")