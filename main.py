import csv
import os.path


def convert_dict_number_values_to_int(dict_):
    number_atributes = ["id", "intelligence", "power", "strength", "agility"]

    return {
        key: (int(value) if (key in number_atributes) else value)
        for key, value in dict_.items()
    }


def create_character(filename, name, intelligence, power, strength, agility):

    expected_field_names = [
        "id",
        "name",
        "intelligence",
        "power",
        "strength",
        "agility",
    ]

    if os.path.isfile(filename):

        with open(filename, "r") as readable_file:
            reader = csv.DictReader(readable_file)

            has_reader = reader.fieldnames == expected_field_names

            rows = list(reader)

            try:
                last_id = rows[-1]["id"]
            except IndexError:
                last_id = 0

            new_character_id = int(last_id) + 1

            new_character = {
                "id": new_character_id,
                "name": name,
                "intelligence": intelligence,
                "power": power,
                "strength": strength,
                "agility": agility,
            }

        with open(filename, "a+") as writable_file:
            writer = csv.DictWriter(writable_file, fieldnames=expected_field_names)

            if not has_reader:
                writer.writeheader()

            writer.writerow(new_character)

    else:
        with open(filename, "w+") as writable_file:
            writer = csv.DictWriter(writable_file, fieldnames=expected_field_names)

            new_character = {
                "id": 1,
                "name": name,
                "intelligence": intelligence,
                "power": power,
                "strength": strength,
                "agility": agility,
            }

            writer.writeheader()
            writer.writerow(new_character)

    return new_character


def find_character_by_id(filename, character_id):

    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)

        for row in reader:
            if row["id"] == str(character_id):
                return convert_dict_number_values_to_int(row)

    raise ValueError("Character not found by given id")


def find_all_characters(filename):

    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)

        return [convert_dict_number_values_to_int(character) for character in reader]


def delete_character(filename, character_id):

    try:
        find_character_by_id(filename, character_id)
    except ValueError:
        return False

    with open(filename, "r") as readable_file:

        reader = csv.DictReader(readable_file)

        new_file = [
            character for character in reader if character["id"] != str(character_id)
        ]

    with open(filename, "w") as writable_file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(writable_file, fieldnames=fieldnames)

        writer.writeheader()

        for character in new_file:
            writer.writerow(character)

    return True


def update_character(filename, character_id, **kwargs):

    try:
        character_to_update = find_character_by_id(filename, character_id)
        character_to_update.update(kwargs)
    except ValueError:
        return None

    with open(filename, "r") as readable_file:

        reader = csv.DictReader(readable_file)

        new_file = [
            character if character["id"] != str(character_id) else character_to_update
            for character in reader
        ]

    with open(filename, "w") as writable_file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(writable_file, fieldnames=fieldnames)

        writer.writeheader()

        for character in new_file:
            writer.writerow(character)

        return character_to_update


if __name__ == "__main__":
    csv_filename = "characters.csv"

    create_character(csv_filename, "Hulk", 10, 10, 10, 10)
    create_character(csv_filename, "Batman", 10, 10, 10, 10)

    delete_character(csv_filename, 2)

    create_character(csv_filename, "Spiderman", 10, 10, 10, 10)

    update_character(csv_filename, 1, agility=1)
