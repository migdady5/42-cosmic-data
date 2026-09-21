from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field()
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field()
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_leader = any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(member.years_experience >= 5
                              for member in self.crew)
            if experienced < len(self.crew) / 2:
                raise ValueError("Long missions need 50 experienced crew")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM01",
                name="Sarah Connor",
                rank=Rank.commander,
                age=38,
                specialization="Mission Command",
                years_experience=12,
            ),
            CrewMember(
                member_id="CM02",
                name="John Smith",
                rank=Rank.lieutenant,
                age=30,
                specialization="Navigation",
                years_experience=6,
            ),
            CrewMember(
                member_id="CM03",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=5,
            ),
        ],
    )

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")

    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) -\
{member.specialization}"
        )

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Failed Test Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=30,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="CM04",
                    name="Tom Lee",
                    rank=Rank.officer,
                    age=26,
                    specialization="Navigation",
                    years_experience=3,
                ),
                CrewMember(
                    member_id="CM05",
                    name="Mia Ray",
                    rank=Rank.cadet,
                    age=24,
                    specialization="Engineering",
                    years_experience=1,
                ),
            ],
        )
    except ValidationError as error:
        print("Expected validation error:")
        for err in error.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
