from kucoin.client import Client
import config
import time
import sys 

client=Client(config.API_KEY,config.API_SECRET_KEY,config.API_PASSPHRASE)

par=client.get_ticker(config.SYMBOL)
print("Precio del par {}:{}".format(config.SYMBOL,par["price"]))

POSITION_SIZE=round(config.INVERSION_TOTAL_USDT/float(par["price"]), config.ROUN_ORDER)

buy_orders=[]
sell_orders=[]

print("#####                                              INFO                                                ####")

#compra inicial
compra_inicial=client.create_market_order(config.SYMBOL,"BUY",POSITION_SIZE*config.NUM_SELL_GRID_LINES)
print("se ha realizado una compra de "+str(POSITION_SIZE*config.NUM_SELL_GRID_LINES)+" en el par de "+str(config.SYMBOL))



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
        orden=client.create_limit_order(config.SYMBOL,"BUY",precio,POSITION_SIZE)
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
                        new_sell_order=client.create_limit_order(config.SYMBOL,"SELL",new_price,POSITION_SIZE)
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
                        new_sell_order=client.create_limit_order(config.SYMBOL,"BUY",new_price,POSITION_SIZE)
                        print("nueva orden de compra posicionada en {}".format(new_price))
                        buy_orders.append(new_sell_order["orderId"])
                        sell_orders.remove(orderDetail["id"])

                time.sleep(config.CHECK_ORDERS_FREQUENCY)

        if len(sell_orders) == 0: 
                sys.exit("tomando ganancias, todas las ordenes de ventas ejecutadas")     
