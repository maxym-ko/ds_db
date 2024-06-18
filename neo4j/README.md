### Setting up Neo4j (Graph database)

#### Step 1: Start Neo4j service
```shell
brew services start neo4j
```

### Populate both DB with fake data

#### Step 1: (Optional) Clean tables
```shell
pip install -r requirements.txt
python clean_db.py
```

#### Step 2: Populate with fake data
```shell
pip install -r requirements.txt
python populate_db.py
```

### Run some queries
```shell
python example.py
```

### Cleaning up
```shell
brew services stop neo4j
```