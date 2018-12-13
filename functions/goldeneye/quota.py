
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cybertool.users')

def get_quota(username):
  result = table.get_item(
    Key = {
      'username': username
    }
  )

  return {
    'free_quota': result['Item'].get('free_quota', 0),
    'paid_quota': result['Item'].get('paid_quota', 0)
  }

def reduce_quota(username, q, amount):
  new_free_quota = max(q['free_quota'] - amount, 0)
  if new_free_quota == 0:
    new_paid_quota = q['paid_quota'] - (amount - q['free_quota'])
  else:
    new_paid_quota = q['paid_quota']
  response = table.update_item(
    Key={
      'username': username
    },
    UpdateExpression='set free_quota = :free_quota, paid_quota = :paid_quota',
    ExpressionAttributeValues={
      ':free_quota': new_free_quota,
      ':paid_quota': new_paid_quota
    },
    ReturnValues='UPDATED_NEW'
  )

  return response['Attributes']