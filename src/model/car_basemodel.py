from pydantic import BaseModel


class Car(BaseModel):
    id: int
    make: str
    model: str
    color: str | None = None
    year_manufactured: int | None = None
    year_model: int | None = None
    fuel: str | None = None
    horsepower: int | None = None
    doors: int | None = None
    seats: int | None = None
    fipe: str | None = None
    date_created: int
    date_updated: int | None = None


class CarPost(BaseModel):
    make: str
    model: str
    color: str | None = None
    year_manufactured: int | None = None
    year_model: int | None = None
    fuel: str | None = None
    horsepower: int | None = None
    doors: int | None = None
    seats: int | None = None
    fipe: str | None = None

    def get_field_names(self) -> (str, str, list):
        field_names = ''
        field_binds = ''
        fiels_values = []

        for key in self.__dict__.keys():
            field_names += key + ','
            field_binds += '?,'
            value = self.__dict__[key]
            if value is None:
                fiels_values.append(None)
            else:
                fiels_values.append(value)

        return field_names[:-1], field_binds[:-1], fiels_values
