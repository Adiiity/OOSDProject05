from game_library import Board,Tile,Player
class Game:
    def __init__(self,board_data,players_data=[]) -> None:

        self.board = Board()
        if board_data:
            self.board.process_board_data(board_data)
        self.players = [Player(name, 6000) for name in players_data]

    def generate_state(self):
        board_state = self.generate_board_state()
        players_state = self.generate_players_state()
        return {"board": board_state, "players": players_state}

    def generate_board_state(self):
        hotels = []
        standalone_tiles = []

        # Process hotel tiles
        for hotel_name, hotel_tiles in self.board.played_hotels.items():
            if hotel_tiles:  # Ensure we only include hotels with tiles
                formatted_tiles = [{"row": chr(row + ord('A')), "column": col + 1} for row, col in hotel_tiles]
                hotels.append({"hotel": hotel_name, "tiles": formatted_tiles})

        # Add tiles not part of any hotel
        for (row_index, col_index), hotel_name in self.board.played_tiles.items():
            board_tiles = {"row": chr(row_index + ord('A')), "column": col_index + 1}
            standalone_tiles.append(board_tiles)

        return {"tiles": standalone_tiles, "hotels": hotels}


    def generate_players_state(self):
        return [{
            "player": player.name,
            "cash": player.cash,
            "shares": [{"share": share.hotel_label, "count": share.count} for share in player.shares],
            "tiles": [{"row": tile.row, "column": tile.col} for tile in player.tiles]
        } for player in self.players]


    # def setup_players(self, player_names):
    #     players = []
    #     for name in player_names:
    #         player = Player(name)
    #         players.append(player)
    #     return players

    def singleton(self,row,col):

        tile = Tile(str(row), str(col))
        row_index, col_index = tile.get_row_index(),tile.get_col_index()


        if 0 <= row_index < self.board.rows and 0 <= col_index < self.board.cols:
            if self.board.board_matrix[row_index][col_index] == 0:  #checking if the tile is unoccupied
                self.board.board_matrix[row_index][col_index] = 1
                self.board.played_tiles[row_index,col_index] = None  #for now just keeping the value as None
                print("Singleton")
                return "singleton"
            else:
                return {"error" : "Tile is already played."}

        else:
              return {"error": "Invalid Tile"}



    def founding(self,row,column,label, board):

        game_board = board
        total_rows = len(game_board)
        total_cols = len(game_board[0])
        tile=Tile(row,column)
        current_row_num = tile.get_row_index()
        current_col_num = tile.get_col_index()


        #  neighbors indices
        delRow = [ -1, 0, +1, 0 ]
        delCol = [ 0, +1, 0, -1 ]


        # task 1: Check if the given grid is empty else return error.
        if(game_board[current_row_num][current_col_num] ==1):
            return {"error":"Tile is already occupied"}

        #  TASK 2: check if there is  any tile as neighbor to the given grid.
        else:
            neighbour_tiles = []
            for i in range(4):
                # adding valid indices only to neighbor tiles
                next_row =  current_row_num+delRow[i]
                next_col =  current_col_num+delCol[i]
                if(next_row>=0 and next_row<total_rows and next_col>=0 and next_col<total_cols):
                        neighbour_tiles.append((next_row,next_col))



