import csv


def create_character(filename, name, intelligence, power, strength, agility) -> dict:

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
