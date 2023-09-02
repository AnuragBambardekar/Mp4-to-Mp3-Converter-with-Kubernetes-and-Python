import os
import requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing Credentials", 401)
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing Credentials", 401)
    
    # we forward it to the auth service endpoint (the implementation in the auth folder)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization":token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)