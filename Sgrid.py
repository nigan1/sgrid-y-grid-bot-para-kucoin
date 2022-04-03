from kucoin.client import Client
import config
import time
import sys 
import decimal


client=Client(config.API_KEY,config.API_SECRET_KEY,config.API_PASSPHRASE)

par=client.get_ticker(config.SYMBOL)
print("Precio del par {}:{}".format(config.SYMBOL,par["price"]))

#consulto todos los pares comerciales
symbols=client.get_symbols()

#extraigo los decimales de tamaño de orde y de precio de la moneda que voy a trabajar
for element in symbols:
    if element['symbol']==config.SYMBOL:
        decimales_orderSize=element['baseIncrement']
        decimales_precio=element['priceIncrement']

new_decimales_precio=decimal.Decimal(decimales_precio)
new_decimales_orderSize=decimal.Decimal(decimales_orderSize)

new_decimales_precio=new_decimales_precio.as_tuple().exponent*-1
new_decimales_orderSize=new_decimales_orderSize.as_tuple().exponent*-1


buy_orders=[]
sell_orders=[]

print("#####                                              INFO                                                ####")

invest=int(config.INVEST_SIZE*config.NUM_SELL_GRID_LINES)

#compra inicial
compra_inicial=client.create_market_order(config.SYMBOL,"BUY",size=None,funds=round(invest,new_decimales_precio),client_oid=None,remark=None,stp=None,trade_type=None)
compra_inicialInfo=client.get_order(compra_inicial["orderId"])

print("se ha realizado una compra de "+str(compra_inicialInfo['dealSize'])+" en el par de "+str(config.SYMBOL))



print("#####                                         ORDENES DE VENTA                                         ####")
#colocar ordenes de venta
for orden in range(config.NUM_SELL_GRID_LINES):
        precio=round(float(par["price"])+(config.GRID_SIZE*(orden+1)),new_decimales_precio)
        orden_size=config.INVEST_SIZE/precio
        orden_size_round=round(orden_size, new_decimales_orderSize)
        orden=client.create_limit_order(config.SYMBOL,"SELL",precio,orden_size_round)
        sell_orders.append(orden["orderId"])
        print("Orden de VENTA colocada en {},tamaño de la orden {}".format(precio, orden_size_round))



print("#####                                        ORDENES DE COMPRA                                         ####")
#colocar ordenes de compra
for orden in range(config.NUM_BUY_GRID_LINES):
        precio=round(float(par["price"])-(config.GRID_SIZE*(orden+1)),new_decimales_precio)
        orden_size=config.INVEST_SIZE/precio
        orden_size_round=round(orden_size, new_decimales_orderSize)
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
                        new_price=round(float(orderDetail["price"])+config.GRID_SIZE,new_decimales_precio)
                        new_orden_size=config.INVEST_SIZE/new_price
                        new_orden_size_round=round(new_orden_size, new_decimales_orderSize)
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
                        new_price=round(float(orderDetail["price"])-config.GRID_SIZE,new_decimales_precio)
                        new_orden_size=config.INVEST_SIZE/new_price
                        new_orden_size_round=round(new_orden_size, new_decimales_orderSize)
                        new_sell_order=client.create_limit_order(config.SYMBOL,"BUY",new_price,new_orden_size_round)
                        print("nueva orden de compra posicionada en {},tamaño de la orden {}".format(new_price,new_orden_size_round))
                        buy_orders.append(new_sell_order["orderId"])
                        sell_orders.remove(orderDetail["id"])

                time.sleep(config.CHECK_ORDERS_FREQUENCY)

        if len(sell_orders) == 0: 
                sys.exit("tomando ganancias, todas las ordenes de ventas ejecutadas")
