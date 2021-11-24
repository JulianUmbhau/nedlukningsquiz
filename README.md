# nedlukningsquiz
https://www.bmc.com/blogs/mongodb-docker-container/
https://www.youtube.com/watch?v=2pWwSm6X24o&ab_channel=CharmingData



To use:

Set .env file
- dash_port=8080
- dash_debug=True
```
docker-compose up
```
Test mongodb database over python:
```
python3 test-mongo.py
```
Test mongodb database over shell:
```
docker exec -it mongodb bash
```
Run dash app with database connection:\
NB - If "animals" database is empty, error message created
```
Python3 mongo-dash.py
```
Close down again - data volume is persistent and opens up again next time
```
docker-compose down
```


