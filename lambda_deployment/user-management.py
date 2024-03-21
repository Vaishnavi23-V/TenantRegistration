import json
import boto3

client = boto3.client('cognito-idp')

def create_tenant_admin_user(event, context):
    print("event:",)
    print(event)
    print("context:")
    print(context)
    try:
        user_pool_id = 'us-east-1_jDEPOze1y'
        app_client_id = '5upvaeujc8no8lnr1tpjrhcuvc'

        # Parse request body to get tenant details
        tenant_details = event
        print(tenant_details)
        tenant_id = tenant_details['tenantId']
        tenant_admin_user_name = f'tenant-admin-{tenant_id}'
        print(tenant_admin_user_name)

        # Create user in Cognito user pool
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=tenant_admin_user_name,
            UserAttributes=[
                {'Name': 'email', 'Value': tenant_details['email']},
            ],
            TemporaryPassword='Temp123',  
            ForceAliasCreation=False
        )

        print("User creation response:", response)

        # Return successful response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "User created successfully"})
        }
    except Exception as e:
        # return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
