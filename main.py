import requests
import json
from bs4 import BeautifulSoup


def get_recipe(url):
    client = requests.session()
    client.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    })

    r = client.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    all_data = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).contents[0])
    recipeSchema = all_data['props']['pageProps']['recipeSchema']
    ingred_info = all_data['props']['pageProps']['ingredients'][0]['ingredients']

    res = {}
    res['name'] = recipeSchema['name']

    assert len(recipeSchema['recipeIngredient']) == len(ingred_info)
    ingred_list = []
    for ingredientText, info in zip(recipeSchema['recipeIngredient'], ingred_info):
        ingred_list.append({
            'ingredientText': ingredientText,
            'quantityText': info.get('quantityText', None),
            'term': info['term']['display'],
        })
    res['ingredients'] = ingred_list

    instructions = []
    for instr in recipeSchema['recipeInstructions']:
        temp_soup = BeautifulSoup(instr['text'], 'html.parser')
        instructions.append(temp_soup.get_text())
    res['instructions'] = instructions
    return res


url = input()
recipe = get_recipe(url)

print(json.dumps(recipe, indent=4))
