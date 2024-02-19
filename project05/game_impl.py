import random
from game_library import Board,Tile,Player, Share
import random
class Game:
    def __init__(self,board_data,players_data=[]) -> None:
        self.board = Board()

        if board_data:
            self.board.process_board_data(board_data)
            # get valid hotels
        self.availableHotels = self.board.valid_hotels


        self.setup(players_data)

        #setup price table
        self.hotel_tiers = {
            "Worldwide": "Tier1",
            "Sackson": "Tier1",
            "Festival": "Tier2",
            "Imperial": "Tier2",
            "American": "Tier2",
            "Continental": "Tier3",
            "Tower": "Tier3"
        }

        self.pricing_table = {
            "Tier1": {2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 11: 700, 21: 800, 31: 900, 41: 1000},
            "Tier2": {2: 300, 3: 400, 4: 500, 5: 600, 6: 700, 11: 800, 21: 900, 31: 1000, 41: 1100},
            "Tier3": {2: 400, 3: 500, 4: 600, 5: 700, 6: 800, 11: 900, 21: 1000, 31: 1100, 41: 1200}
        }

        self.available_shares = {
            "American" : 25, "Continental" : 25, "Festival" : 25, "Imperial" : 25,
            "Sackson" : 25, "Tower" : 25, "Worldwide" : 25
        }

    def setup(self, players_data):
        self.players = []  # Clear existing players list
        if isinstance(players_data, list) and players_data and isinstance(players_data[0], dict):
            # Load from state (dictionary input)
            for player_info in players_data:
                player = Player(player_info["player"], player_info.get("cash", 6000))
                # Assume add_share and add_tile methods exist to properly add shares and tiles
                for share_info in player_info.get("shares", []):
                    player.add_share(Share(share_info["share"], share_info["count"]))
                for tile_info in player_info.get("tiles", []):
                    player.add_tile(Tile(tile_info["row"], str(tile_info["column"])))
                self.players.append(player)
        else:
            # Its list when requested setup
            player_names = players_data
            if len(player_names) > 6:
                return {"error": "Cannot have more than 6 players."}
            if len(set(player_names)) != len(player_names):
                return {"error":"Player names must be unique."}

            # Initialize players with names and default cash
            self.players = [Player(name, 6000) for name in player_names]

            # define the total rows and columns based on 9*12 board setup
            rows = [chr(r) for r in range(ord('A'), ord('I')+1)]
            columns = list(range(1, 13))

            # Generate all possible tiles
            all_tiles = [(row, col) for row in rows for col in columns]

            # Shuffle the tiles to randomize allocation
            random.shuffle(all_tiles)

            # Allocate 6 tiles to each player
            for player in self.players:
                for _ in range(6):
                    tile_data = all_tiles.pop()
                    tile = Tile(tile_data[0], tile_data[1])
                    player.add_tile(tile)

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


    def singleton(self,row,col):

        tile = Tile(str(row), str(col))
        row_index, col_index = tile.get_row_index(),tile.get_col_index()

        if 0 <= row_index < self.board.rows and 0 <= col_index < self.board.cols:
            if self.board.board_matrix[row_index][col_index] == 0:  #checking if the tile is unoccupied

                self.board.board_matrix[row_index][col_index] = 1
                self.board.played_tiles[row_index,col_index] = None  #for now just keeping the value as None

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
                                # create a key with hotel name
                                self.board.played_hotels[label] = []
                                letter_row_ascii_number = ord('A') + row_index
                                letter_row = chr(letter_row_ascii_number)
                                # add the given tile and the single tile to this key
                                self.board.played_hotels[label].append((letter_row,column_index + 1))
                                self.board.played_hotels[label].append((row,column))

                                # change occupied tiles as well. add hotel label now

                                # update given row and col
                                self.board.played_tiles[row,column] = label
                                # update teh single neighbour tile

                                self.board.played_tiles[letter_row,column_index + 1] = label



                                # remove the label from available hotels
                                self.availableHotels.remove(label)

                                
                                return "founding"
                    # If there are no available hotel chains, the player can place the tile but cannot found a new hotel
                        elif label not in self.availableHotels:
                        
                        # we create and place the tile

                            return self.singleton(row,column)

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
            self.board.played_hotels[neighbor_hotel].append(tile_tuple)
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
        valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < self.board.rows and 0 <= c < self.board.cols and self.board.board_matrix[r][c] == 1]

        if not valid_neighbors:


            self.singleton(row, col)

            self.board.played_tiles.__delitem__(tile_tuple)
            self.board.board_matrix[row_index][col_index] = 0


            return "singleton"

        elif len(valid_neighbors) == 1:

            neighbor_row, neighbor_col = valid_neighbors[0]
            neighbor_hotel = self.board.played_tiles.get((neighbor_row, neighbor_col))

            if neighbor_hotel in self.board.played_hotels:
                # we run growing func to check the expected board.
                self.growing(row, col)
                # now the board is updated. must remove that update cos inspect doesnt change the board state permanently.


                # remove from played hotels. remove from played tiles

                self.board.played_hotels[neighbor_hotel].remove(tile_tuple)


                self.board.played_tiles.__delitem__(tile_tuple)

                # self.board.board_matrix[row_index][col_index] = 
                return "growing"


            else:
                return "founding"

        elif len(valid_neighbors) >= 2:
            # Founding not possible since we have more than 1 neighbour

            neighbor_hotels = [self.board.played_tiles.get(neighbor) for neighbor in valid_neighbors if self.board.played_tiles.get(neighbor)]
            unique_neighbor_hotels = list(set(neighbor_hotels))

            safe_hotels = [hotel for hotel in unique_neighbor_hotels if len(self.board.played_hotels[hotel]) >= 11]
            if safe_hotels:
                return {"impossible": "Cannot merge with a safe hotel."}
            if len(unique_neighbor_hotels) == 0:  # Added this condition to handle the case when there are no valid hotels
                # No valid hotels among neighbors



                return "singleton"

            elif len(unique_neighbor_hotels) == 1:
                # All neighbors belong to the same hotel
                acquirer_label = unique_neighbor_hotels[0]

                return "growing"


            else:
                # Different hotels among neighbors, determine acquirer and acquired
                acquirer_label = max(unique_neighbor_hotels, key=lambda x: len(self.board.played_hotels.get(x, [])))
                acquired_labels = [hotel for hotel in unique_neighbor_hotels if hotel != acquirer_label]
                return "merging"



    def merging(self, row, col, input_label):
        tile = Tile(row, col)
        row_index, col_index = tile.get_row_index(), tile.get_col_index()

        neighbors = [
            (row_index - 1, col_index),
            (row_index + 1, col_index),
            (row_index, col_index - 1),
            (row_index, col_index + 1)
        ]
        # checking for neighboring tiles and its hotel chains
        neighbor_hotels = {self.board.played_tiles.get(neighbor) for neighbor in neighbors if neighbor in self.board.played_tiles}

        safe_hotels = [hotel for hotel in neighbor_hotels if hotel and len(self.board.played_hotels[hotel]) >= 11]
        if safe_hotels:
            return {"impossible": "Cannot merge with a safe hotel."}

        # looking for the max length of neighboring hotels, if no neighbor hotels available then set it to 0
        max_length = max(len(self.board.played_hotels[hotel]) for hotel in neighbor_hotels) if neighbor_hotels else 0

        # Could be more than one hotels with same maximum hotel chain length, so creating a list of max hotels
        max_hotels = [hotel for hotel in neighbor_hotels if len(self.board.played_hotels[hotel]) == max_length]

        # checking if merge conflicts
        if len(max_hotels) > 1:
            if not input_label:
                return {"error": "Tiebreaker needed between " + ", ".join(max_hotels)}
            elif input_label not in max_hotels:
                return {"impossible": f"The given hotel name '{input_label}' cannot be the acquirer."}

        # If there's no tie or input_label is one of the max hotels
        acquirer_label = input_label if input_label in max_hotels else max_hotels[0] if max_hotels else None


        # this also catches the case where max_hotels might be empty
        if not acquirer_label:
            return {"impossible": "No valid merger found."}


        acquired_labels = [hotel for hotel in neighbor_hotels if hotel != acquirer_label]


        # merging here
        for acquired_label in acquired_labels:
            self.board.played_hotels[acquirer_label].extend(self.board.played_hotels[acquired_label])
            del self.board.played_hotels[acquired_label]

        return {"acquirer": acquirer_label, "acquired": acquired_labels}


    def getHotelPrice(self, label: str):
        hotelCount = len(self.board.played_hotels[label])

        if hotelCount < 2:
            return {"error" : "Not valid hotel to purchase shares of"}
        tier = self.hotel_tiers.get(label)

        if tier is not None:
            # Get the pricing table for the specified tier
            tier_prices = self.pricing_table.get(tier)

            if tier_prices is not None:
                # Find the row with the first number smaller or equal to the number of tiles
                price = next((price for size, price in sorted(tier_prices.items(), reverse=True) if size <= hotelCount), None)

                if price is not None:
                   return price


    def buy(self, shares: list):
        currPlayer = self.players[0]


        #check if count is valid
        shareCount = len(shares)
        if shareCount < 1:

            return {"error" : "Cannot purchase less than 1 share"}
        elif shareCount > 3:

            return {"error" : "Cannot purchase more than 3 shares"}

        #go through labels and purchase if possible
        for share in shares:
            if len(self.board.played_hotels[share]) < 2:
                return {"error" : "Not valid hotel to purchase shares of"}
            price = self.getHotelPrice(share)

            if currPlayer.cash < price:
                return {"error" : "Not enough cash to purchase share"}
            if self.available_shares[share] <= 0:
                return {"error" : "Not enough shares to purchase"}

            requested_share = Share(share, 1)
            if len(currPlayer.shares) > 0:
                share_found = False
                print(currPlayer.shares)
                for owned_share in currPlayer.shares:
                    if owned_share.hotel_label == requested_share.hotel_label:
                        print(owned_share.hotel_label, requested_share.hotel_label)
                        # Player already owns the share, update the count
                        owned_share.count += 1
                        share_found = True
                        break
                if not share_found:
                    currPlayer.add_share(requested_share)
            else:
                currPlayer.add_share(requested_share) #init share
            print(currPlayer.shares)
            currPlayer.cash = currPlayer.cash - price
            self.available_shares[share] -= 1
        currState = self.generate_state()
        return currState


    def done(self):
        currPlayer = self.players[0]
        rows = 9
        columns = 12
        if len(self.board.played_tiles) < 108: #total number of slots on board
            #generate random tile that is not on the board
            while True:
                random_row = random.randint(0, rows - 1)
                random_column = random.randint(1, columns)
                random_tile = Tile(chr(ord('A') + random_row), random_column)
                random_tuple = (random_row, random_column-1)

                if random_tuple not in self.board.played_tiles:
                    opponent_tile_check = all(random_tile not in player.tiles for player in self.players)
                    if opponent_tile_check:
                        break

            currPlayer.add_tile(random_tile)
        self.players.append(self.players.pop(0))
        currState = self.generate_state()
        return currState




