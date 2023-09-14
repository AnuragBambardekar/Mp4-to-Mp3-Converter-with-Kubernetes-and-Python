import jwt, datetime, os
from flask import Flask, request # squiggly lines will show because installations are local(venv)
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
# print(server.config["MYSQL_HOST"]) # to get the set values, just print it.
print("MYSQL_HOST:", os.environ.get("MYSQL_HOST"))
print("MYSQL_USER:", os.environ.get("MYSQL_USER"))
print("MYSQL_PASSWORD:", os.environ.get("MYSQL_PASSWORD"))
print("MYSQL_DB:", os.environ.get("MYSQL_DB"))
print("MYSQL_PORT:", os.environ.get("MYSQL_PORT"))


# create route
@server.route("/login", methods=["POST"])
def login():
    """Handles login functionality.
    Checks if user exists in the DB and returns a JWT.
    """

    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    # Check DB for user
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    # Check result list to generate JWT or deny access
    if result > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)

    else:
        return "Wrong username or password", 401

@server.route("/validate", methods=["POST"])
def validate():
    """Validates a JWT within a request."""

    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"],
        )
        print(decoded)
        return decoded, 200
    except jwt.ExpiredSignatureError:
        return "JWT has expired", 401
    except jwt.InvalidTokenError:
        return f"Invalid JWT: {encoded_jwt}", 401
    except:
        return "Unauthorized", 403
    

def createJWT(username, secret, is_admin):
    """Creates a JWT.
    Default expiration is 24 hrs.
    """

    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin,
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    # print(__name__)
    server.run(host="0.0.0.0",port=5000,debug=True) # this tells your OS to listen on all public IP's

    """
    The host is the server that is hosting our application.
    In our case, the server that is hosting our flask application is the docker container
    that it is running in. So, we need to tell our flask app to listen on our Dcoker
    container's IP address. But, the docker container's IP address is subject to change.
    So, instead of setting it to the static IP address of our Dcoker container, we set
    it to 0.0.0.0 (Wild Card). if we don;t configure this, it will listen to the localhost
    and it is only accessible from within the host, therefore outside requests sent to our
    Docker container would never actually be sent to our Flask app, because the loopback
    address isn't publicly accessible.
    """