from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify

app = Flask(__name__)
app.secret_key = "sadSJdsZMxcMC123231"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    if session['test'] == None:
        session['test'] = 'None'
    return render_template('test.html', empty_area=session['test'])

@app.route('/data/update/<uuid>', methods=['POST'])
def getClientData(uuid):
    data = request.json
    sended_dev_key = data['dev_key']
    print(f"dev_key is : {sended_dev_key}")
    if sended_dev_key == 'xssdQsdxcgtRS':
        session['test'] = data['empty_slots']
        return jsonify(success=True)
    else:
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)

# TODO Add database for current car positions
# You can either get all positions of the cars or get how many spaces left
# TODO Add sockets to change database according to live data from arduino server
# TODO get google maps data and if full reroute to another otopark 