import requests
import json

# Gets a random inspiration quote and sends back to the async
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return (quote)


# Gets a random red panda picture and sends back to the async
def get_panda():
    response = requests.get("https://some-random-api.ml/img/red_panda")
    json_data = json.loads(response.text)
    quote = json_data["link"]
    return (quote)


# Gets a random cat panda picture and sends back to the async
def get_cat():
    response = requests.get("https://cataas.com/cat?json=true")
    json_data = json.loads(response.text)
    quote = "https://cataas.com" + json_data["url"]
    return (quote)
