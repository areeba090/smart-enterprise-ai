import csv

from mongodb import db


def import_knowledge():
    collection = db.organizational_knowledge

    with open(
        "data/organizational_knowledge.csv",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        documents = []

        for row in reader:
            document = {
                "title": row["title"].strip(),
                "category": row["category"].strip(),
                "content": row["content"].strip(),
                "source": row["source"].strip()
            }

            documents.append(document)

    # Remove old manually inserted test knowledge
    collection.delete_many({})

    if documents:
        collection.insert_many(documents)

    print(
        f"{len(documents)} knowledge documents "
        "imported into MongoDB successfully."
    )


if __name__ == "__main__":
    import_knowledge()