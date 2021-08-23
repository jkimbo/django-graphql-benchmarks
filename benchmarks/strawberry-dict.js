import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    {
      duration: "5s",
      target: 10
    },
    {
      duration: "10s",
      target: 10
    }
  ]
};

export default function() {
  const payload = JSON.stringify({
    query: `query {
      top250 {
        id
        imdbId
        title
        year
        imageUrl
        imdbRating
        imdbRatingCount
        director {
          id
          name
        }
      }
    }
    `
  });
  const params = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  const url = __ENV.API_URL || "https://django-graphql-benchmark.herokuapp.com";
  const response = http.post(`${url}/strawberry-graphql-dict/`, payload, params);

  check(response, {
    "is status 200": r => r.status === 200
  });
  check(response, {
    "is response correct": r => {
      return (
        response.json().data.top250.length === 250 &&
        response.json().data.top250[0].title === "The Shawshank Redemption"
      );
    }
  });
}
