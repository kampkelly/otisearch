import json


def create_json(database, table, es_index, columns):
    json_structure = [{
        "database": database,
        "index": es_index,
        "plugins": ["Fullname", "Description"],
        "mapping": {
            "description_vector": {
                "type": "dense_vector",
                "dims": 1024,
                "index": "true",
                "similarity": "cosine"
            }
        },
        "nodes": {
            "table": table,
            "schema": "public",
            "columns": columns,
            "transform": {
                "rename": {
                    "phone": "mobile"
                }
            },
            "children": [
                {
                    "table": "document",
                    "columns": [
                        "id",
                        "type",
                        "s3Key",
                        "fileName"
                    ],
                    "relationship": {
                        "variant": "object",
                        "type": "one_to_many"
                    }
                }
            ]
        }
    }]

    return json_structure


def create_json_file(database, table, es_index, columns):
    json_output = create_json(database, table, es_index, columns)

    # Save the JSON output to a file
    with open('esearch/schemas/schema.json', 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

    print("JSON saved to schemas/schema.json")
