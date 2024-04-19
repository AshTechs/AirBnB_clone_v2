#!/usr/bin/python3

""" Start a flask with application. """


from flask import Flask

app = Flask(__name__)


# Define the route for the root URL '/'
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Display 'Hello HBNB! """
    return "hello HBNB!"


if __name__ == "__main__":
    # Start the flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 500
    app.run(host='0.0.0.0', port=500)