# We must found a hotel if the neighbour single tiles are occupied. '0' tiles can be single as well, we must ignore it.
            occupied_neighbour = False
            for i,j in neighbour_tiles:

                row_index = i
                column_index = j

                if game_board[row_index][column_index] != 1:
                    continue


                else:
                    occupied_neighbour = True
                    isSingleTile =self.singleTile(row_index,column_index,delRow,delCol,game_board,total_rows,total_cols)

                    if isSingleTile:
                        if label in self.availableHotels:

                            # make the given indices by user as tile
                            self.singleton(row,column)


                            if label not in self.occupied_hotels:
                                # create a key with hotel name
                                self.occupied_hotels[label] = []
                                letter_row_ascii_number = ord('A') + row_index
                                letter_row = chr(letter_row_ascii_number)
                                # add the given tile and the single tile to this key
                                self.occupied_hotels[label].append((letter_row,column_index + 1))
                                self.occupied_hotels[label].append((row,column))

                                # change occupied tiles as well. add hotel label now

                                # update given row and col
                                self.board.playe_tiles[row,column] = label
                                # update teh single neighbour tile

                                self.board.played_tiles[letter_row,column_index + 1] = label



                                # remove the label from available hotels
                                self.availableHotels.remove(label)


                            return "founding"
                    # If there are no available hotel chains, the player can place the tile but cannot found a new hotel
                    elif label not in self.availableHotels:
                        # print("The given hotel label is not present in the available hotel chains. So adding tile only")
                        # we create and place the tile
                        self.singleton(row,column)

                        return

            if occupied_neighbour == False:

                return {"error": "Hotels can be found next to singly occupied tiles only"}

    def singleTile(self,row,column,delRow,delCol,game_board,total_rows,total_cols):

        for i in range(4):
            next_row =  row+delRow[i]
            next_col =  column+delCol[i]
            if( next_row>=0 and next_row<total_rows and next_col>=0 and next_col<total_cols ):
                if(game_board[next_row][next_col]!=0):
                    return False


        return True

    def growing(self, row, col):
        tile = Tile(str(row), str(col))
        row_index, col_index = tile.get_row_index(), tile.get_col_index()
        tile_tuple = (row_index, col_index)  # Use 0-based indices for internal tracking


        # Check if the tile is already played
        if tile_tuple in self.board.played_tiles:
            # If the tile is already associated with a hotel, raise an error
            if self.board.played_tiles[tile_tuple] is not None:
                return {"error": "Tile is already played and is in a hotel chain."}



        # Check orthogonal neighbors
        neighbors = [
            (row_index - 1, col_index),  # Up
            (row_index + 1, col_index),  # Down
            (row_index, col_index - 1),  # Left
            (row_index, col_index + 1)   # Right
        ]
        neighbor_hotels = set()
        for neighbor in neighbors:
            if neighbor in self.board.played_tiles:
                neighbor_hotel = self.board.played_tiles[neighbor]
                if neighbor_hotel is not None:
                    neighbor_hotels.add(neighbor_hotel)



        if len(neighbor_hotels) == 1:
            # Only one neighbor with the same hotel
            neighbor_hotel = neighbor_hotels.pop()
            self.board.played_tiles[tile_tuple] = neighbor_hotel
            self.occupied_hotels[neighbor_hotel].append(tile_tuple)
            return {"growing": neighbor_hotel}

        elif len(neighbor_hotels) == 0:
            # No neighbor with a hotel
            return {"error": "No neighboring tile belongs to a hotel."}

        else:
            # Multiple neighbors with different hotels
            return {"error": "Multiple neighboring tiles belong to different hotels."}



    # def inspect
    def inspect(self, row, col):
        acquirer_label = None
        acquired_labels = None
        tile = Tile(row, col)
        row_index, col_index = tile.get_row_index(), tile.get_col_index()
        tile_tuple = (row_index, col_index)

        # Get orthogonal neighbors
        neighbors = [
            (row_index - 1, col_index),  # Up
            (row_index + 1, col_index),  # Down
            (row_index, col_index - 1),  # Left
            (row_index, col_index + 1)   # Right
        ]

        # Filter valid neighbors within the board boundaries
        valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < self.board.rows and 0 <= c < self.board.cols]

        if not valid_neighbors:
            self.singleton(row, col)
            return "singleton"
            # print("singleton")
        elif len(valid_neighbors) == 1:
            neighbor_row, neighbor_col = valid_neighbors[0]
            neighbor_hotel = self.board.played_tiles.get((neighbor_row, neighbor_col))
            if neighbor_hotel in self.occupied_hotels:
                self.growing(row, col, neighbor_hotel)
                return {"growing": neighbor_hotel}

            else:
                return "founding"

        elif len(valid_neighbors) >= 2:
            neighbor_hotels = [self.board.played_tiles.get(neighbor) for neighbor in valid_neighbors if self.board.played_tiles.get(neighbor)]
            unique_neighbor_hotels = list(set(neighbor_hotels))

            safe_hotels = [hotel for hotel in unique_neighbor_hotels if len(self.occupied_hotels[hotel]) >= 11]
            if safe_hotels:

                return {"impossible": "Cannot merge with a safe hotel."}
            if len(unique_neighbor_hotels) == 0:  # Added this condition to handle the case when there are no valid hotels
                # No valid hotels among neighbors
                print("Singleton")
                return "singleton"
                # print("singleton inspect")
            elif len(unique_neighbor_hotels) == 1:
                # All neighbors belong to the same hotel
                acquirer_label = unique_neighbor_hotels[0]
                return {"growing": acquirer_label}


            else:
                # Different hotels among neighbors, determine acquirer and acquired
                acquirer_label = max(unique_neighbor_hotels, key=lambda x: len(self.occupied_hotels.get(x, [])))
                acquired_labels = [hotel for hotel in unique_neighbor_hotels if hotel != acquirer_label]


                return {"acquirer": acquirer_label, "acquired": acquired_labels}


    def merging(self, row, col, input_label):
        tile = Tile(row, col)
        row_index, col_index = tile.get_row_index(), tile.get_col_index()

        neighbors = [
            (row_index - 1, col_index),
            (row_index + 1, col_index),
            (row_index, col_index - 1),
            (row_index, col_index + 1)
        ]
        neighbor_hotels = {self.board.played_tiles.get(neighbor) for neighbor in neighbors if neighbor in self.board.played_tiles}

        safe_hotels = [hotel for hotel in neighbor_hotels if hotel and len(self.board.played_hotels[hotel]) >= 11]
        if safe_hotels:
            return {"impossible": "Cannot merge with a safe hotel."}

        # Find the max length of neighboring hotels
        max_length = max(len(self.board.played_hotels[hotel]) for hotel in neighbor_hotels) if neighbor_hotels else 0
        max_hotels = [hotel for hotel in neighbor_hotels if len(self.board.played_hotels[hotel]) == max_length]
        print("max hotels: ",max_hotels)
        # Handle tie situation
        if len(max_hotels) > 1:
            if not input_label:
                return {"error": "Tiebreaker needed between " + ", ".join(max_hotels)}
            elif input_label not in max_hotels:
                return {"impossible": f"The given hotel name '{input_label}' cannot be the acquirer."}

        # If there's no tie or input_label is one of the max hotels
        acquirer_label = input_label if input_label in max_hotels else max_hotels[0] if max_hotels else None
        print("acquirer: ",acquirer_label)
        if not acquirer_label:  # This also catches the case where max_hotels might be empty
            return {"impossible": "No valid merger found."}
        print("Neighbor: ",neighbor_hotels)
        acquired_labels = [hotel for hotel in neighbor_hotels if hotel != acquirer_label]
        print("acquired : ",acquired_labels)

        # Perform the merger
        for acquired_label in acquired_labels:
            self.board.played_hotels[acquirer_label].extend(self.board.played_hotels[acquired_label])
            del self.board.played_hotels[acquired_label]
        print("acquirer: ", acquirer_label, "acquired: ", acquired_labels)
        return {"acquirer": acquirer_label, "acquired": acquired_labels}



