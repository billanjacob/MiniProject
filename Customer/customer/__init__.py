from flask import Flask

app = Flask(__name__)
app.secret_key = "super secret key"

from customer import views
from customer import customeractions
from customer import guest
