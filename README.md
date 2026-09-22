# Reconciliation API for messy Irish geographic location

## Requirements
- [Recommended ] UV package manager https://docs.astral.sh/uv/getting-started/installation/
- [If no UV available] Python 3.14 and above: https://www.python.org/downloads/
- OpenRefine client: https://openrefine.org/download

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

## Database
Database is build in the project (but if you want to rebuild it run as follows):
```bash
uv run -m src.scripts.init_db 
uv run -m src.scripts.load_official_data
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
http://127.0.0.1:8000/reconcile?q=Dublin&entity_type=county

## Reconciliation with OpenRefine client
- start API server if not started already:  uv run uvicorn src.main:app --reload
Start OpenRefine:
- start OpenRefine client
- Create project -> upload openrefine.csv from project root -> next
- Make sure in the window “Parse data as”: -> Columns are separated by -> commas (CSV) is
checked
- Create project (right upper corner)
- Click on the column and choose -> 'reconcile' -> start reconciling
- Chose “Irish Geographic Reconciliation Service” checkbox -> next
- Can choose checkbox “Reconcile against no particular type” or County, City, Local
Authority
Screenshots are provided in the screenshots folder in the root.

Service URL
- http://127.0.0.1:8000/openrefine/reconcile

