API_KEY = 
API_SECRET_KEY = ""
API_PASSPHRASE = ""


SYMBOL = "ETH-USDT"

INVERSION_TOTAL_USDT=300 #INVERSION TOTAL EN USDT PARA LOS BOTS

 
# gridbot settings
NUM_BUY_GRID_LINES = 5 #ordenes de compra
NUM_SELL_GRID_LINES = 5 #ordenes de venta
GRID_SIZE = 100 #diferencia de precios entre ordenes

CHECK_ORDERS_FREQUENCY = 0.5 #frecuencia para revisar las ordenes

INVEST_SIZE=INVERSION_TOTAL_USDT//(NUM_BUY_GRID_LINES+NUM_SELL_GRID_LINES) #cantidad en usd para comprar y vender en el sgrid
