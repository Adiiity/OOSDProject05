import json
from game_impl import Game

def handle_request(request):

    state = request.get("state", {})
    # Assuming "state" contains "board" directly, not "board_data"
    board_data = state.get("board", {})  # Adjusted to "board" if that's what the state contains
    players_data = state.get("players", [])

    # Initialize Game with potentially updated keys
    game = Game(board_data=board_data, players_data=players_data)

    # Process the request
    if request["request"] == "setup":
        # Setup might need to only receive player names, not the detailed state
        response = game.setup(players_data)  # Assuming setup is correctly implemented to handle this
    elif request["request"] == "place":
        response = game.place(request["row"], request["column"], request.get("hotel"))
    elif request["request"] == "buy":
        response = game.buy(request["shares"])
    elif request["request"] == "done":
        response = game.done()  # Assuming a method done() that wraps generate_state() or similar logic
    else:
        response = {"error": "Unknown request type."}


    if isinstance(response, dict) and ("error" in response or "impossible" in response):
        return response
    else:
        return game.generate_state()


if __name__ == "__main__":
    try:
        with open("/Users/aditithakkar/Desktop/oosd-personal/OOSDProject05/project05/demo1.json", 'r') as file:
            request = json.load(file)
            response = handle_request(request)
            print(json.dumps(response, indent=2))  # Pretty print the response
    except FileNotFoundError:
        print("The file 'demo.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from 'demo.json'.")

# admin-tester/state-tests/in2.json