import pandas as pd
import os, sys, glob, time
import requests, json
import csv
from flask import Flask

# Global Variables
url = "https://rickandmortyapi.com/api/character/?Species=Human&status=alive&origin=earth"
csv_file = "ricknmorty.csv"
app = Flask(__name__)

def download_json(url):
    try:
        response = requests.get(url)
        json_data = response.json()
    except ValueError as e:
        print(e)
        print("Error downloading json")
        sys.exit(1)
    return json_data

# Check if a json is valid or not
def validate_json(response):
    try:
        json.dumps(response)
    except ValueError as e:
        print("Json response is not valid!")
        sys.exit(1)
    return True

def convert_json_to_csv(response):
    try:
        data = json.dumps(response)
        df = pd.DataFrame(response["results"], columns=["name", "image", "location"])
        cols = ['location']
        df[cols] = df[cols].applymap(lambda x: x['name'])
        new = pd.concat([df], ignore_index=True)
        print(new)
        new.to_csv(csv_file)
    except ValueError as e:
        print(e)
        sys.exit(1)

def convert_csv_to_json(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df.to_json()
    except ValueError as e:
        print(e)
        print("Couldn't convert csv to a valid json. Exiting...")
        sys.exit(1)

def main():
    try:
        response = download_json(url)
        validate_json(response)
        convert_json_to_csv(response)
    except ValueError as e:
        print("Couldn't fetch a valid json response and convert is to CSV. Exiting...")
        sys.exit(1)

@app.route('/healthcheck')
def healthcheck():
    return "Healthy!\n"

@app.route('/get_results')
def get_results():
    return convert_csv_to_json(csv_file)

# Main loop function
if __name__ == "__main__":
    print("Staring to parse endpoint's response to CSV file.")
    main()
    app.run(port=5000, debug=True, host='0.0.0.0')
