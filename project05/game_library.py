class Tile:
    def __init__(self, row, col):
        if not ('A' <= row.upper() <= 'I') or not (1 <= int(col) <= 12):
            raise ValueError("Invalid tile location.")
        self.row = row.upper()
        self.col = int(col)

    def get_col_index(self):
        return self.col - 1

    def get_row_index(self):
        return ord(self.row) - ord('A')

    def __repr__(self):
        return f"Tile({self.row}, {self.col})"

class Board:
    def __init__(self, board_data=None):
        self.rows = 9
        self.cols = 12
        self.board_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.valid_hotels = ["American", "Continental", "Festival", "Imperial", "Sackson", "Tower", "Worldwide"]
        self.played_tiles = {}  # Maps tile indices to hotel names or None
        self.played_hotels = {name: [] for name in self.valid_hotels}  # Maps hotel names to lists of tile indices
        if board_data:
            self.process_board_data(board_data)

    def process_board_data(self, board_data):
        # First, add all tiles as general tiles (None for hotel_name)
        all_tiles = set()  # To track all tiles and avoid duplication
        for tile_data in board_data.get('tiles', []):
            tile = Tile(tile_data['row'], str(tile_data['column']))
            if (tile.get_row_index(), tile.get_col_index()) not in all_tiles:
                self.add_tile_to_board(tile, None)
                all_tiles.add((tile.get_row_index(), tile.get_col_index()))

        # Next, process hotels and override any tile's hotel association if necessary
        for hotel_data in board_data.get('hotels', []):
            hotel_name = hotel_data['hotel']
            if hotel_name not in self.valid_hotels:
                raise ValueError(f"{hotel_name} is not a valid hotel name.")
            for tile_data in hotel_data.get('tiles', []):
                tile = Tile(tile_data['row'], str(tile_data['column']))
                # Directly add or update the hotel association without checking duplication
                # Because all_tiles ensures no tile is processed more than once
                self.add_tile_to_board(tile, hotel_name)
        # print("played tiles: ",self.played_tiles)
        # print("played hotels: ",self.played_hotels)


    def add_tile_to_board(self, tile, hotel_name=None):
        row_index, col_index = tile.get_row_index(), tile.get_col_index()
        tile_tuple = (row_index, col_index)

        # Update the board matrix and played_tiles with the tile
        # This line adds the tile to the board if it's not already there
        self.board_matrix[row_index][col_index] = 1

        # Update or add the hotel association for the tile
        self.played_tiles[tile_tuple] = hotel_name

        # Add the tile under the specified hotel if provided
        if hotel_name:
            if hotel_name not in self.played_hotels:
                self.played_hotels[hotel_name] = []
            if tile_tuple not in self.played_hotels[hotel_name]:
                self.played_hotels[hotel_name].append(tile_tuple)


    def print_board(self):
        for row in self.board_matrix:
            print(' '.join(map(str, row)))

class Player:
    def __init__(self, name, cash=0):
        self.name = name
        self.cash = 6000
        self.shares = []
        self.tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def add_share(self, share):
        self.shares.append(share)

class Share:
    def __init__(self, hotel_label, count):
        self.hotel_label = hotel_label
        self.count = count
# class admin_state:
#     def __init__(self):
#         self.board = Board()
#         self.players = []

#     def add_player(self, player):
#         self.players.append(player)