import json
import boto3
import decimal
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cybertool.users')

promotion_codes = json.loads(os.environ.get('PROMOTION_CODES', []))

def lambda_handler(event, context):
    # TODO implement
    username = event['queryStringParameters']['username']
    if event['httpMethod'] == 'GET':
      type = event['queryStringParameters'].get('type', None)
      if type == 'get_quota_from_promo_code':
        promo_code = event['queryStringParameters'].get('promo_code', None)
        response = get_quota_from_promo_code(username, promo_code)
        if not response:
          return errorResponse('Quota code not found')
        print("from promo_code result", response)
        return successResponse(response)
          
      if type == 'get_free_quota': 
        if should_get_free_quota(username):
          response = get_free_quota(username)
          print(response)
          return successResponse(response)
        else:
          return errorResponse('You already get the free quota for this month!')
      else:
        q = get_quota(username)
    
        return {
          'statusCode': 200,
          'body': json.dumps(q)
        }
        
    #if event['httpMethod'] == 'POST':
        
 
def get_quota(username):
  result = table.get_item(
    Key = {
      'username': username
    }
  )
  data = result.get('Item', {})
  return {
    'free_quota': int(data.get('free_quota', 0)),
    'paid_quota': int(data.get('paid_quota', 0))
  }

def should_get_free_quota(username):
  result = table.get_item(
    Key = { 'username': username },
    AttributesToGet = ['last_free_quota_renewal']
  )
  now = datetime.now()
  last_free_quota_renewal = result.get('Item', {}).get('last_free_quota_renewal', None)
  if not last_free_quota_renewal:
     return True
  last = datetime.strptime(last_free_quota_renewal, '%Y-%m-%d %H:%M:%S.%f')
  if last.year < now.year or last.month < now.month:
     return True
  return False
  
  
def get_free_quota(username):
  response = table.update_item(
    Key={
      'username': username
    },
    UpdateExpression='set free_quota = :free_quota, last_free_quota_renewal = :last_free_quota_renewal',
    ExpressionAttributeValues={
        ':free_quota': 600,
        ':last_free_quota_renewal': str(datetime.now())
    },
    ReturnValues='UPDATED_NEW'
  )
  return response['Attributes']
  
def get_quota_from_promo_code(username, promo_code):
  if not promo_code:
    return None
  paid_quota = 0
  for code in promotion_codes:
      if code['promo_code'] == promo_code:
          paid_quota = code['paid_quota']
  
  print('get paid_quota from code', paid_quota)
  if not paid_quota:
      return None
  response = table.update_item(
      Key={
        'username': username
      },
      UpdateExpression='set paid_quota = paid_quota + :paid_quota',
      ExpressionAttributeValues={
          ':paid_quota': paid_quota
      },
      ReturnValues='UPDATED_NEW'
  )
  return response['Attributes']
    
def errorResponse(message):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': False,
            'error': message
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