# %%
import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient

# %%
client = MongoClient("mongodb://0.0.0.0:27017/")
# %%
client
# %%
mydb = client["animals"]
# %%
collection = mydb.shelterA
# %%
record = {
    "animal": "cat",
    "breed": "shorthair",
    "age": 2,
    "health": "good",
    "neutered": "false",
}
# %%
collection.insert_one(record)
# %%
testing = collection.find_one()
print(testing)
# %%
df = pd.DataFrame(list(collection.find()))
print(df)
# %%
