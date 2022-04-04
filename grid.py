from kucoin.client import Client
import config
import time
import sys 
import decimal
import telegram_send


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


#####                                        ORDENES DE COMPRA                                         ####

cant_orden_compra=0

while True:
    precio=round(config.MIN_RANGE+(config.GRID_SIZE*cant_orden_compra),new_decimales_precio)
    orden_size_round=round(config.INVEST_SIZE/precio, new_decimales_orderSize)
    orden=client.create_limit_order(config.SYMBOL,"BUY",precio,orden_size_round)
    buy_orders.append(orden["orderId"])
    print("Orden de COMPRA colocada en {},tamaño de la orden {}".format(precio, orden_size_round))
    cant_orden_compra=cant_orden_compra+1
    
    if precio+config.GRID_SIZE>=float(par["price"])-config.GRID_SIZE:
        break

#####                                         ORDENES DE VENTA                                         ####
cant_orden_ventas=1


while True:
    precio=round(float(par["price"])+(config.GRID_SIZE*cant_orden_ventas),new_decimales_precio)
    orden_size_round=round(config.INVEST_SIZE/precio, new_decimales_orderSize)
    client.create_market_order(config.SYMBOL,"BUY",orden_size_round)
    orden=client.create_limit_order(config.SYMBOL,"SELL",precio,orden_size_round)
    sell_orders.append(orden["orderId"])
    print("Orden de VENTA colocada en {},tamaño de la orden {}".format(precio, orden_size_round))
    cant_orden_ventas=cant_orden_ventas+1

    if precio+config.GRID_SIZE>=config.MAX_RANGE:
        break



#####                                        OPERACIONES DEL BOT                                         ####

while True:
        try:
        
                for buy_order in buy_orders:
                
                        orderDetail=client.get_order(buy_order)
                
                
                        if orderDetail["isActive"]==False:
                        
                                new_price=round(float(orderDetail["price"])+config.GRID_SIZE,new_decimales_precio)
                                new_POSITION_SIZE=orderDetail['size']
                                new_sell_order=client.create_limit_order(config.SYMBOL,"SELL",new_price,new_POSITION_SIZE)
                        
                                telegram_send.send(messages=["orden de compra ejecutada en {},nueva orden de venta en {}".format(orderDetail["price"],new_price)])
                                sell_orders.append(new_sell_order["orderId"])
                                buy_orders.remove(orderDetail["id"])

                        time.sleep(config.CHECK_ORDERS_FREQUENCY)

                for sell_order in sell_orders:
                
                        orderDetail=client.get_order(sell_order)
                
                
                
                        if orderDetail["isActive"]==False:
                       
                                new_price=round(float(orderDetail["price"])-config.GRID_SIZE,new_decimales_precio)
                                new_POSITION_SIZE=orderDetail['size']
                                new_sell_order=client.create_limit_order(config.SYMBOL,"BUY",new_price,new_POSITION_SIZE)
                        
                                telegram_send.send(messages=["orden de venta ejecutada en {},nueva orden de compra en {}".format(orderDetail["price"],new_price)])
                                buy_orders.append(new_sell_order["orderId"])
                                sell_orders.remove(orderDetail["id"])

                        time.sleep(config.CHECK_ORDERS_FREQUENCY)

                if len(sell_orders) == 0: 
                        telegram_send.send(messages=["tomando ganancias, todas las ordenes de ventas ejecutadas"])
                        sys.exit("tomando ganancias, todas las ordenes de ventas ejecutadas")     
        
                if len(buy_orders) == 0: 
                        telegram_send.send(messages=["ha bajado el precio fuera del rango del bot"])
        except:
                telegram_send.send(messages=["el bot ha dado error por algun motivo, reviselo!"])