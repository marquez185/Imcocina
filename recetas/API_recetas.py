import requests
import random

# Configura tus credenciales de Edamam
# app_id = '47feccff'
# app_key = '8a0789f66cca1de26802c29469689e28'
app_id = '54866250'
app_key = '9ae82763987957791cf01e17edf276ea'

# Define la función para buscar recetas
def obtener_recetas(ingredientes, diet, health, cuisineType, mealType, dishType, calories_min, calories_max, time):
    url = "https://api.edamam.com/search"
    params = {
        'q': ingredientes,
        'app_id': app_id,  # Reemplaza con tu app_id
        'app_key': app_key,  # Reemplaza con tu app_key
    }

    # Añadir parámetros opcionales si no están vacíos y son válidos
    if diet in ['balanced', 'high-fiber', 'high-protein', 'low-carb', 'low-fat', 'low-sodium']:
        params['diet'] = diet
    if health in ['alcohol-cocktail', 'alcohol-free', 'celery-free', 'crustacean-free', 'dairy-free', 'DASH', 
                  'egg-free', 'fish-free', 'fodmap-free', 'gluten-free', 'immuno-supportive', 'keto-friendly', 
                  'kidney-friendly', 'kosher', 'low-fat-abs', 'low-potassium', 'low-sugar', 'lupine-free', 
                  'Mediterranean', 'mollusk-free', 'mustard-free', 'no-oil-added', 'paleo', 'peanut-free', 
                  'pescatarian', 'pork-free', 'red-meat-free', 'sesame-free', 'shellfish-free', 'soy-free', 
                  'sugar-conscious', 'sulfite-free', 'tree-nut-free', 'vegan', 'vegetarian', 'wheat-free']:
        params['health'] = health
    if cuisineType:  # Validar según sea necesario
        params['cuisineType'] = cuisineType
    if mealType in ['Breakfast', 'Dinner', 'Lunch', 'Snack', 'Teatime']:
        params['mealType'] = mealType
    if dishType:  # Validar según sea necesario
        params['dishType'] = dishType
    if calories_min and calories_max:
        params['calories'] = f'{calories_min}-{calories_max}'
    elif calories_min:
        params['calories'] = f'{calories_min}+'
    elif calories_max:
        params['calories'] = f'{calories_max}'
    if time:
        params['time'] = time

    # Print the parameters to ensure they are correct
    print("Request Parameters:", params)
    
    response = requests.get(url, params=params)
    try:
        data = response.json()
    except ValueError:
        data = {}
    
    # Print the API response for debugging
    # print("API Response:", data)

    # Verificar si la respuesta es una cadena de error
    if isinstance(data, str):
        print("Error from API:", data)
        return []
    

    # Transformar los datos para que se ajusten al template
    recetas = []
    for receta in data.get('hits', []):
        recetas.append({
            'nombre': receta['recipe']['label'],
            'imagen': receta['recipe']['image'],
            'link': receta['recipe']['url'],
            'calorias': receta['recipe']['calories'],
            'nutrientes': receta['recipe']['totalNutrients']
        })
        
    return recetas

# Define la funcion para recetas aleatorias en el index
def buscar_recetas_aleatorias(num_recetas=8):
    url = 'https://api.edamam.com/api/recipes/v2'
    consultas = ['chicken', 'beef', 'vegetarian', 'pasta', 'dessert']
    query = random.choice(consultas)
    
    params = {
        'type': 'public',
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
        'random': 'true',
        'to': num_recetas
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        recetas = []
        for hit in data['hits'][:num_recetas]:
            receta = hit['recipe']
            recetas.append({
                'nombre': receta['label'],
                'imagen': receta['image'],
                'link': receta['url']
            })
        return recetas
    else:
        print(f"Error: {response.status_code}")
        return None

def buscar_recetas_ingredientes(ingredientes, num_recetas=5):
    url = 'https://api.edamam.com/api/recipes/v2'
    query = ','.join(ingredientes.split(','))  # Separar los ingredientes por comas
    
    params = {
        'type': 'public',
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
        'random': 'true',
        'to': num_recetas
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        recetas = []
        for hit in data['hits'][:num_recetas]:
            receta = hit['recipe']
            recetas.append({
                'nombre': receta['label'],
                'imagen': receta['image'],
                'link': receta['url']
            })
        return recetas
    else:
        print(f"Error: {response.status_code}")
        return None



'''# Ejemplo de uso
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
    print("No se encontraron recetas.")'''


