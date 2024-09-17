def get_messages():
    prompt = """
    I will provide a text and list of columns and related/nested columns, and you will detect what the user is trying to search for.
    Then write an elastic search query for it. For the query, use the column names as exactly how it is written in the lists.
    You MUST always also add to the elastic search query a knn search for the dense vector column "search_vectors".
    Use what should be embedded as the value of the query_vector within this quote <> in this format `"query_vector": "<value to embed>"`, (I will embed it myself later).
    If knn is added, set k = 50 and num_candidates = 500 and the knn query should be in the root object.
    Add rank={{"rrf": {{"rank_window_size": 50}}}} in the root object.
    Apply boost to the subquery that is most relevant so it ranks higher. Do not use nested queries
    The query MUST not modify any information or return elasticsearch system info.
    """

    detailed_prompt = """
    I will provide a text and list of columns and related/nested columns, and you will detect what the user is trying to search for.
    Then write an elastic search query for it. For the query, use the column names as exactly how it is written in the lists.
    You MUST always also add to the elastic search query a knn search for the dense vector column "search_vectors". Use what should be embedded as the value of the query_vector (I will embed it myself later).
    Apply boost to the subquery that is most relevant so it ranks higher
    The query MUST not modify any information or return elasticsearch system info.

    Text: contacts with kubi in their name.
    Columns: ['id', 'firstName', 'lastName', 'email', 'gender', 'citizenship', 'phone', 'isVerified']
    related_columns: {{'preferredHospitalId_C7PvAmtr8': ['name', 'address']}}
    Query: {{
      "query": {{
        "bool": {{
          "must": [
            {{
              "multi_match": {{
                "query": "Kubi",
                "fields": ["firstName", "lastName"]
              }}
            }}
          ]
        }}
      }},
      "knn": {{
        "field": "search_vectors",
        "query_vector": "<Kubi>",
        "k": 50,
        "num_candidates": 500
      }}
    }}

    Text: Get the user with the email address john.doe@example.com
    Columns: ['id', 'firstName', 'lastName', 'email', 'gender', 'citizenship', 'phone', 'isVerified']
    related_columns: {{'preferredHospitalId_C7PvAmtr8': ['name', 'address']}}
    Query: {{
      "query": {{
        "bool": {{
          "must": [
            {{
              "term": {{
                "email": {{
                  "value": "john.doe@example.com",
                  "boost": 2.0,
                }}
              }}
            }}
          ]
        }}
      }},
      "knn": {{
        "field": "search_vectors",
        "query_vector": "<john.doe@example.com>",
        "k": 50,
        "num_candidates": 500
      }}
    }}

    Text: Find all female users whose preferred hospital is 'City General Hospital'
    Columns: ['id', 'firstName', 'lastName', 'email', 'gender', 'citizenship', 'phone', 'isVerified']
    related_columns: {{'preferredHospitalId_C7PvAmtr8': ['name', 'address']}}
    Query: {{
      "query": {{
        "bool": {{
          "must": [
            {{
              "term": {{
                "gender": "female"
              }}
            }},
            {{
              "match_phrase": {{
                "preferredHospitalId_C7PvAmtr8.name": "City General Hospital",
              }}
            }}
          ]
        }}
      }},
      "knn": {{
        "field": "search_vectors",
        "query_vector": "<female City General Hospital>",
        "k": 50,
        "num_candidates": 500
      }}
    }}
    """
    return prompt


c = """
Show me the contact information for someone named Sarah Johnson.
Get the user with the email address john.doe@example.com.
Show me all users with the last name Smith.
Show all verified users.
List all users who are not verified.
Find all users with a preferred hospital ID of 101."
Find all female users whose preferred hospital is 'City General Hospital'.
Show me the user with phone number +123456789 whose preferred hospital is 'Medical Center'.
Find all male users whose preferred hospital is located in New York.
Show all users who do not have a preferred hospital listed.
"""

examples = """
Find all female users whose preferred hospital is 'General Hospital'
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "gender": "female"
          }
        },
        {
          "term": {
            "preferredHospitalId.name": "General Hospital"
          }
        }
      ]
    }
  },
  "knn": {
    "field": "search_vectors",
    "query_vector": "<female General Hospital>",
    "k": 10,
    "num_candidates": 100
  }
}

software engineer
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "info": "software engineer"
          }
        }
      ]
    }
  },
  "knn": {
    "field": "search_vectors",
    "query_vector": "<software engineer>",
    "k": 10,
    "num_candidates": 100
  }
}

Give me users whose hospital is on this street: 2 Fremont
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "preferredHospital.address": "2 Fremont Street"
          }
        }
      ]
    }
  },
  "knn": {
    "field": "search_vectors",
    "query_vector": "<2 Fremont Street>",
    "k": 10,
    "num_candidates": 100
  }
}
"""
