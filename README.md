# Reconciliation API for messy Irish geographic location

## Installation
### There are two installation methods by UV(recommended) and PIP 

#### Setup UV package manager (recommended)

##### uv installation
- https://docs.astral.sh/uv/ - Fast Python package manager
- unix run: 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- Windows run: 
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- Version checker: 
```bash
uv --version
```
##### project dependencies
- from the project root run: 
```bash
uv sync
```

##### run uv project
```bash
 uv run uvicorn src.main:app --reload
```

##### run uv test
```bash
uv run pytest
```

#### Setup with PIP (in case if no UV available)

- Unix
```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

- Windows

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

##### project dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```


## run project
##### run python project
```bash
 uvicorn src.main:app --reload
```

##### run pytest test
```bash
pytest
```

## server url
http://127.0.0.1:8000

## example query url 
http://127.0.0.1:8000/reconcile?q=Dublin
http://127.0.0.1:8000/reconcile?q=Co.%20Dublin




### tests/fixtures/sprint3_ranking_cases.json
the fixture provides stable repeatable ranking tests for sprint 2 and 3 scoring algorithm.


### initialise database
uv run -m src.scripts.init_db

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
