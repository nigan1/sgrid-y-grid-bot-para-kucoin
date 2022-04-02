from kucoin.client import Client
import config
import time
import sys 
import decimal

client=Client(config.API_KEY,config.API_SECRET_KEY,config.API_PASSPHRASE)

par=client.get_ticker(config.SYMBOL)

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



print("Precio del par {}:{}".format(config.SYMBOL,par["price"]))

POSITION_SIZE=round(config.INVEST_SIZE/float(par["price"]), new_decimales_orderSize)

buy_orders=[]
sell_orders=[]

print("#####                                              INFO                                                ####")

#compra inicial
compra_inicial=client.create_market_order(config.SYMBOL,"BUY",round(POSITION_SIZE*config.NUM_SELL_GRID_LINES,new_decimales_orderSize))
print("se ha realizado una compra de "+str(round(POSITION_SIZE*config.NUM_SELL_GRID_LINES,new_decimales_precio))+" en el par de "+str(config.SYMBOL))


print("#####                                         ORDENES DE VENTA                                         ####")
#colocar ordenes de venta
for orden in range(config.NUM_SELL_GRID_LINES):
        precio=float(par["price"])+(config.GRID_SIZE*(orden+1))
        orden=client.create_limit_order(config.SYMBOL,"SELL",precio,POSITION_SIZE)
        sell_orders.append(orden["orderId"])
        print("Orden de VENTA colocada en {}".format(precio))



print("#####                                        ORDENES DE COMPRA                                         ####")
#colocar ordenes de compra
for orden in range(config.NUM_BUY_GRID_LINES):
        precio=float(par["price"])-(config.GRID_SIZE*(orden+1))
        new_POSITION_SIZE=round(config.INVEST_SIZE/float(precio), new_decimales_orderSize)
        orden=client.create_limit_order(config.SYMBOL,"BUY",precio,new_POSITION_SIZE)
        buy_orders.append(orden["orderId"])
        print("Orden de COMPRA colocada en {}".format(precio))

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
                        new_POSITION_SIZE=orderDetail['size']
                        new_sell_order=client.create_limit_order(config.SYMBOL,"SELL",new_price,new_POSITION_SIZE)
                        print("nueva orden de venta posicionada en {}".format(new_price))
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
                        new_POSITION_SIZE=orderDetail['size']
                        new_sell_order=client.create_limit_order(config.SYMBOL,"BUY",new_price,new_POSITION_SIZE)
                        print("nueva orden de compra posicionada en {}".format(new_price))
                        buy_orders.append(new_sell_order["orderId"])
                        sell_orders.remove(orderDetail["id"])

                time.sleep(config.CHECK_ORDERS_FREQUENCY)

        if len(sell_orders) == 0: 
                sys.exit("tomando ganancias, todas las ordenes de ventas ejecutadas")     