import json
import decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

table = boto3.resource('dynamodb').Table('cybertool.history')

def handler(event, context=None):
  username = event["queryStringParameters"].get("username", None)
  if not username: 
    return errorResponse('No username provided')
  data = get_history(username)
  return successResponse({"history": data})

def get_history(username):
  response = table.query(
    KeyConditionExpression=Key('username').eq(username),
    ScanIndexForward=False
  )
  return response.get("Items",[])

def errorResponse(error):
  return {
    'statusCode': 200,
    'body': json.dumps({
      'success': False,
      'error': error
    })
  }

def successResponse(data):
  return {
    'statusCode': 200,
    'body': json.dumps({
      'success': True,
      'data': data
    }, cls=DecimalEncoder)
  }

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
  def default(self, o): # pylint: disable=E0202
    if isinstance(o, decimal.Decimal):
      return str(o)
    return super(DecimalEncoder, self).default(o)

if __name__ == '__main__':
  event = {
    "queryStringParameters": {
      "username": "2404a44a-8276-4c27-a3e3-f17dd9dd5b36"
    }
  }
  result = handler(event=event)
  print(result)