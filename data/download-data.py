import json
import re
import os

from dataclasses import dataclass, asdict
import requests  # type: ignore


API_KEY = os.environ["IMDB_API_KEY"]


@dataclass
class Director:
    name: str


def parse_director(crew: str) -> Director:
    match = re.search(r"(.*)\(dir\.\),", crew)
    if not match:
        raise Exception(f"Can't find director: {crew}")

    return Director(name=match.group(1).strip())


@dataclass
class Movie:
    imdb_id: str
    title: str
    year: int
    image_url: str
    imdb_rating: float
    imdb_rating_count: str

    director: Director

    @classmethod
    def from_data(cls, data):
        return cls(
            imdb_id=data["id"],
            title=data["title"],
            year=int(data["year"]),
            image_url=data["image"],
            imdb_rating=float(data["imDbRating"]),
            imdb_rating_count=data["imDbRatingCount"],
            director=parse_director(data["crew"]),
        )


request = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{API_KEY}")
request.raise_for_status()

data = request.json()

json_data = []

for item in data["items"]:
    json_data.append(asdict(Movie.from_data(item)))

with open("movies.json", "w") as output_file:
    json.dump(json_data, output_file, indent=2)
