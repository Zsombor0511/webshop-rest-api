from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json,update_item_in_basket,delete_item_in_basket
from data.filereader import get_user_by_id, get_basket_by_user_id, get_all_users, get_total_price_of_basket, load_json
from typing import List
from data.filehandler import copy_data_file

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try:
        user_dict = user.model_dump()
        add_user(user_dict)
        return JSONResponse(status_code = 201, content=user_dict)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))


@routers.post('/addshoppingbag', response_model=str)
def addshoppingbag(userid: int) -> str:
    try:
        if userid < 0:
            raise ValueError("Az azonosító nem lehet negatív")
        adatok = load_json()
        maxid=0
        for kosar in adatok["Baskets"]:
            if kosar["id"]>maxid:
                maxid = kosar["id"]
        ujid=maxid+1
        kosar = {
            "id":ujid,
            "user_id":userid,
            "items":[]
        }
        add_basket(kosar)
        return JSONResponse(status_code=201,content="Sikeres kosár hozzárendelés.")
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet == "Ennek a kosarnak a felhasznalo ID-ja nem letezik":
            raise HTTPException(status_code=404,detail=hiba_uzenet)
        else:
            raise HTTPException(status_code=400,detail=hiba_uzenet)        

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        if userid < 0:
            raise ValueError("Az azonosító nem lehet negatív")
        get_user_by_id(userid)
        item_dict = item.model_dump()
        add_item_to_basket(userid,item_dict)
        adatok = load_json()
        for kosar in adatok["Baskets"]:
            if kosar["user_id"] == userid:
                return JSONResponse(status_code=201, content=kosar)
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet in ["A felhasználó nem található", "Ennek a felhasznalonak nincs kosara"]:
            raise HTTPException(status_code = 404, detail=hiba_uzenet)
        else:
            raise HTTPException(status_code = 400, detail=hiba_uzenet)


@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        if userid < 0 or itemid < 0:
            raise ValueError("Az azonosító nem lehet negatív")

        get_user_by_id(userid)
        
        uj_adat_dict = updateItem.model_dump()
        update_item_in_basket(userid, itemid, uj_adat_dict)
        
        adatok = load_json()
        for kosar in adatok["Baskets"]:
            if kosar["user_id"] == userid:
                return JSONResponse(status_code=200, content=kosar)
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet in ["A felhasználó nem található", "Ennek a felhasznalonak nincs kosara", "Nincs ilyen termek a kosarban"]:
            raise HTTPException(status_code = 404, detail=hiba_uzenet)
        else:
            raise HTTPException(status_code = 400, detail=hiba_uzenet)

@routers.delete('/deleteitem', response_model=Basket)
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        if userid < 0 or itemid < 0:
            raise ValueError("Az azonosító nem lehet negatív")

        get_user_by_id(userid)
        delete_item_in_basket(userid,itemid)

        adatok = load_json()
        for kosar in adatok["Baskets"]:
            if kosar["user_id"] == userid:
                return JSONResponse(status_code=200, content=kosar)
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet in ["A felhasználó nem található","Ennek a felhasznalonak nincs kosara","Nincs ilyen termek a kosarban"]:
            raise HTTPException(status_code = 404, detail=hiba_uzenet)
        else:
            raise HTTPException(status_code = 400, detail=hiba_uzenet)

@routers.get('/user', response_model = User)
def user(userid: int) -> User:
    try:
        if userid < 0:
            raise ValueError("Az azonosító nem lehet negatív")

        felhasznalo = get_user_by_id(userid)
        
        return JSONResponse(status_code=200,content=felhasznalo)
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet == "Az azonosító nem lehet negatív":
            raise HTTPException(status_code = 400, detail=str(e))
        raise HTTPException(status_code = 404, detail=str(e))

@routers.get('/users', response_model = List[User])
def users() -> List[User]:
    try:
        felhasznalok=get_all_users()
        return JSONResponse(status_code=200, content=felhasznalok)
    except Exception as e:
        raise HTTPException(status_code = 400, detail=str(e))

@routers.get('/shoppingbag', response_model = List[Item])
def shoppingbag(userid: int) -> List[Item]:
    try:
        if userid < 0:
            raise ValueError("Az azonosító nem lehet negatív")

        get_user_by_id(userid)
        cikkek = get_basket_by_user_id(userid)

        return JSONResponse(status_code=200, content=cikkek)
    except ValueError as e:
        hiba_uzenet=str(e)
        if hiba_uzenet in ["Nincs kosara","A felhasználó nem található"]:
            raise HTTPException(status_code=404,detail=hiba_uzenet)
        else:
            raise HTTPException(status_code=400,detail=hiba_uzenet)

@routers.get('/getusertotal',response_model=float)
def getusertotal(userid: int) -> float:
    try:
        if userid < 0:
            raise ValueError("Az azonosító nem lehet negatív")

        get_user_by_id(userid)
        osszeg = get_total_price_of_basket(userid)

        return JSONResponse(status_code=200, content = osszeg)
    except ValueError as e:
        hiba_uzenet = str(e)
        if hiba_uzenet in ["A felhasználó nem található","Nincs kosara"]:
            raise HTTPException(status_code=404,detail=hiba_uzenet)
        else:
            raise HTTPException(status_code=400,detail=hiba_uzenet)


    
@routers.post('/save')
def save(source: str, dest: str):
    try:
        copy_data_file(source, dest)
        return JSONResponse(status_code=201, content=f"Sikeres mentés: {source} -> {dest}")
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@routers.post('/reload')
def reload(dest: str, source: str):
    try:
        copy_data_file(source, dest)
        return JSONResponse(status_code=200, content=f"Sikeres visszatöltés: {source} -> {dest}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
