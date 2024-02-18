from game_library import Board,Tile,Player, Share
import random
class Game:
    def __init__(self,board_data,players_data=[]) -> None:

        self.board = Board()
        
        if board_data:
            self.board.process_board_data(board_data)
            # get valid hotels
            self.availableHotels = self.board.valid_hotels
            
            
            #change back to 6000
        self.players = [Player(name, 6000) for name in players_data]
        

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

        print(row_index,col_index)
        print(self.board.board_matrix[row_index][col_index])
        if 0 <= row_index < self.board.rows and 0 <= col_index < self.board.cols:
            if self.board.board_matrix[row_index][col_index] == 0:  #checking if the tile is unoccupied
                print("inside if  = 0")
                self.board.board_matrix[row_index][col_index] = 1
                self.board.played_tiles[row_index,col_index] = None  #for now just keeping the value as None
                print("Singleton")
                return "singleton"
            else:
                print("singleton error")
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
                        print("SINGLE TILE")
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

                                print(game.board.played_hotels)
                                print(game.board.played_tiles)
                                return "founding"
                    # If there are no available hotel chains, the player can place the tile but cannot found a new hotel
                        elif label not in self.availableHotels:
                        # print("The given hotel label is not present in the available hotel chains. So adding tile only")
                        # we create and place the tile
                            print("UNAVAILABLE")
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
        print(" NEIGBOUR INDICES", neighbors)
        # Filter valid neighbors within the board boundaries
        valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < self.board.rows and 0 <= c < self.board.cols and self.board.board_matrix[r][c] == 1]
        print("VALID NEIGBOURS",valid_neighbors)
        if not valid_neighbors:
            
            print("SIngleton is running with no valid neighbors")
            self.singleton(row, col)
            print(row,col)
            print(row_index,col_index)
            print(self.board.played_tiles)
            self.board.played_tiles.__delitem__(tile_tuple)
            self.board.board_matrix[row_index][col_index] = 0
            print(self.board.played_tiles)
                
            return "singleton"
            # print("singleton")
        elif len(valid_neighbors) == 1:
            print("INSIDE THIS CODE")
            neighbor_row, neighbor_col = valid_neighbors[0]
            neighbor_hotel = self.board.played_tiles.get((neighbor_row, neighbor_col))
            print("NEIGHBOR INDEX's HOTEL FOR GROW ACTION -> ", neighbor_hotel)
            if neighbor_hotel in self.board.played_hotels:
                # we run growing func to check the expected board.
                self.growing(row, col)
                # now the board is updated. must remove that update cos inspect doesnt change the board state permanently.
                print("Test")
                
                # remove from played hotels. remove from played tiles
                # print(self.board.played_hotels)
                self.board.played_hotels[neighbor_hotel].remove(tile_tuple)
                # print(self.board.played_hotels)
                # print(self.board.played_tiles)
                self.board.played_tiles.__delitem__(tile_tuple)
                print("Grow TEST:",self.board.board_matrix[row_index][col_index] )
                # self.board.board_matrix[row_index][col_index] = 0
                # print(self.board.played_tiles)
                
                # return {"growing": neighbor_hotel}
                return "growing"


            else:
                return "founding"

        elif len(valid_neighbors) >= 2:
            # Founding not possible since we have more than 1 neighbour
            print("INSIDE THIS CODE")
            neighbor_hotels = [self.board.played_tiles.get(neighbor) for neighbor in valid_neighbors if self.board.played_tiles.get(neighbor)]
            unique_neighbor_hotels = list(set(neighbor_hotels))

            safe_hotels = [hotel for hotel in unique_neighbor_hotels if len(self.board.played_hotels[hotel]) >= 11]
            if safe_hotels:
                return {"impossible": "Cannot merge with a safe hotel."}
            if len(unique_neighbor_hotels) == 0:  # Added this condition to handle the case when there are no valid hotels
                # No valid hotels among neighbors
                # print(self.board.board_matrix)
                # print("Singleton")
                
                return "singleton"
                # print("singleton inspect")
            elif len(unique_neighbor_hotels) == 1:
                # All neighbors belong to the same hotel
                acquirer_label = unique_neighbor_hotels[0]
                # print(self.board.board_matrix)
                # print("growing")
                # return {"growing": acquirer_label}
                return "growing"


            else:
                # Different hotels among neighbors, determine acquirer and acquired
                acquirer_label = max(unique_neighbor_hotels, key=lambda x: len(self.board.played_hotels.get(x, [])))
                acquired_labels = [hotel for hotel in unique_neighbor_hotels if hotel != acquirer_label]
                # print("MERGER")
                return "merging"
                
                # return {"acquirer": acquirer_label, "acquired": acquired_labels}


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

        acquirer_label = max(neighbor_hotels, key=lambda hotel: len(self.board.played_hotels[hotel]) if hotel else 0)
        if not acquirer_label or acquirer_label != input_label:
            # print("error")
            return {"impossible": "Input label does not match the acquirer label or no valid merger found."}

        acquired_labels = [hotel for hotel in neighbor_hotels if hotel and hotel != acquirer_label]

        for acquired_label in acquired_labels:
            self.board.played_hotels[acquirer_label].extend(self.board.played_hotels[acquired_label])
            del self.board.played_hotels[acquired_label]


        return {"acquirer": acquirer_label, "acquired": acquired_labels}
    

    def getHotelPrice(self, label: str):
        hotelCount = len(self.board.played_hotels[label])
        #print(hotelCount)
        if hotelCount < 2:
            return {"error" : "Not valid hotel to purchase shares of"}
        tier = self.hotel_tiers.get(label)
        #print(tier)
        if tier is not None:
            # Get the pricing table for the specified tier
            tier_prices = self.pricing_table.get(tier)
            #print(tier_prices)
            if tier_prices is not None:
                # Find the row with the first number smaller or equal to the number of tiles
                price = next((price for size, price in sorted(tier_prices.items(), reverse=True) if size <= hotelCount), None)
                #print(price)
                if price is not None:
                   return price
    

    def buy(self, shares: list, player_list: list):
        currPlayer = self.players[0]

        #check if count is valid
        shareCount = len(shares)
        if shareCount < 1:
            #print("short worked")
            return {"error" : "Cannot purchase less than 1 share"}
        elif shareCount > 3:
            #print("long worked")
            return {"error" : "Cannot purchase more than 3 shares"}
        
        #go through labels and purchase if possible
        for share in shares:
            if len(self.board.played_hotels[share]) < 2:
                #print("Short hotel worked")
                return {"error" : "Not valid hotel to purchase shares of"}
            price = self.getHotelPrice(share)
            #print(share, price)
            if currPlayer.cash < price:
                #print("less cash worked")
                return {"error" : "Not enough cash to purchase share"}
            if self.available_shares[share] <= 0:
                #print("0 worked ")
                return {"error" : "Not enough shares to purchase"}

            currPlayer.add_share(Share(share, 1)) #init share
            currPlayer.cash = currPlayer.cash - price
            self.available_shares[share] -= 1
            print(f"Player: {currPlayer.name} bought share of {share}")
        currState = self.generate_state()
        return currState
    

    def done(self):
        currPlayer = self.players[0]
        rows = 9
        columns = 12
        if len(self.board.played_tiles) != 108: #total number of slots on board
            #generate random tile that is not on the board
            while True:
                random_row = random.randint(0, rows - 1)
                random_column = random.randint(1, columns)
                random_tile = Tile(chr(ord('A') + random_row), random_column)
                random_tuple = (random_row, random_column-1)

                if random_tuple not in self.board.played_tiles:
                    break

            currPlayer.add_tile(random_tile)
        #currPlayer.add_tile(random_tile)
        self.players.append(self.players.pop(0))
        currState = self.generate_state()
        return currState
        
        
        
        
