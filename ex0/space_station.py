from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class Space(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field()
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    stat = Space(
        station_id="ISS001",
        name="ALI-SPACE-STATION",
        crew_size=6,
        power_level=80.5,
        oxygen_level=90.5,
        last_maintenance=datetime.now()
    )

    print("valid data")
    print(f"id: {stat.station_id}")
    print(f"name: {stat.name}")
    print(f"crew: {stat.crew_size}")
    print(f"power: {stat.power_level}")
    print(f"oxygen: {stat.oxygen_level}")
    print("status:  Operational")

    try:
        Space(
            station_id="B",
            name="Broken Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=60.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as error:
        print("Expected validation error:")

        for err in error.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
