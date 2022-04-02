from kucoin.client import Client
import config

client=Client(config.API_KEY,config.API_SECRET_KEY,config.API_PASSPHRASE)


order=client.get_orders(status='active',symbol='BTC-USDT')

ordenes=order['items']

ordenes_venta=[]
ordenes_compra=[]

for element in ordenes:
        if element['side']=='sell':
                ordenes_venta.append(element['id'])
        else:
                ordenes_compra.append(element['id'])


print("tiene un total de {} ordenes abiertas, {} de venta y {} de compra.".format(len(ordenes_venta)+len(ordenes_compra),
                        len(ordenes_venta),len(ordenes_compra)))