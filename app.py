from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(message='jhgyfvb vyghbjn'),404



@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name, age):
    if age < 18:
        return jsonify(message= name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


if __name__ == '__main__':
    app.run()