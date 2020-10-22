import pandas as pd
import os, sys, glob, time
import requests, json
import csv
from flask import Flask
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
def check_json(response):
    try:
        json.dumps(response)
    except ValueError as e:
        sys.exit(1)
    return True

def convert_to_csv(response):
    try:
        data = json.dumps(response)
        df = pd.DataFrame(response["results"], columns=["name", "image", "location"])
        cols = ['location']
        df[cols] = df[cols].applymap(lambda x: x['name'])
        new = pd.concat([df], ignore_index=True)
        print(new)
        new.to_csv("data.csv")
    except ValueError as e:
        print(e)
        sys.exit(1)

def main():
    url="https://rickandmortyapi.com/api/character/?Species=Human&status=alive&origin=earth"
    try:
        response = download_json(url)
        check_json(response)
        convert_to_csv(response)
    except ValueError as e:
        print("Couldn't fetch a valid json response and convert is to CSV. Exiting...")
        sys.exit(1)

@app.route('/healthcheck')
def healthcheck():
    return "Healthy!"

@app.route('/get_results')
def get_results():
    return "results"

# Main loop function
if __name__ == "__main__":
    print("Staring to parse endpoint's response to CSV file.")
    main()
    app.run()
