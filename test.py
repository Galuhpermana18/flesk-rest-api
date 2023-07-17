import requests

BASE = "http://127.0.0.1:5000/"

headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
}

def insert():
    data ={"tglPendaftaran": "2023-05-31", "nama": "Ali", "jenisKelamin":"Laki-laki", "jenisKursus":"Kursus Bahasa Java"}

    response = requests.put(BASE+ "peserta/insert/0", json=data, headers=headers)
    print(response.json())

def update():
    data ={"tglPendaftaran": "2023-06-01", "nama": "Dimas", "telp":"021-000-000", "jenisKelamin":"Laki-laki", "jenisKursus":"Kursus Bahasa Java"}

    response = requests.patch(BASE+ "peserta/update/0", json=data, headers=headers)
    print(response.json())

def deleteAll():
    response = requests.delete(BASE+ "peserta/delete")
    print(response)

def deleteData():
    response = requests.delete(BASE+ "peserta/delete/0")
    print(response)

def getData():
    response = requests.get(BASE + "peserta/0")
    print(response.json())

def getAll():
    response = requests.get(BASE + "peserta")
    print(response.json())


# deleteData()
# insert()
update()
# getAll()