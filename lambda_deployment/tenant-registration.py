import json
import uuid
import requests


def register_tenant(event, context):
    print("event:",)
    print(event)
    print("context:")
    print(context)
    try:
        # Generate a unique user ID
        tenant_id = str(uuid.uuid4())

        # Get user details from event
        tenant_details = event
        print(tenant_details)
        
        # Add generated user ID to the user details
        tenant_details['userId'] = tenant_id
        print(tenant_details)
        
        # Validate tenant details 
        validate_tenant_details(tenant_details)
        create_admin_tenant(tenant_details)
        
        return {
            "statusCode": 200,
            "body": "Tenant creation is successful."
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

def validate_tenant_details(tenant_details):
    required_fields = ['tenantname', 'email']
    for field in required_fields:
        if field not in tenant_details or not tenant_details[field]:
            raise ValueError(f"{field.capitalize()} is required.")


def create_admin_tenant(tenant_details):
    try:
        url = "https://5npujorei3.execute-api.us-east-1.amazonaws.com/prod/user/tenant-admin"
        print("calling create admin tenant api")
        
        response=requests.post(url, json=tenant_details, timeout=5) 
        print("response:",response)
    except requests.RequestException as e:
        print(f"Error creating user: {e}")