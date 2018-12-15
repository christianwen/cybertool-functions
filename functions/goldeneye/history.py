
import uuid
import time
import datetime

import boto3

table = boto3.resource('dynamodb').Table('cybertool.history')

def update_history(username, data):
  # get the id by concatenate current timestamp with uuid
  id = str(int(time.time()*1000)) + '-' + str(uuid.uuid4())
  data["id"] = id
  data["username"] = username
  data["created_at"] = str(datetime.datetime.utcnow().isoformat())

  response = table.put_item(
    Item = data
  )
  # return response["Attributes"]

if __name__ == '__main__':
  username = 'christianwen'
  data = {
    "target": "hn-ams.edu.vn",
    "duration": 20
  }

  update_history(username=username, data=data)