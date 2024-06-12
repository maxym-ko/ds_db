### Setting up PostgreSQL (Relational database)

#### Step 1: Start PostgreSQL
```shell
brew services start postgresql
```

#### Step 2: Create database
```shell
createdb hr_system
```

### Populate both DB with fake data

#### Step 1: Create tables
```shell
pip install -r requirements.txt
python init_db.py
```

#### Step 2: (Optional) Clean tables
```shell
python clean_db.py
```

#### Step 3: Populate with fake data
```shell
python populate_db.py
```

### Delete DB
```shell
dropdb hr_system
```
