from main import (
    create_character,
    find_character_by_id,
    find_all_characters,
    delete_character,
)

from pytest import fixture, raises

import csv
import os


@fixture(scope="module")
def character():

    name = "Hulk"
    intelligence = 9
    power = 7
    strength = 10
    agility = 8

    return [name, intelligence, power, strength, agility]


@fixture(scope="module")
def character_dict():
    return {
        "id": 1,
        "name": "Hulk",
        "intelligence": 9,
        "power": 7,
        "strength": 10,
        "agility": 8,
    }


@fixture(scope="module")
def csv_file():

    file_name = "test_characters.csv"

    with open(file_name, "w") as file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    yield file_name

    os.remove(file_name)


@fixture
def csv_file_with_invalid_field_names():

    invalid_file_name = "invalid.csv"

    with open(invalid_file_name, "w") as file:
        fieldnames = ["id", "name", "intelligence", "agility"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    yield invalid_file_name

    os.remove(invalid_file_name)


@fixture
def csv_empty_file():

    empty_file_name = "empty.csv"

    with open(empty_file_name, "w") as file:
        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    yield empty_file_name

    os.remove(empty_file_name)


def test_create_character_standard(character, character_dict, csv_file):

    file_name = csv_file

    expected_return = character_dict

    actual_return = create_character(file_name, *character)

    expected_csv_last_row = ["1", "Hulk", "9", "7", "10", "8"]

    with open(file_name) as file:
        reader = csv.reader(file)

        characters = [character for character in reader]
        actual_csv_last_row = characters[-1]

    assert actual_return == expected_return

    assert actual_csv_last_row == expected_csv_last_row


def test_create_characters_with_invalid_csv(
    character, csv_file_with_invalid_field_names
):

    invalid_file_name = csv_file_with_invalid_field_names

    with raises(ValueError):
        create_character(invalid_file_name, *character)


def test_find_character_by_id_standard(csv_file, character, character_dict):

    file_name = csv_file

    character_id = 1

    expected = character_dict

    actual = find_character_by_id(file_name, character_id)

    assert actual == expected

    with raises(ValueError):
        inexistent_character_id = 56
        find_character_by_id(file_name, inexistent_character_id)


def test_find_all_characters_standard(character_dict, csv_file):

    file_name = csv_file

    expected = [character_dict]

    actual = find_all_characters(file_name)

    assert actual == expected


def test_find_all_characters_empty_file(csv_empty_file):

    empty_file_name = csv_empty_file

    expected = []

    actual = find_all_characters(empty_file_name)

    assert actual == expected


def test_delete_character_standard(csv_file):

    file_name = csv_file

    character_id = 1

    was_deleted = delete_character(file_name, character_id)

    assert was_deleted

    with open(file_name, "r") as readable_file:

        reader = csv.reader(readable_file)

        for row in reader:
            assert row != ["1", "Hulk", "9", "7", "10", "8"]


def test_deleted_character_inexistent_character(csv_file):

    file_name = csv_file

    character_id = 45

    was_deleted = delete_character(file_name, character_id)

    assert not was_deleted
