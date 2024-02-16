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

class Hotel:
    valid_hotels = ["American", "Continental", "Festival", "Imperial", "Sackson", "Tower", "Worldwide"]
    played_hotels = {}  # Shared among all instances
    played_tiles = {}  # Maps tile indices tuples to hotel names

    @classmethod
    def update_hotel_tiles(cls, hotel_name, tiles):
        for tile in tiles:
            tile_indices = (tile.get_row_index(), tile.get_col_index())
            if hotel_name not in cls.played_hotels:
                cls.played_hotels[hotel_name] = []
            cls.played_hotels[hotel_name].append(tile_indices)
            cls.played_tiles[tile_indices] = hotel_name

    @classmethod
    def add_tile_to_hotel(cls, hotel_name, tile):
        if hotel_name not in cls.valid_hotels:
            raise ValueError(f"{hotel_name} is not a valid hotel name.")

        tile_indices = (tile.get_row_index(), tile.get_col_index())

        if tile_indices in cls.played_tiles:
            # Update the hotel association for the tile
            cls.played_tiles[tile_indices] = hotel_name
            if hotel_name not in cls.played_hotels:
                cls.played_hotels[hotel_name] = []
            if tile_indices not in cls.played_hotels[hotel_name]:
                cls.played_hotels[hotel_name].append(tile_indices)
        else:
            raise ValueError(f"Tile at {tile_indices} cannot be added to {hotel_name} because it is not on the board.")

class Board:
    def __init__(self, board_data=None):
        self.rows = 9
        self.cols = 12
        self.board_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.played_tiles = Hotel.played_tiles
        self.played_hotels = Hotel.played_hotels
        if board_data:
            self.process_board_data(board_data)

    def process_board_data(self, board_data):
        # Process tiles without hotel names
        for tile_data in board_data.get('tiles', []):
            tile = Tile(tile_data['row'], str(tile_data['column']))
            self.add_tile_to_board(tile, None)  # Initialize with hotel_name as None

        # Process hotels separately to associate tiles with hotels
        for hotel_data in board_data.get('hotels', []):
            hotel_name = hotel_data['hotel']
            if hotel_name not in Hotel.valid_hotels:
                raise ValueError(f"{hotel_name} is not a valid hotel name.")
            for tile_data in hotel_data.get('tiles', []):
                tile = Tile(tile_data['row'], str(tile_data['column']))
                Hotel.add_tile_to_hotel(hotel_name, tile)  # Associate tile with hotel


    def add_tile_to_board(self, tile, hotel_name):
        row_index, col_index = tile.get_row_index(), tile.get_col_index()
        self.board_matrix[row_index][col_index] = 1
        # Initialize played_tiles with hotel_name as None for new tiles
        if (row_index, col_index) not in self.played_tiles:
            self.played_tiles[(row_index, col_index)] = hotel_name

    def print_board(self):
        for row in self.board_matrix:
            print(' '.join(map(str, row)))

