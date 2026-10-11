import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    with open(JSON_FILE_PATH,"r",encoding="utf-8") as beolvasas:
        adatok = json.load(beolvasas)
    return adatok

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH,"w",encoding="utf-8") as kiiras:
        json.dump(data,kiiras,indent=4,ensure_ascii=False)


def add_user(user: Dict[str, Any]) -> None:
    adatok = load_json()
    for felhasznalo in adatok["Users"]:
        if felhasznalo["id"] == user["id"]:
            raise ValueError("Ez a felhasználó ID már létezik!")
    adatok["Users"].append(user)
    save_json(adatok)

def add_basket(basket: Dict[str, Any]) -> None:
    adatok = load_json()
    felhasznalok = adatok["Users"]
    van = False
    for user in felhasznalok:
        if user["id"] == basket["user_id"]:
            van = True
            break
    if van==False:
        raise ValueError("Ennek a kosarnak a felhasznalo ID-ja nem letezik")
    kosarak = adatok["Baskets"]
    for kosar in kosarak:
        if kosar["user_id"] == basket["user_id"]:
            raise ValueError("Ennek az embernek mar van kosara")
        if kosar["id"] == basket["id"]:
            raise ValueError("Ez a kosar mar letezik")
    adatok["Baskets"].append(basket)
    save_json(adatok)
    
    

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    adatok = load_json()
    kosarvan = False
    itemvan = False
    for kosar in adatok["Baskets"]:
        if kosar["user_id"] == user_id:
            kosarvan = True
            for cikk in kosar["items"]:
                if cikk["item_id"] == item["item_id"]:
                    itemvan = True
                    cikk["quantity"] += item["quantity"]
                    break
            if itemvan == False:
                kosar["items"].append(item)
            break
    if kosarvan==False:
        raise ValueError("Ennek a felhasznalonak nincs kosara")
    save_json(adatok)

def update_item_in_basket(user_id: int, item_id: int, uj_adat: Dict[str, Any]) -> None:
    adatok = load_json()
    kosar_megvan = False
    item_megvan = False
    
    for kosar in adatok["Baskets"]:
        if kosar["user_id"] == user_id:
            kosar_megvan = True
            for cikk in kosar["items"]:
                if cikk["item_id"] == item_id:
                    item_megvan = True
                    # Felülírjuk az adatokat:
                    cikk["name"] = uj_adat["name"]
                    cikk["brand"] = uj_adat["brand"]
                    cikk["price"] = uj_adat["price"]
                    cikk["quantity"] = uj_adat["quantity"]
                    break
            break
            
    if kosar_megvan == False:
        raise ValueError("Ennek a felhasznalonak nincs kosara")
    if item_megvan == False:
        raise ValueError("Nincs ilyen termek a kosarban")
        
    save_json(adatok)

def delete_item_in_basket(userid: int, itemid: int) -> None:
    adatok = load_json()
    kosarvan = False
    item_megvan = False

    for kosar in adatok["Baskets"]:
        if kosar["user_id"] == userid:
            kosarvan = True
            for cikk in kosar["items"]:
                if cikk["item_id"] == itemid:
                    item_megvan = True
                    kosar["items"].remove(cikk)
                    break
            break
    
    if kosarvan == False:
        raise ValueError("Ennek a felhasznalonak nincs kosara")
    if item_megvan == False:
        raise ValueError("Nincs ilyen termek a kosarban")
    
    save_json(adatok)

def copy_data_file(source: str, dest: str) -> None:
    base_dir = os.path.dirname(__file__)
    source_path = os.path.join(base_dir, source)
    dest_path = os.path.join(base_dir, dest)
    
    if not os.path.exists(source_path):
        raise ValueError(f"A forrásfájl ({source}) nem található!")

    with open(source_path, "r", encoding="utf-8") as beolvasas:
        adatok = json.load(beolvasas)
    
    with open(dest_path, "w", encoding="utf-8") as kiiras:
        json.dump(adatok, kiiras, indent=4,ensure_ascii=False)
    
