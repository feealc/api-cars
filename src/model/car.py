from gen.generic import Generic


class Car:
    id: int
    make: str
    model: str
    color: str
    year_manufactured: int
    year_model: int
    fuel: str
    horsepower: int
    doors: int
    seats: int
    fipe: str
    date_created: int
    date_updated: int

    def __init__(self, make: str, model: str):
        self.id = 0
        self.make = make
        self.model = model
        self.color = ''
        self.year_manufactured = 0
        self.year_model = 0
        self.fuel = ''
        self.horsepower = 0
        self.doors = 0
        self.seats = 0
        self.fipe = ''
        self.date_created = Generic.get_current_date()
        self.date_updated = 0

    def __str__(self):
        return f'id {self.id} : make {self.make} : model {self.model}'

    def load_from_tuple(self, line: tuple):
        self.id = line[0]
        self.make = line[1]
        self.model = line[2]
        self.color = line[3]
        self.year_manufactured = line[4]
        self.year_model = line[5]
        self.fuel = line[6]
        self.horsepower = line[7]
        self.doors = line[8]
        self.seats = line[9]
        self.fipe = line[10]
        self.date_created = line[11]
        self.date_updated = line[12]
