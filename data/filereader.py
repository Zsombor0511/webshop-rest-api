import json
import os
from typing import Dict, Any, List

'''
Útmutató a fájl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    with open(JSON_FILE_PATH,"r",encoding="utf-8") as beolvasas:
        adatok = json.load(beolvasas)
    return adatok

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    adatok = load_json()
    felhasznalok = adatok["Users"]
    for user in felhasznalok:
        if user["id"] == user_id:
            return user
    raise ValueError("A felhasználó nem található")

def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    adatok = load_json()
    kosarak = adatok["Baskets"]
    for kosar in kosarak:
        if kosar["user_id"] == user_id:
            return kosar["items"]
    raise ValueError("Nincs kosara")

def get_all_users() -> List[Dict[str, Any]]:
    adatok = load_json()
    return adatok["Users"]

def get_total_price_of_basket(user_id: int) -> float:
    cikkek = get_basket_by_user_id(user_id)
    osszeg = 0
    for cikk in cikkek:
        osszeg = osszeg + (cikk["quantity"] * cikk["price"])
    return osszeg