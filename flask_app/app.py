from flask import Flask
from routes.interviews import bp
from routes.answers import bp2

app = Flask(__name__)

app.register_blueprint(bp)
app.register_blueprint(bp2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
