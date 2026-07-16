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
├── evidence # help save project progression milestones
│   ├── sprint2_matching_results.json # saved sprint 2 candidate rankings
│   └── sprint2_test_results.txt # pytest output after sprint 2
├── pyproject.toml # project configuration
├── src
│   ├── config.py # setting 
│   ├── data
│   │   └── geo_data.json
│   ├── data_loader.py
│   ├── main.py # main file Fast Api routing
│   ├── match.py # link dataset, normaliser, similarity score, and matcher
│   ├── matcher.py # filter candidates and ranked result
│   ├── place_normaliser.py # normalise 
│   └── similarity_score.py # calculate similarity score
├── tests
│   ├── fixtures
│   │   └── sprint3_ranking_cases.json # evaluation fixture
│   ├── test_data
│   │   └── test_data.py
│   ├── test_matcher.py
│   ├── test_matching_data.py
│   ├── test_normaliser.py
│   └── test_similarity_score.py
