from main import create_character

from pytest import fixture, raises

import csv
import os


@fixture(scope="module")
def file_name():
    return "test_characters.csv"


@fixture(scope="module")
def character(file_name):

    name = "Hulk"
    intelligence = 9
    power = 7
    strength = 10
    agility = 8

    return [file_name, name, intelligence, power, strength, agility]


@fixture(scope="module")
def csv_file(file_name):

    with open(file_name, "w") as file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    yield

    os.remove(file_name)


@fixture
def csv_file_with_invalid_field_names():

    invalid_file_name = "invalid.csv"

    with open(invalid_file_name, "w") as file:
        fieldnames = ["id", "name", "intelligence", "agility"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    yield

    os.remove(invalid_file_name)


def test_create_character_standard(character, csv_file):
    expected_return = {
        "id": 1,
        "name": "Hulk",
        "intelligence": 9,
        "power": 7,
        "strength": 10,
        "agility": 8,
    }

    actual_return = create_character(*character)

    expected_csv_last_row = ["1", "Hulk", "9", "7", "10", "8"]

    with open(character[0]) as file:
        reader = csv.reader(file)

        characters = [character for character in reader]
        actual_csv_last_row = characters[-1]

    assert actual_return == expected_return

    assert actual_csv_last_row == expected_csv_last_row


def test_create_characters_with_invalid_csv(
    character, csv_file_with_invalid_field_names
):

    character[0] = "invalid.csv"

    with raises(ValueError):
        create_character(*character)


# def test_find_character_by_id_standard(test_csv, test_character):

#     character_id = 1
