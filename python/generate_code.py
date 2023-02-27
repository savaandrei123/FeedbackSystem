from elasticsearch import Elasticsearch
import random
import schedule


ELASTIC_CLOUD_ID = 'S8t3CIJmSP2AGsQDL1GWnQ'
ELASTIC_CLOUD_URL = 'https://8f9677360fc34e2eb943d737b2597c7b.us-east-1.aws.found.io:9243/'
ELASTIC_CLOUD_USER = 'elastic'
ELASTIC_CLOUD_PASSWORD = 'AWbtmGda2Q7BI2bYpdjyF4qd'

es = Elasticsearch(
    [ELASTIC_CLOUD_URL],
    http_auth=(ELASTIC_CLOUD_USER, ELASTIC_CLOUD_PASSWORD),
    scheme="https",
)

def security_code():
  print("security_code")
  new_code = {
      "code" : random.randint(1000,9999)
  }
  es.index(index="security_code", id=1, document=new_code)


def scheduler():
  #schedule.every(15).seconds.do(security_code)
  schedule.every().day.at("08:00").do(security_code)
  schedule.every().day.at("10:00").do(security_code)
  schedule.every().day.at("12:00").do(security_code)
  schedule.every().day.at("14:00").do(security_code)
  schedule.every().day.at("16:00").do(security_code)
  schedule.every().day.at("18:00").do(security_code)
  schedule.every().day.at("20:00").do(security_code)

  while True:
    schedule.run_pending()

print("Starting...")
scheduler()