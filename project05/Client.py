import json
from game_impl import Game

def handle_request(request):

    state = request.get("state", {})
    game = Game(board_data=state.get("board_data", {}), players_data=state.get("players", []))

    if request["request"] == "setup":
        response = game.setup(request["players"])
    elif request["request"] == "place":
        response = game.place(request["row"], request["column"], request.get("hotel"))
    elif request["request"] == "buy":
        response = game.buy(request["shares"], state)
    elif request["request"] == "done":
        response = game.generate_state()
    else:
        response = {"error": "Unknown request type."}


    if isinstance(response, dict) and ("error" in response or "impossible" in response):
        return response
    else:
        return game.generate_state()


if __name__ == "__main__":
    try:
        with open("/Users/aditithakkar/Desktop/oosd-personal/OOSDProject05/project05/demo.json", 'r') as file:
            request = json.load(file)
            response = handle_request(request)
            print(json.dumps(response, indent=2))  # Pretty print the response
    except FileNotFoundError:
        print("The file 'demo.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from 'demo.json'.")
