from flask import Flask, render_template
import os
from dotenv import dotenv_values

env_config = dotenv_values('.env')

value = os.environ.get('IO_KEY')

value = os.environ['IO_KEY'] if ('IO_KEY' in os.environ) else env_config['IO_KEY']

print(value)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title=value)

if __name__ == '__main__':
    app.run(debug=True)