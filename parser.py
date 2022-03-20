import json
import boto3
import urllib.request

acm = boto3.client('acm')

print('Loading function...')

def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=4)) 
    message = json.dumps(event, indent=2)
    ## ExportCertificate nests all these variables in the['detail'] sub-dict, prompting this gnarly try-except and if statements.
    try:
        action = event['eventName'] 
    except:
        action = event['detail']['eventName']
    title = "ACM change detected: " + action
    
    
    if (action == 'ExportCertificate'):
        account = event['account']        
        certificateArn = event['detail']['requestParameters']['certificateArn']
        certInfo = acm.describe_certificate(CertificateArn = certificateArn)
        domainName = certInfo['Certificate']['DomainName']
        eventTime = event['detail']['eventTime']
        principalId = event['detail']['userIdentity']['principalId']

    else:
        account = event['recipientAccountId']        
        eventTime = event['eventTime']
        principalId = event['userIdentity']['principalId']

    
    ## certificateArn and domainName occur differently in the response syntax based on the eventName. 
    ## Here are four cases:
    
        if action == 'DeleteCertificate':
            certificateArn = event['requestParameters']['certificateArn']
            certInfo = acm.describe_certificate(CertificateArn = certificateArn)
            domainName = certInfo['Certificate']['DomainName']
    
        if action == 'ImportCertificate':
            certificateArn = event['responseElements']['certificateArn']
            certInfo = acm.describe_certificate(CertificateArn = certificateArn)
            domainName = certInfo['Certificate']['DomainName']
            
        if action == 'RequestCertificate':
            certificateArn = event['responseElements']['certificateArn']
            domainName = event['requestParameters']['domainName']
        
        if action == 'ResendValidationEmail':
            certificateArn = event['requestParameters']['certificateArn']
            domainName = event['requestParameters']['domain']
            
    print(domainName)
    
    
    
    
    ## Gotta find a better way to handle the ExportCertificate differences
    ## Do I move it to another function or just add a bunch of ugly exceptions?
    ## To avoid forgetting I need the following six variables to send to Jira
    ### Action
    ### Account
    ### certificateArn
    ### domainName
    ### eventTime
    ### principalId
    
