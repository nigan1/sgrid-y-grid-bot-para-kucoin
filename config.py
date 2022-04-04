API_KEY = ""
API_SECRET_KEY = ""
API_PASSPHRASE = ""


SYMBOL = "BTC-USDT"

INVERSION_TOTAL_USDT=300 #INVERSION TOTAL EN USDT PARA LOS BOTS

# gridbot settings
MAX_RANGE=50000
MIN_RANGE=40000


GRID_AMOUNT=50 #grid para ponerle al bot
GRID_SIZE = int(MAX_RANGE-MIN_RANGE)//GRID_AMOUNT     #diferencia de precios entre ordenes

CHECK_ORDERS_FREQUENCY = 0.5 #frecuencia para revisar las ordenes

INVEST_SIZE=INVERSION_TOTAL_USDT//GRID_AMOUNT #cantidad en usd para comprar y vender en el sgrid
