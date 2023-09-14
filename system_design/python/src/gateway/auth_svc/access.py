import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        print("Missing Creds!!")
        return None, ("Missing Credentials!!",401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )

    # if basicAuth:
    #     return None, (os.environ.get('AUTH_SVC_ADDRESS'),response.status_code)
    # print(response.status_code)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)