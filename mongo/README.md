### Setting up MongoDB (Document-oriented database)

#### Step 1: Start MongoDB service
```shell
brew services start mongodb-community
```

#### Step 2: Create database and collection
```shell
mongosh hr_system
db.createCollection("users")
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

### Delete DB
```shell
mongosh hr_system --eval "db.dropDatabase()"
```