# PLACE REQUEST:
# Inputs are row/col/state and/or hotellabel
# basically place are just actions like singleton, merge, grow,found
# if we have an hotel name, one of the last 3 actions happen else we just have singleton

    def place(self,row,col,hotel_name = None):
        print("PLACE FUNCTION -> BOARD : ",self.board.board_matrix)
        print()
        if(hotel_name is None):
            print("PLACE FUNCTION WITH NO HOTEL LABEL")
            print()
            possible_action =  self.inspect(row,col)
            
            print("PLACE FUNCTION WITH NO HOTEL LABEL-> Possible Action : ",possible_action)

            print()
                            
            # if the possible action is singleton
            if(possible_action == 'singleton'):
                print("I am here")
                print(self.board.played_tiles)
                return self.singleton(row, col)
            
            # if the possible action is growing
            elif(possible_action == 'growing'):
                print("GIVEN ROW:",row,col)
                print("Board after inspect:",self.board.board_matrix)
                return self.growing(row, col)
            
            # if the possible action is foundnig
            elif(possible_action == 'founding'):
                message = {"msg" : "Founding action is possible."}
                return message
            elif(possible_action == 'merging'):
                message = {"msg" : "Merging action is possible if label is given."}
                return message
            
        elif (hotel_name is not None):
            print("PLACE FUNCTION -> HOTEL NAME : ",hotel_name)
            print()
            possible_action =  self.inspect(row,col)
            print("PLACE FUNCTION -> Possible Action : ",possible_action)
            print()
            if(possible_action == 'singleton'):
                return self.singleton(row, col)
            
            # if the possible action is growing
            elif(possible_action == 'growing'):
                print("GIVEN ROW:",row,col)
                print("Board after inspect:",self.board.board_matrix)
                return self.growing(row, col)
            
            # if the possible action is foundnig
            elif(possible_action == 'founding'):
                print("GIVEN ROW:",row,col)
                print("Board after inspect:",self.board.board_matrix)
                return self.founding(row,col,hotel_name,self.board.board_matrix)
            elif(possible_action == 'merging'):
                print("GIVEN ROW:",row,col)
                print("Board after inspect:",self.board.board_matrix)
                return self.merging(row,col,hotel_name)


        
