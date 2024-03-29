from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify
import flask_talisman
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, time
import json
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TRAFFIC_RADIUS = 300 # diameter of circle that will be used to check traffic amount around a car park
TRAFFIC_DATA_REFRESH_TIME = 60

app = Flask(__name__)
    
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        '*.gstatic.com',
        '*.googleapis.com',
        '*.here.com',
        '\'unsafe-eval\'',
        '*.hereapi.com',
        'blob:'
    ]
}

talisman = Talisman(app, content_security_policy=csp)
app.secret_key = "sadSJdsZMxcMC123231"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parkdata.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
port = 587

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
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    slotAmount = db.Column(db.Integer, nullable=False)
    emptySlots = db.Column(db.Text, nullable=False)
    lastUpdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastUpdater = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)

    def __repr__(self):
        emptySlotArr = json.loads(self.emptySlots)
        return f"Parking Lot(id : {self.id} | Name : {self.name} | Address : {self.address} | Location : {self.location_x}, {self.location_y} | Slot amount : {self.slotAmount} | Empty Slot Amount {len(emptySlotArr)} | Empty Slots : {emptySlotArr} | Last Update : {self.lastUpdate} | Updater : {self.lastUpdater})"

class Car_park(db.Model):
    # Difference between this and Parking_lot this one does not support empty slot reading and just and not smart
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    jam_factor = db.Column(db.Float, nullable=False)
    lastUpdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Car Park(id : {self.id} | Name : {self.name} | Address : {self.address} | Location : {self.location_x}, {self.location_y}) | Jam Factor : {self.jam_factor} | Last Update {self.lastUpdate}"

def create_Developer(_name, _password):
    dev = Developer(name=_name, password=_password)
    db.session.add(dev)
    db.session.commit()
    return dev

def create_Lot(_name, _address, _location, _slotAmount, _emptySlots, _developer):
    x_loc, y_loc = _location
    _emptySlots = json.dumps(_emptySlots)
    parking_lot_a = Parking_lot(name= _name, address= _address, location_x= x_loc, location_y= y_loc, slotAmount=_slotAmount, emptySlots=_emptySlots, lastUpdater=_developer.id)
    db.session.add(parking_lot_a)
    db.session.commit()
    return parking_lot_a

def create_Park(_name, _address, _location):
    loc_x, loc_y = _location
    park_a = Car_park(name=_name, address= _address, location_x=loc_x, location_y=loc_y, jam_factor=calculateJamFactor((loc_x, loc_y, TRAFFIC_RADIUS)))
    db.session.add(park_a)
    db.session.commit()

    return park_a

def update_Empty_Slot(parking_lot, _dev, _emptySlots):
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

def getParkingLotEmptySlotArr(lot_id):
    lot = Parking_lot.query.filter_by(id=lot_id).first()
    if lot is None:
        Exception("Wrong lot id")
    return json.loads(lot.emptySlots)

def getParkingLotEmptySlotNum(lot_id):
    return len(getParkingLotEmptySlotArr(lot_id))

def updateParkJamFactor(park, jam_factor):
    park.jam_factor = jam_factor
    park.lastUpdate = datetime.utcnow()
    db.session.commit()

def calculateJamFactor(location):
    base_url = "https://traffic.ls.hereapi.com"
    url_path = "/traffic/6.2/"
    resource = "flow"
    data_type = ".json"
    #latitude, longitude, diameter
    location = f"?prox={location[0]},{location[1]},{location[2]}"
    api_key = "&apiKey=H9eImXWLstldKWISj-5HXAkiQpP5IOyV_uXjAc6lkyw"
    get_url =  base_url + url_path + resource + data_type + location + api_key
    res = requests.get(get_url)
    res_json = res.json()
    # each dictionary is inside a list
    lot_jam_factor = 0
    jam_factor_amount = 0
    base_json = res_json['RWS'][0]['RW']
    for flow_datas in base_json:
        fi_data = flow_datas['FIS'][0]['FI']
        for current_flow in fi_data:
            jam_factor = current_flow['CF'][0]['JF']
            if jam_factor == -1.0:
                jam_factor = 0
            lot_jam_factor += jam_factor
            jam_factor_amount += 1
    return lot_jam_factor/jam_factor_amount

def getRecomendedLot():
    availableLots = [f for f in Parking_lot.query.all() if getParkingLotEmptySlotNum(f.id) > 0]
    if len(availableLots) > 0:
        return availableLots[0] # TODO make this one elected by the position of the client or traffic
    else:
        least_traffic_park = {"park": None, "jam": 20}
        for park in Car_park.query.all():
            jam_factor = None
            deltaTime = datetime.utcnow() - park.lastUpdate
            if deltaTime.total_seconds() > TRAFFIC_DATA_REFRESH_TIME:
                jam_factor = calculateJamFactor((park.location_x, park.location_y, TRAFFIC_RADIUS))
            else:
                jam_factor = park.jam_factor
            if jam_factor < least_traffic_park["jam"]:
                least_traffic_park["jam"] = jam_factor
                least_traffic_park["park"] = park
            updateParkJamFactor(park, jam_factor)
        return least_traffic_park["park"]

