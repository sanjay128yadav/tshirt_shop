from instamojo_wrapper import Instamojo

API_KEY = "test_7b213440232364c830e1cff15c0"
AUTH_TOKEN = "test_05354ff312181df156c9ec2ed08"

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');

# Create a new Payment Request
response = api.payment_request_create(
    amount='11',
    purpose='Testing',
    send_email=True,
    email="sanjay128yadav@gmail.com",
    redirect_url="http://localhost:8000/handle_redirect"
    )

print (response['payment_request']['longurl'])