# board_data={
#     "tiles": [
#       { "row": "C", "column": 3 },
#       { "row": "A", "column": 3 }
#     ],
#     "hotels": [
#       { "hotel": "American", "tiles": [{ "row": "C", "column": 3 }] },
#       { "hotel": "Imperial", "tiles": [{ "row": "A", "column": 3 }] }
#     ]
#   }

# game=Game(board_data)

# game.singleton("D",6)

# Assuming board_data and player_names are provided as in the previous examples
board_data = {
    "tiles": [
        {"row": "B", "column": 2}, {"row": "B", "column": 3},  # American

        {"row": "B", "column": 5}, {"row": "D", "column": 6},  # Continental

        {"row": "C", "column": 4}  # Imperial
    ],
    "hotels": [
        {"hotel": "American", "tiles": [{"row": "B", "column": 2}, {"row": "B", "column": 3} #, {"row": "B", "column": 4}, {"row": "B", "column": 5}
                                        ]},
        {"hotel": "Continental", "tiles": [{"row": "B", "column": 5}, {"row": "D", "column": 6}]},
        {"hotel": "Imperial", "tiles": [{"row": "C", "column": 4}]}
    ]
}
player_names = ["Alice", "Bob"]

# Initialize GameState with board data and player names
game = Game(board_data, player_names)
game.merging("B", 4, "American")
# Generate and print the current state of the game
current_state = game.generate_state()
print(current_state)