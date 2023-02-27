from flask import Flask, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from datetime import datetime,timedelta
from operator import itemgetter
import json

ELASTIC_CLOUD_ID = 'S8t3CIJmSP2AGsQDL1GWnQ'
ELASTIC_CLOUD_URL = 'https://8f9677360fc34e2eb943d737b2597c7b.us-east-1.aws.found.io:9243/'
ELASTIC_CLOUD_USER = 'elastic'
ELASTIC_CLOUD_PASSWORD = 'AWbtmGda2Q7BI2bYpdjyF4qd'

es = Elasticsearch(
    [ELASTIC_CLOUD_URL],
    http_auth=(ELASTIC_CLOUD_USER, ELASTIC_CLOUD_PASSWORD),
    scheme="https",
)

app = Flask (__name__)

@app.route("/facultycourses")
def get_courses():
  id = request.args.get("id")
  result = es.search(
    index='courses',size=50,
    query={
      "match" : {"faculty_id" : id}
    }
)
  response_list = []
  courses_name = []
  for course in result["hits"]["hits"]:
    if not course["_source"]["name"] in courses_name:
     courses_name.append(course["_source"]["name"])      
     response_list.append(course["_source"])
  return sorted(response_list,key=itemgetter("name"))



@app.route("/facultyprogrammes")
def get_programmes():
  id = request.args.get("id")
  result = es.search(
    index='programmes',
    query={
      "match" : {"faculty_id" : id}
    }
)
  response_list = []
  for prg in result["hits"]["hits"]:
    response_list.append(prg["_source"])
  return response_list


@app.route("/insertbasics",methods=["POST"])
def insert_basics():
  data = request.get_json()
  fdate = datetime.strptime(data["date"],"%d/%m/%Y %H:%M:%S")
  rating = int(data["rating"])
  room = data["room"]
  courses = es.search(
    index='courses',
    query={
    "bool": {
      "should": [
        { "match": { "week_type": 0 } },
        { "match": { "week_type": get_week_type(fdate.date()) } }
      ],
      "must": [
        { "match": { "room": room } },
        { "match": { "day": fdate.weekday()+1 } },
        { "range": {
            "start": {
              "lte":fdate.time().strftime("%H:%M:%S")
            }
          }
        },
        {
          "range": {
            "end": {
              "gte": fdate.time().strftime("%H:%M:%S")
            }
          }
        }
      ]
    }
  }
)
  for course in courses["hits"]["hits"]:
    es.index(
          index="basic_ratings",
          document={
            "rating" : rating,
            "course" : course["_source"]["name"],
            "date_time" : fdate
          }
        )
  return {"response":"rating inserted"}


@app.route("/currentcourse")
def get_current_course():
  data = request.get_json()
  fdate = datetime.strptime(data["date"],"%d/%m/%Y %H:%M:%S")
  room = data["room"]

  courses = es.search(
  index='courses',
      query={
      "bool": {
        "should": [
          { "match": { "week_type": 0 } },
          { "match": { "week_type": get_week_type(fdate.date()) } }
        ],
        "must": [
          { "match": { "room": room } },
          { "match": { "day": fdate.weekday()+1 } },
          { "range": {
              "start": {
                "lte":fdate.time().strftime("%H:%M:%S")
              }
            }
          },
          {
            "range": {
              "end": {
                "gte": fdate.time().strftime("%H:%M:%S")
              }
            }
          }
        ]
      }
    }
  )
  response_list = []
  for crs in courses["hits"]["hits"]:
    response_list.append(crs["_source"]["name"])
  return json.dumps(response_list), 200, {'Content-Type': 'application/json'}

@app.route("/currentcode")
def get_current_code():
  result = es.get(index='security_code', id=1, _source=['code'])
  code = result['_source']['code']
  return {"code":code}

def get_week_type(day: datetime):
  dt = day
  start = dt - timedelta(days=dt.weekday())
  end = start + timedelta(days=6)
  result = es.search(
  index='weeks',
  query={
    "bool": {
      "must": [
        { "match": { "start": start } },
        { "match": { "end": end } },
      ]
    }
  }
)
  if result["hits"]["hits"][0]["_source"]["id"] % 2 == 1:
    return 1
  else:
    return 0
  
    
if __name__ == '__main__':

  CORS(app)
  app.run(debug = True,host="0.0.0.0")

