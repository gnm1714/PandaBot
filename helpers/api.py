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
    quote = "Here's your panda uwu: " + json_data["link"]
    return (quote)


# Gets a random undertale goat picture and sends back to the async
def get_goat():
    response = requests.get("http://0.0.0.0:8081/")
    json_data = json.loads(response.text)
    quote = "Here's your goat uwu: " + json_data[0]["link"]
    return (quote)
