class InvalidCoordinatesException(Exception):
    def __init__(self):
        super().__init__("Coordinates should be from 1 to 3!")


class OccupiedCellException(Exception):
    def __init__(self):
        super().__init__("This cell is occupied! Choose another one!")