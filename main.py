import csv
import requests
from flask import Flask, jsonify

API_URL = "https://rickandmortyapi.com/api/character"
CSV_FILE = "/data/characters.csv"

app = Flask(__name__)

def fetch_characters():
    page = 1
    results = []

    while True:
        res = requests.get(API_URL, params={"page": page})
        data = res.json()

        for c in data["results"]:
            if (
                c["species"] == "Human"
                and c["status"] == "Alive"
                and c["origin"]["name"] == "Earth"
            ):
                results.append({
                    "name": c["name"],
                    "location": c["location"]["name"],
                    "image": c["image"]
                })

        if not data["info"]["next"]:
            break
        page += 1

    return results


def write_csv(data):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "location", "image"])
        writer.writeheader()
        writer.writerows(data)


@app.route("/characters")
def characters():
    data = fetch_characters()
    write_csv(data)
    return jsonify(data)


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
