import json
import boto3

client = boto3.client('cognito-idp')

def create_tenant_admin_user(event, context):
    print("event:", event)
    try:
        user_pool_id = 'us-east-1_jDEPOze1y'

        # Get tenant details from event
        tenant_details = event
        # Get tenant_id from tenant_details
        tenant_id = tenant_details['tenantId']
        print("tenant-details", tenant_details)
        tenant_admin_user_name = f'tenant-admin-{tenant_id}'

        print("Creating user group for tenant:", tenant_id)
        # Create user group
        group_response = client.create_group(
            GroupName=f'Tenant_{tenant_id}_Admin',  
            UserPoolId=user_pool_id,
            Description=f'Admins group for Tenant {tenant_id}'
        )
        group_name = group_response['Group']['GroupName']
        print("User group created:", group_name)

        # Create tenant admin user within the group
        print("Creating tenant admin user:", tenant_admin_user_name)
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=tenant_admin_user_name,
            UserAttributes=[
                {'Name': 'email', 'Value': tenant_details['email']},
            ],
            TemporaryPassword='Temp@1234',  
            ForceAliasCreation=False
        )

        # Add the user to the admin group
        print("Adding user to group:", group_name)
        client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=tenant_admin_user_name,
            GroupName=group_name
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
