import json
import boto3
import urllib.request

acm = boto3.client('acm')

print('Loading function...')

def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=4)) 
    message = json.dumps(event, indent=2)
## Each action has a slightly different dictionary set. Let's brute force it.
    try:
        action = event['eventName']
        account = event['recipientAccountId']        
        eventTime = event['eventTime']
        principalId = event['userIdentity']['principalId']
        try:
            certificateArn = event['requestParameters']['certificateArn']
        except KeyError:
            certificateArn = event['responseElements']['certificateArn']
        certInfo = acm.describe_certificate(CertificateArn = certificateArn)
        domainName = certInfo['Certificate']['DomainName']
## The key error comes from the action variable when it occurs.
    except KeyError:
        action = event['detail']['eventName']
        account = event['account']
        certificateArn = event['detail']['requestParameters']['certificateArn']
        certInfo = acm.describe_certificate(CertificateArn = certificateArn)
        domainName = certInfo['Certificate']['DomainName']
        eventTime = event['detail']['eventTime']
        principalId = event['detail']['userIdentity']['principalId']
