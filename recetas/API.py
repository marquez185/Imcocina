import requests

# Configura tus credenciales de Edamam
app_id = '47feccff'
app_key = '8a0789f66cca1de26802c29469689e28'

# Define la función para buscar recetas
def buscar_recetas(query):
    url = 'https://api.edamam.com/api/recipes/v2'
    
    # Parámetros de consulta
    params = {
        'type': 'public',  # Tipo de receta (public, user, any)
        'q': query,  # Texto de consulta
        'app_id': app_id,
        'app_key': app_key,
        'diet': ['low-carb'],  # Opcional: etiquetas de dieta
        'health': ['gluten-free'],  # Opcional: etiquetas de salud
        'cuisineType': ['Mexican'],  # Opcional: tipo de cocina
        'mealType': ['Dinner'],  # Opcional: tipo de comida
        'dishType': ['Main course'],  # Opcional: tipo de plato
        'calories': '100-500',  # Opcional: rango de calorías
        'time': '1-60',  # Opcional: rango de tiempo en minutos
        'random': 'false'  # Opcional: seleccionar recetas aleatorias
    }
    
    response = requests.get(url, params=params)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

# Ejemplo de uso
query = 'chicken'
recetas = buscar_recetas(query)

# Mostrar los resultados
if recetas:
    for hit in recetas['hits']:
        receta = hit['recipe']
        print(f"Título: {receta['label']}")
        print(f"Fuente: {receta['source']}")
        print(f"URL: {receta['url']}")
        print(f"Calorías: {receta['calories']:.2f}")
        print(f"Ingredientes: {', '.join(receta['ingredientLines'])}")
        print("\n")
else:
    print("No se encontraron recetas.")
