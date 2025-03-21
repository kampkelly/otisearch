import json

foreign_key_suffix = "C7PvAmtr8"


def populate_children(relationships):
    children = []
    for item in relationships:
        new_child = {
            "table": item["name"],
            "label": f"{item['foreign_key']}_{foreign_key_suffix}",
            "columns": item["columns"],
            "relationship": {
                "variant": "object",
                "type": item["type"].replace("-", "_"),
                "foreign_key": {
                    "child": ["id"],
                    "parent": [item["foreign_key"]]
                }
            }
        }
        children.append(new_child)
        return children


def create_json(database, table, es_index, columns, relationships):
    json_structure = [{
        "database": database,
        "index": es_index,
        "plugins": ["Vector"],
        "mapping": {
            "search_vectors": {
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
            "children": populate_children(relationships) or []
        }
    }]

    return json_structure


def create_json_file(database, table, es_index, columns, relationships):
    json_output = create_json(database, table, es_index, columns, relationships)
    file_name = f'esearch/schemas/{es_index}_schema.json'
    with open(file_name, 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

    print(f"JSON saved to {file_name}")
    return json_output, file_name
