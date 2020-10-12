"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    result = []
    with open(neo_csv_path, newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            result.append(NearEarthObject(
                designation=row[3], name=row[4], hazardous=(row[7] == 'Y'), diameter=row[15]))
    return result


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    result = []
    with open(cad_json_path) as json_file:
        data = json.load(json_file)
        for item in data['data']:
            result.append(CloseApproach(
                designation=item[0], time=item[3], distance=item[4], velocity=item[7]))
    return result
