from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import json

app = Flask(__name__)
app.secret_key = "sadSJdsZMxcMC123231"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parkdata.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

devs = db.Table('devs',
                db.Column('dev_id', db.Integer, db.ForeignKey('developer.id')),
                db.Column('lot_id', db.Integer, db.ForeignKey('parking_lot.id')))

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    parks = db.relationship('Parking_lot', secondary= devs, backref= db.backref('developers', lazy='dynamic'))
    
    def __repr__(self):
        return f"Developer(id : {self.id} | Name : {self.name} | Password : {self.password})"

class Parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    slotAmount = db.Column(db.Integer, nullable=False)
    emptySlots = db.Column(db.Text, nullable=False)
    lastUpdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastUpdater = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)

    def __repr__(self):
        emptySlotArr = json.loads(self.emptySlots)
        return f"Parking Lot(id : {self.id} | Name : {self.name} | Location : {self.location_x}, {self.location_y} | Slot amount : {self.slotAmount} | Empty Slot Amount {len(emptySlotArr)} | Empty Slots : {emptySlotArr} | Last Update : {self.lastUpdate} | Updater : {self.lastUpdater})"

def create_Developer(_name, _password):
    dev = Developer(name=_name, password=_password)
    db.session.add(dev)
    db.session.commit()
    return dev

def create_Lot(_name, _location, _slotAmount, _emptySlots, _developer):
    x_loc, y_loc = _location
    _emptySlots = json.dumps(_emptySlots)
    parking_lot_a = Parking_lot(name= _name, location_x= x_loc, location_y= y_loc, slotAmount=_slotAmount, emptySlots=_emptySlots, lastUpdater=_developer.id)
    db.session.add(parking_lot_a)
    db.session.commit()
    return parking_lot_a

def update_Empty_Slot(parking_lot_id, _dev, _emptySlots):
    parking_lot = Parking_lot.query.filter_by(id=parking_lot_id).first()
    if parking_lot is None:
        return "Invalid parking lot"
    if parking_lot.developers.filter_by(id= _dev.id).first() is None:
        return "Unauthorized access"
    if len(_emptySlots) > parking_lot.slotAmount:
        return "Empty slots cannot be more than slot number"
    if len(_emptySlots) != 0:
        if max(_emptySlots) > parking_lot.slotAmount:
            return "Cannot have empty slot higher than the slot amount in the parking lot"
        if min(_emptySlots) < 1:
            return "Cannot have empty slot slower than 0"
    parking_lot.emptySlots = json.dumps(_emptySlots)
    parking_lot.lastUpdate = datetime.utcnow()
    parking_lot.lastUpdater = _dev.id
    db.session.commit()
    return "Successfully Updated"

def getParkingLotEmptySlotArr(lot_name):
    lot = Parking_lot.query.filter_by(name=lot_name).first()
    if lot is None:
        Exception("Wrong lot name")
    return json.loads(lot.emptySlots)

def getParkingLotEmptySlotNum(lot_name):
    return len(getParkingLotEmptySlotArr(lot_name))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html', empty_area=getParkingLotEmptySlotNum("MainLot"))

@app.route('/data/update/<dev_id>', methods=['POST'])
def getClientData(dev_id):
    data = request.json
    sended_password = data['dev_key']
    print(f"dev_key is : {sended_password}")
    dev = Developer.query.filter_by(id=dev_id).first()
    if (dev is None) or (not dev.password == sended_password):
        return jsonify("Invalid Credentials")
    return jsonify(update_Empty_Slot(data['lot_id'], dev, data['empty_slots']))

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)

# TODO get google maps data and if full reroute to another otopark 