import json
import dns.resolver
import hashlib

def handler(event, context):
  username = event['queryStringParameters'].get('username', None)
  domain = event['queryStringParameters'].get('domain', None)
  
    
  if not username or not domain:
    return errorResponse('No username or no domain specified')
  if event['httpMethod'] == 'POST':
    result = verify_domain_owner(username, domain)

    return {
      'statusCode': 200,
      'body': json.dumps({
        'success': True,
        'username': username,
        'domain': domain,
        'is_verified': result
      })
    }
  if event['httpMethod'] == 'GET':
    return successResponse({
      'txt_record': generate_txt_record(username, domain)
    })

def get_txt_records(domain):
  results = []
  try:
    result = dns.resolver.query(domain, 'TXT')
    for item in result:
      results.append(item.to_text())
    return results
  except Exception as e:
    print(e)
    pass
  return results

def verify_domain_owner(username, domain):
  txt_records = get_txt_records(domain)
  if len(txt_records) == 0:
    return False
  txt = generate_txt_record(username, domain)
  print(str(txt))
  for txt_record in txt_records:
    if txt == json.loads(txt_record):
      return True
  
  return False
  
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
    })
  }

def generate_txt_record(username, domain):
  hashstring = '{domain:' + domain + ',owner:' + username+ '}'
  hash_object = hashlib.sha1(hashstring.encode())
  txt = 'cybertool-site-verification=' + hash_object.hexdigest()
  return txt

if __name__ == '__main__':
  event = {
    "httpMethod": "POST",
    "queryStringParameters": {
      "username": 'tienanhnguyen0108',
      "domain": 'christianwen.com'
    }
  }
  result = handler(event, None)
  print(result)



