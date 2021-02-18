import csv


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
    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)

        if reader.fieldnames != expected_field_names:
            raise ValueError("CSV Fieldnames are invalid or dont exist")

        rows = list(reader)
        total_rows = len(rows)

        new_character_id = total_rows + 1

        new_character = {
            "id": new_character_id,
            "name": name,
            "intelligence": intelligence,
            "power": power,
            "strength": strength,
            "agility": agility,
        }

    with open(filename, "a") as writable_file:
        writer = csv.DictWriter(writable_file, fieldnames=expected_field_names)

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

        for row in new_file:
            writer.writerows(row)

    return True


def update_character(filename, character_id, **kwargs):

    try:
        character_to_update = find_character_by_id(filename, character_id)
        character_to_update.update(kwargs)
        delete_character(filename, character_id)
    except ValueError:
        return None

    with open(filename, "a+", newline="") as writable_file:

        fieldnames = ["id", "name", "intelligence", "power", "strength", "agility"]
        writer = csv.DictWriter(writable_file, fieldnames=fieldnames)

        writer.writerow(character_to_update)

        return character_to_update
