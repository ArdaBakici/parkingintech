from app import *

def load():
    db.create_all()
    dev = create_Developer("MasterDev", "deneme123")
    db.session.add(dev)
    lot = create_Lot("MainLot", (38.43082385998546, 27.14129463284438), 6, [], dev)
    db.session.add(lot)
    db.session.commit()

def initiate_park():
    loc_list = [["Çankaya Katlı Otoparkı", 38.420149679975815, 27.137890875859828],
                ["İzelman", 38.431730654083324, 27.155788513707098],
                ["Fuar Otoparkı", 38.431250, 27.145250],
                ["Alsancak otomatik otopark", 38.433417, 27.144694],
                ["Atatürk Spor salonu", 38.434278, 27.147722],
                ["Kordon katlı otopark", 38.441139, 27.145000],
                ["özel otoparklar", 38.439250, 27.145556],
                ["katlı özel otopark", 38.432139, 27.147500]]

    for loc in loc_list:
        name = loc[0]
        park_loc = loc[1:3]
        park_a = create_Park(name, park_loc)
        db.session.add(park_a)
    db.session.commit()

if __name__ == '__main__':
    #load()
    initiate_park()