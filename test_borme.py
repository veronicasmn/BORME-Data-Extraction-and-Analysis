from datetime import datetime, timedelta
from pdf_borme_new import get_borme_data  

borme_date = ''
provinces = ['', '']

# Obtener la fecha de ayer
today = datetime.now()
yesterday = today - timedelta(days=1)
borme_date = yesterday.strftime('%Y%m%d')  # Usa la fecha de ayer

# Inicializar una lista para almacenar los posibles openings
possible_openings = []
for province in provinces:
    possible_openings += get_borme_data(borme_date, province)

# Añadir un id a cada apertura
for i, opening in enumerate(possible_openings):
    opening['id'] = i

# Mostrar los resultados
for opening in possible_openings:
    print(opening)

