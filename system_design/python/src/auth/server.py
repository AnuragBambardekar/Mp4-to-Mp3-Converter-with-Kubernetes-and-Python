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
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
# print(server.config["MYSQL_HOST"]) # to get the set values, just print it.

# create route
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    # auth.username
    # auth.password
    if not auth:
        return "missing credentials", 401
    
    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )

    if res > 0:
        # user exists in our DB
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        # check if username and password in DB is same as in Request
        if auth.username != email or auth.password != password:
            return "Invalid credentials!", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
        
    else:
        # user doesn't exist in our DB
        return "Invalid credentials!", 401

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing Credentials",401
    
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "Not Authorized",403
    
    return decoded,200

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username":username,
            "exp":datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat":datetime.datetime.utcnow(),
            "admin":authz
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    # print(__name__)
    server.run(host="0.0.0.0",port=5000,) # this tells your OS to listen on all public IP's

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