'''
board_data={
    "tiles": [
      { "row": "C", "column": 3 },
      { "row": "A", "column": 3 }
    ],
    "hotels": [
      { "hotel": "American", "tiles": [{ "row": "C", "column": 3 }] },
      { "hotel": "Imperial", "tiles": [{ "row": "A", "column": 3 }] }
    ]
  }
'''
# game=Game(board_data)

# game.singleton("D",6)

# Assuming board_data and player_names are provided as in the previous examples
board_data = {
    "tiles": [
        {"row": "C", "column": 3},
        {"row": "A", "column": 3},
        {"row": "C", "column": 4},
        {"row": "A", "column": 4},
        {"row": "E", "column": 3},
        {"row": "E", "column": 4},
        {"row": "E", "column": 5},
        {"row": "E", "column": 6},
        {"row": "E", "column": 7},
        {"row": "E", "column": 8},
        {"row": "E", "column": 9},
        {"row": "E", "column": 10}

    ],
    "hotels": [
        {"hotel": "American", "tiles": [{"row": "C", "column": 3}, {"row": "C", "column": 4}]},
        {"hotel": "Imperial", "tiles": [{"row": "A", "column": 3}, {"row": "A", "column": 4}]},
        {"hotel": "Continental", "tiles": [{"row": "E", "column": 3}, {"row": "E", "column": 4}
        ,{"row": "E", "column": 5}, {"row": "E", "column": 6}, {"row": "E", "column": 7},
        {"row": "E", "column": 8}, {"row": "E", "column": 9}, {"row": "E", "column": 10}]}
    ]
}
player_names = ["Alice", "Bob", "Jim", "Joe"]

# # Initialize GameState with board data and player names
game = Game(board_data, player_names)


#-----------BUY TEST-----------
labels = ["American", "Imperial", "Continental"]
#print(game.buy(labels, player_names))
#print(game.available_shares)
#print(game.players[0].shares)
# Generate and print the current state of the game
#current_state = game.generate_state()
#print(current_state)

#----------DONE TEST-----------

player_state = game.generate_players_state()
print(player_state)
print()
game.done()
print(game.generate_players_state())
print()
game.done()
print(game.generate_players_state())
print()
game.done()
print(game.generate_players_state())
print()
game.done()
print(game.generate_players_state())
print()


''' JAYANTH TEST DATA. DO NOT DELETE'''

# board_data={
#     "tiles": [
#         { "row": "D", "column":5 },
#       { "row": "C", "column": 7 },
#       { "row": "A", "column": 3 },
#       { "row": "C", "column": 3 }
#       ,{ "row": "G", "column": 1 }
#       ,{ "row": "I", "column": 1 }
#     ],
#     "hotels": [
#       { "hotel": "American", "tiles": [{ "row": "C", "column": 3 }] },
#       { "hotel": "Imperial", "tiles": [{ "row": "A", "column": 3 },{ "row": "C", "column":7 }] }
      
#     ]
#   }
# game=Game(board_data)

# ans = game.singleton("D",6)
# ONE NEIGHBOR
# ans = game.place("D",6) #founding
# ans = game.place("H",7) #singleton
# ans = game.place("A",4) #grow


# Multiple NEIGHBOR
# ans = game.place("H",1) #singleton
# ans = game.place("B",3) # merging
# ans = game.place("C",8) # grow

# with labels only merge,grow, found is done
# grow
# ans = game.place("C",8,"Imperial")
# found
# ans = game.place("D",6,"Sackson")
# merge
# ans = game.place("B",3,"American")
# print(ans)



# print(game.board.board_matrix)
# print(game.board.played_hotels)
# print(game.board.played_tiles)