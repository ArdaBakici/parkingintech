from app import *

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

if __name__ == '__main__':
    load()
    initiate_park()