## run server
uv run uvicorn src.main:app --reload

## server url
http://127.0.0.1:8000

## example query url 
http://127.0.0.1:8000/reconcile?q=Dublin
http://127.0.0.1:8000/reconcile?q=Co.%20Dublin




### tests/fixtures/sprint3_ranking_cases.json
the fixture provides stable repeatable ranking tests for sprint 2 and 3 scoring algorithm.


## structure
├── README.md
├── evidence
│   ├── sprint2_matching_results.json
│   └── sprint2_test_results.txt
├── pyproject.toml
├── src
│   ├── config.py
│   ├── data
│   │   └── geo_data.json
│   ├── data_loader.py
│   ├── main.py
│   ├── match.py
│   ├── matcher.py
│   ├── place_normaliser.py
│   ├── save_records.py
│   └── similarity_score.py
├── tests
│   ├── fixtures
│   │   └── sprint3_ranking_cases.json
│   ├── test_data
│   │   └── test_data.py
│   ├── test_matcher.py
│   ├── test_matching_data.py
│   ├── test_normaliser.py
│   └── test_similarity_score.py
└── uv.lock
