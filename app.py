from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify

app = Flask(__name__)
app.secret_key = "sadSJdsZMxcMC123231"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    if not session.get('empty-area'):
        session['empty-area'] = 'none'
    return render_template('test.html', empty_area=session['empty-area'])

@app.route('/data/update/<uuid>', methods=['POST'])
def getClientData(uuid):
    data = request.json
    sended_dev_key = data['dev_key']
    print(f"dev_key is : {sended_dev_key}")
    session['empty-area'] = data['empty_slots']
    if sended_dev_key == 'xssdQsdxcgtRS':
        print('success')
        print(f"Sucsess : {session['empty-area']}")
        return jsonify(success=True)
    else:
        return jsonify(success=False)

def create_app(config_filename):
    app = Flask(__name__)
    app.secret_key = "sadSJdsZMxcMC123231"
    return app

if __name__ == '__main__':
    app.run(debug=True)

# TODO Add database for current car positions
# You can either get all positions of the cars or get how many spaces left
# TODO Add sockets to change database according to live data from arduino server
# TODO get google maps data and if full reroute to another otopark 