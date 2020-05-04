# django-rest-api
Simple RESTful HTTP API to query a dataset. Implemented with Django Rest framework.

The REST API offers an interface to query a dataset from a RDBMS (example sqlite database is included in repo).

Consider an example dataset of metrics such as:
```
date,os,source,country,impressions,clicks,installs,spend,revenue
2018-01-01,ios,B,US,17590,320,94,764.5310552912023,2024.2677277486446
2018-01-01,android,D,AU,21521,222,33,920.2063657355452,130.00132429842702
2018-01-01,android,D,BR,27391,163,155,2536.9714925495637,2022.68810030078
2018-01-01,android,D,GB,4723,802,25,3801.03259531429,31.925240912640227
2018-01-02,ios,F,CN,16783,434,175,3594.7177640262444,1726.5795993417332
2018-01-03,ios,D,CN,22587,934,151,3113.2221889366906,1324.9620346669
```

A common SQL queries such as:
```
SELECT country, source, sum(impressions) as impressions, sum(clicks) as clicks
FROM dataset
WHERE date < '2018-03-02'
GROUP BY country, source
ORDER BY clicks DESC
```

can be translated to an API request:
```
http://{DOMAIN}:{PORT}/api/endpoint?select=impressions,clicks&groupby=source,country&date_before=2018-03-01&ordering=-clicks
```

Example response:
```
{
    "count": 49,
    "next": "http://127.0.0.1:8000/api/endpoint?date_before=2018-03-01&groupby=source%2Ccountry&limit=20&offset=20&ordering=-clicks&select=impressions%2Cclicks",
    "previous": null,
    "results": [
        {
            "source": "C",
            "country": "CA",
            "impressions": 73441,
            "clicks": 3517
        },
        {
            "source": "C",
            "country": "JP",
            "impressions": 75936,
            "clicks": 2698
        },
        [...]
```

## Quickstart
Clone the repository
```
git clone https://github.com/grbtm/django-rest-api.git
cd django-rest-api
```
Create a virtual env and activate it, install requirements into the environment:
```
python3 -m venv api_venv
source api_venv/bin/activate
pip install -r requirements.txt
```
Start the Django test server:
```
cd endpoint
python manage.py runserver
```
Start for example with viewing all the records:
```
http://127.0.0.1:8000/api/endpoint
```

## Tests
To run the tests, `cd` to directory of manage.py:
```
cd /path/to/django-rest-api/endpoint
python manage.py test
```

## Usage

Available parameters for `GET` requests:

`select`

`date`
`date_after`
`date_before`
`source`
`country`
`os`
`impressions`
`clicks`
`installs`
`spend`
`revenue`

`groupby`

`ordering`

### Other example queries

A)
```
SELECT sum(installs) as installs, date
FROM dataset
WHERE (date >= '2018-03-01') AND (date <= '2018-03-31') AND (os = 'ios')
GROUP BY date
ORDER BY date ASC
```
converted to API request:
```
http://{DOMAIN}:{PORT}/api/endpoint?select=installs&os=ios&groupby=date&date_after=2018-03-01&date_before=2018-03-31&ordering=date
```
Response:
```
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/endpoint?date_after=2018-05-01&date_before=2018-05-31&groupby=date&limit=20&offset=20&ordering=date&os=ios&select=installs",
    "previous": null,
    "results": [
        {
            "date": "2018-05-01",
            "installs": 45
        },
        {
            "date": "2018-05-02",
            "installs": 179
        },
        [...]
```
