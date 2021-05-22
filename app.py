from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import json

app = Flask(__name__)
app.secret_key = "sadSJdsZMxcMC123231"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parkdata.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    parks = db.relationship('Parking_lot', backref='author', lazy=True)
    
    def __repr__(self):
        return f"Developer(id : {self.id} | Password : {self.password})"

class Parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    slotAmount = db.Column(db.Integer, nullable=False)
    emptySlotAmount = db.Column(db.Integer, nullable=False)
    emptySlots = db.Column(db.Text, nullable=False)
    lastUpdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastUpdater = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)

    def __repr__(self):
        return f"Parking Lot(id : {self.id} | Location : {self.location_x}, {self.location_y} | Slot amount : {self.slotAmount} | Empty Slot Amount {self.emptySlotAmount} | Empty Slots : {json.loads(self.emptySlots)} | Last Update : {self.lastUpdate} | Updater : {self.lastUpdater})"

def create_Parking_lot(_location, _slotAmount, _emptySlotAmount, _emptySlots, _developer):
    x_loc, y_loc = _location
    _emptySlots = json.dumps(_emptySlots)
    parking_lot_a = Parking_lot(location_x= x_loc, location_y= y_loc, slotAmount=_slotAmount, emptySlotAmount=_emptySlotAmount, emptySlots=_emptySlots, lastUpdater=_developer.id)
    db.session.add(parking_lot_a)
    db.session.commit()

def update_Empty_Slot(parking_lot, _dev, _emptySlots):
    parking_lot.emptySlots = json.dumps(_emptySlots)
    parking_lot.lastUpdate = datetime.utcnow()
    parking_lot.lastUpdater = _dev.id
    db.session.commit()

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

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)

# TODO Add database for current car positions
# You can either get all positions of the cars or get how many spaces left
# TODO Add sockets to change database according to live data from arduino server
# TODO get google maps data and if full reroute to another otopark 