import json
from game_impl import Game

def handle_request(request):
# Initialize variables to hold board and player data if they exist in the state
    board_data = None
    players_data = None

    # Check if state is provided and extract board and players data from it
    if "state" in request:
        state = request["state"]
        board_data = state.get("board", {})
        players_data = state.get("players", [])
    else:
        state = {}

    # Initialize the Game instance differently based on the request type
    if request["request"] == "setup":
        # For setup, use players data directly from the request, not from the state
        players_data = request["players"]
        game = Game(board_data={}, players_data=players_data)
        response = game.setup(players_data)
    else:
        # For other requests, initialize Game with state data
        game = Game(board_data=board_data, players_data=players_data)

        # Process other requests
        if request["request"] == "place":
            response = game.place(request["row"], request["column"], request.get("hotel"))
        elif request["request"] == "buy":
            response = game.buy(request["shares"])
        elif request["request"] == "done":
            response = game.done() 
        else:
            response = {"error": "Unknown request type."}

    # Return the response
    if isinstance(response, dict) and ("error" in response or "impossible" in response or "msg" in response):
        return response
    else:
        return game.generate_state()

if __name__ == "__main__":
    try:
        with open("admin-tester/state-tests/in0.json", 'r') as file:
            request = json.load(file)
            response = handle_request(request)
            print(json.dumps(response, indent=2))  # Pretty print the response
    except FileNotFoundError:
        print("The file 'demo.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from 'demo.json'.")