def send_email(message):
    #us2.smtp.mailhostbox.com
    #smtp.parking-in.tech
    with smtplib.SMTP("smtp.parking-in.tech", port) as server:
        pass
        #server.login("info@parking-in.tech", "CElqRZc2")
        #server.sendmail("info@parking-in.tech", "info@parking-in.tech", message)

def load():
    db.create_all()
    dev = create_Developer("MasterDev", "deneme123")
    db.session.add(dev)
    lot = create_Lot("Akıllı Otopark", "Kültür, Plevne Blv., 35220 Konak/İzmir", (38.43082385998546, 27.14129463284438), 6, [], dev)
    db.session.add(lot)
    dev.parks = [lot]
    db.session.commit()

def initiate_park():
    loc_list = [["Çankaya Katlı Otoparkı", "Çankaya, 939. Sk. NO:1, 35280 Konak/İzmir", 38.420149679975815, 27.137890875859828],
                ["İzelman", "Kahramanlar, İşçiler Cd. No:130, 35250 Konak/İzmir", 38.431730654083324, 27.155788513707098],
                ["Fuar Otoparkı", "Mimar Sinan, Kültürpark, İzmir Fuarı, 35220 Konak/İzmir", 38.43070301007513, 27.14604547939751],
                ["Alsancak Otomatik Otopark", "Mimar Sinan, 1408. Sk. No: 8, 35220 Konak/İzmir", 38.433535797748696, 27.144715737941358],
                ["Atatürk Spor Salonu", "Mimar Sinan, Atatürk Spor Salonu, 1486. Sk. No:2/1, 35220 Konak/İzmir", 38.43421875129906, 27.147593538528948],
                ["Kordon Katlı Otopark", "Alsancak, 1476/1. Sk. No:1, 35220 Konak/İzmir", 38.44119351340975, 27.145624216239195],
                ["Özel Otoparklar", "Alsancak, 1460. Sk. No:17, 35220 Konak/İzmir", 38.4392457298387, 27.145427213297957],
                ["Katlı Özel Otopark", "Mimar Sinan, 1400. Sk. 11 A, 35220 Konak/İzmir", 38.43221786841943, 27.147534409927424]]

    for loc in loc_list:
        name = loc[0]
        address = loc[1]
        park_loc = loc[2:4]
        park_a = create_Park(name, address, park_loc)
        db.session.add(park_a)
    db.session.commit()

load()
initiate_park()

@app.route('/')
def home():
    lot = Parking_lot.query.first()
    empty_lot = getParkingLotEmptySlotArr(lot.id) # TODO decide this by region
    lot_list = [[f.name, f.address, f.location_x, f.location_y] for f in Parking_lot.query.all()]
    park_list = [[f.name, f.address, f.location_x, f.location_y] for f in Car_park.query.all()]
    recomendedLot = getRecomendedLot()
    recLotLoc = [recomendedLot.location_x, recomendedLot.location_y]
    return render_template('home.html', empty_area= empty_lot, empty_area_len= len(empty_lot), slot_num=lot.slotAmount, col_num= 6,
    list_of_lots= lot_list,list_of_parks= park_list,recomended_lot= recLotLoc)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/who')
def whois():
    return render_template('whois.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/success', methods=['POST'])
def contact_success():
    try:
        Exception("No longer working")
        name = request.form.get('name' , None)
        email = request.form.get('email' , None)
        phone = request.form.get('phone' , None)
        user_message = request.form.get('message' , None)
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{name} Kullanıcısından İletişim Formu"
        message["From"] = "info@parking-in.tech"
        message["To"] = "info@parking-in.tech"
        
        html = f"""\
                <html>
                <body>
                    <p><b>İsim Soyisim :</b> {name}</p><br>
                    <p><b>Email :</b> {email}</p><br>
                    <p><b>Telefon :</b> {phone}</p><br>
                    <p><b>Kullanıcı Mesajı :</b> <br>{user_message}</p>
                </body>
                </html>
                """
        message.attach(MIMEText(html, "html"))
        send_email(message.as_string())
        return render_template('contact_success.html')
    except:
        return redirect(url_for('contact_fail'))
    
@app.route('/contact/fail')
def contact_fail():
    return render_template('contact_fail.html')

@app.route('/data/update/<dev_id>', methods=['POST'])
def getClientData(dev_id):
    data = request.json
    sended_password = data['dev_key']
    dev = Developer.query.filter_by(id=dev_id).first()
    lot = Parking_lot.query.filter_by(id=data['lot_id']).first()
    if (dev is None) or (not dev.password == sended_password):
        return jsonify("Invalid Credentials")
    return jsonify(update_Empty_Slot(lot, dev, data['empty_slots']))

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)

# TODO get google maps data and if full reroute to another otopark 
