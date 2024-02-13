from pydantic import BaseModel, Field, ConfigDict


class CarBase:

    def get_field_names(self,
                        update: bool = False,
                        ignore_id: bool = False,
                        ignore_value_none: bool = False) -> (str, str, list):
        field_names = ''
        field_binds = ''
        fiels_values = []

        for key in self.__dict__.keys():
            if ignore_id and key == 'id':
                continue

            if self.__dict__[key] is None and ignore_value_none:
                continue

            if update:
                field_names += f'{key} = ?,'
            else:
                field_names += key + ','
                field_binds += '?,'

            value = self.__dict__[key]
            if value is None:
                fiels_values.append(None)
            else:
                fiels_values.append(value)

        return field_names[:-1], field_binds[:-1], fiels_values


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


class CarPost(BaseModel, CarBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    color: str | None = Field(min_length=1, default=None)
    year_manufactured: int | None = Field(gt=0, default=None)
    year_model: int | None = Field(gt=0, default=None)
    fuel: str | None = Field(min_length=1, default=None)
    horsepower: int | None = Field(gt=0, default=None)
    doors: int | None = Field(gt=0, default=None)
    seats: int | None = Field(gt=0, default=None)
    fipe: str | None = Field(min_length=1, default=None)


class CarPut(BaseModel, CarBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: int = Field(gt=0)
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    color: str | None = Field(min_length=1, default=None)
    year_manufactured: int | None = Field(gt=0, default=None)
    year_model: int | None = Field(gt=0, default=None)
    fuel: str | None = Field(min_length=1, default=None)
    horsepower: int | None = Field(gt=0, default=None)
    doors: int | None = Field(gt=0, default=None)
    seats: int | None = Field(gt=0, default=None)
    fipe: str | None = Field(min_length=1, default=None)


class CarPatch(BaseModel, CarBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: int = Field(gt=0)
    make: str | None = Field(min_length=1, default=None)
    model: str | None = Field(min_length=1, default=None)
    color: str | None = Field(min_length=1, default=None)
    year_manufactured: int | None = Field(gt=0, default=None)
    year_model: int | None = Field(gt=0, default=None)
    fuel: str | None = Field(min_length=1, default=None)
    horsepower: int | None = Field(gt=0, default=None)
    doors: int | None = Field(gt=0, default=None)
    seats: int | None = Field(gt=0, default=None)
    fipe: str | None = Field(min_length=1, default=None)