# PLACE REQUEST:
    def place(self,row,col,hotel_name = None):

        for player in self.players[1:]:  # Skip the first player, who is assumed to be the current player
            for tile in player.tiles:
                if tile.row == row and tile.col == int(col):  # Ensure col is compared as an integer
                    return {"Error": "Tile is already owned by another player"}


        if(hotel_name is None):
            possible_action =  self.inspect(row,col)

            
            # if the possible action is singleton
            if(possible_action == 'singleton'):
                
                return self.singleton(row, col)

            # if the possible action is growing
            elif(possible_action == 'growing'):
                
                return self.growing(row, col)

            # if the possible action is foundnig
            elif(possible_action == 'founding'):
                message = {"msg" : "Founding action is possible."}
                return message
            elif(possible_action == 'merging'):
                message = {"msg" : "Merging action is possible if label is given."}
                return message

        elif (hotel_name is not None):
            if hotel_name not in self.availableHotels:
                return {"Error": "Invalid hotel name"}
            
            possible_action =  self.inspect(row,col)
            
            if(possible_action == 'singleton'):
                return self.singleton(row, col)

            # if the possible action is growing
            elif(possible_action == 'growing'):

                return self.growing(row, col)

            # if the possible action is foundnig
            elif(possible_action == 'founding'):
                
                return self.founding(row,col,hotel_name,self.board.board_matrix)
            elif(possible_action == 'merging'):

                return self.merging(row,col,hotel_name)




