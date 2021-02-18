from main import create_character

from pytest import fixture, raises

import csv
import os


@fixture
def test_file_name():
    return "test_characters.csv"


@fixture
def test_character(test_file_name):

    name = "Hulk"
    intelligence = 9
    power = 7
    strength = 10
    agility = 8

    return [test_file_name, name, intelligence, power, strength, agility]


@fixture
def test_csv(test_file_name):

    with open(test_file_name, "w") as test_file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(test_file, fieldnames=fieldnames)

        writer.writeheader()

    yield

    os.remove(test_file_name)


@fixture
def test_csv_with_invalid_field_names(test_file_name):

    with open(test_file_name, "w") as test_file:
        fieldnames = ["id", "name", "intelligence", "agility"]
        writer = csv.DictWriter(test_file, fieldnames=fieldnames)

        writer.writeheader()

    yield

    os.remove(test_file_name)


def test_create_character_standard_return(test_character, test_csv):

    expected = {
        "id": 1,
        "name": "Hulk",
        "intelligence": 9,
        "power": 7,
        "strength": 10,
        "agility": 8,
    }

    actual = create_character(*test_character)

    assert actual == expected


def test_create_character_written_in_file(test_character, test_csv):

    expected = ["1", "Hulk", "9", "7", "10", "8"]

    create_character(*test_character)

    with open(test_character[0]) as file:
        reader = csv.reader(file)

        characters = [character for character in reader]
        last_character = characters[-1]

    assert last_character == expected


def test_create_character_invalid_field_names(
    test_character, test_csv_with_invalid_field_names
):
    with raises(ValueError):
        create_character(*test_character)
