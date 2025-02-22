import re
import html
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или список конкретных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_maker_list(country: str):
    url = "https://www.arkmotors.kr/search/getMakerList"
    payload = {"country": country}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }
    response = requests.post(url, headers=headers, data=payload)
    content = response.json()
    return content.get("data", [])


def get_model_list(maker: str):
    url = "https://www.arkmotors.kr/search/getModelList"
    payload = {"maker": maker}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }
    response = requests.post(url, headers=headers, data=payload)
    content = response.json()
    return content.get("data", [])


def get_detail_model_list(model: str):
    url = "https://www.arkmotors.kr/search/getDetailModelList"
    payload = {"model": model}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }
    response = requests.post(url, headers=headers, data=payload)
    content = response.json()
    return content.get("data", [])


def get_grade_list(detail_model: str):
    url = "https://www.arkmotors.kr/search/getGradeList"
    payload = {"detail-model": detail_model}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }
    response = requests.post(url, headers=headers, data=payload)
    content = response.json()
    return content.get("data", [])


def get_detail_grade_list(grade: str):
    url = "https://www.arkmotors.kr/search/getDetailGradeList"
    payload = {"grade": grade}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }
    response = requests.post(url, headers=headers, data=payload)
    content = response.json()
    return content.get("data", [])


def fetch_cars(
    country: str = "kor",
    page: int = 1,
    order: str = "",
    ascending: str = "desc",
    view: str = "image",
    customSelect: str = "24",
    carName: str = "",
    maker: str = "",
    model: str = "",
    dmodel: str = "",
    grade: str = "",
    dgrade: str = "",
    price_min: str = "",
    price_max: str = "",
    year_min: str = "",
    year_max: str = "",
    usekm_min: str = "",
    usekm_max: str = "",
    fuel: str = "",
    mission: str = "",
    color: str = "",
    carNo: str = "",
    carPlateNumber: str = "",
    vehicle_model: str = "",
    vehicle_dmodel: str = "",
    vehicle_name: str = "",
    tab: str = "model",
    detailSearch: str = "close",
    type_: str = "",
):
    base_url = f"https://www.arkmotors.kr/search/model/{country}/{page}"
    params = {
        "order": order,
        "ascending": ascending,
        "view": view,
        "customSelect": customSelect,
        "carName": carName,
        "maker": maker,
        "model": model,
        "dmodel": dmodel,
        "grade": grade,
        "dgrade": dgrade,
        "price-min": price_min,
        "price-max": price_max,
        "year-min": year_min,
        "year-max": year_max,
        "usekm-min": usekm_min,
        "usekm-max": usekm_max,
        "fuel": fuel,
        "mission": mission,
        "color": color,
        "country": country,
        "carNo": carNo,
        "carPlateNumber": carPlateNumber,
        "vehicle-model": vehicle_model,
        "vehicle-dmodel": vehicle_dmodel,
        "vehicle-name": vehicle_name,
        "tab": tab,
        "detailSearch": detailSearch,
        "type": type_,
    }
    headers = {
        "Content-Type": "text/html; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/133.0.0.0 Safari/537.36"
        ),
    }

    response = requests.get(base_url, headers=headers, params=params)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")
    car_elements = soup.select("li.car-detail.ul-car-detail")
    cars = []

    for el in car_elements:
        # Извлекаем название автомобиля
        name_elem = el.select_one(".car-name span a")
        name = name_elem.get_text(strip=True) if name_elem else ""

        # Извлекаем ссылку на изображение
        car_img_elem = el.select_one(".car-img")
        raw_image = ""
        if car_img_elem and car_img_elem.has_attr("style"):
            style_attr = car_img_elem["style"]
            match = re.search(r"url\((.*?)\)", style_attr)
            if match:
                raw_image = match.group(1).strip("\"'")
                raw_image = html.unescape(raw_image)

        # Формируем ссылку на страницу автомобиля
        link_elem = el.find("a")
        link = ""
        if link_elem and link_elem.has_attr("href"):
            link = "https://www.arkmotors.kr" + link_elem["href"]

        # Извлекаем данные (год, пробег, тип топлива, КПП)
        car_options = el.select(".car-option li")
        year = car_options[0].get_text(strip=True) if len(car_options) > 0 else ""
        mileage = car_options[1].get_text(strip=True) if len(car_options) > 1 else ""
        fuel_type = car_options[2].get_text(strip=True) if len(car_options) > 2 else ""
        transmission = (
            car_options[3].get_text(strip=True) if len(car_options) > 3 else ""
        )

        # Извлекаем цену
        price_elem = el.select_one(".price .num")
        price = (price_elem.get_text(strip=True) + "만원") if price_elem else ""

        car = {
            "name": name,
            "image": raw_image,
            "link": link,
            "year": year,
            "mileage": mileage,
            "fuelType": fuel_type,
            "transmission": transmission,
            "price": price,
        }
        cars.append(car)

    return cars


# Эндпоинты для получения списков


@app.get("/makers")
def makers(country: str = Query(..., description="Страна, например: kor или foreign")):
    return get_maker_list(country)


@app.get("/models")
def models(maker: str = Query(..., description="ID производителя")):
    return get_model_list(maker)


@app.get("/detail-models")
def detail_models(model: str = Query(..., description="ID модели")):
    return get_detail_model_list(model)


@app.get("/grades")
def grades(
    detail_model: str = Query(
        ..., alias="detail-model", description="ID детальной модели"
    )
):
    return get_grade_list(detail_model)


@app.get("/detail-grades")
def detail_grades(grade: str = Query(..., description="ID грейда")):
    return get_detail_grade_list(grade)


# Эндпоинт для поиска автомобилей с параметрами
@app.get("/cars")
def cars(
    country: str = Query("kor", description="Страна"),
    page: int = Query(1, description="Номер страницы"),
    order: str = Query("", description="Порядок сортировки"),
    ascending: str = Query("desc", description="Направление сортировки"),
    view: str = Query("image", description="Тип представления"),
    customSelect: str = Query("24", description="Custom select"),
    carName: str = Query("", description="Название автомобиля"),
    maker: str = Query("", description="Производитель"),
    model: str = Query("", description="Модель"),
    dmodel: str = Query("", description="Детальная модель"),
    grade: str = Query("", description="Грейд"),
    dgrade: str = Query("", description="Детальный грейд"),
    price_min: str = Query("", alias="price-min", description="Минимальная цена"),
    price_max: str = Query("", alias="price-max", description="Максимальная цена"),
    year_min: str = Query("", alias="year-min", description="Минимальный год"),
    year_max: str = Query("", alias="year-max", description="Максимальный год"),
    usekm_min: str = Query("", alias="usekm-min", description="Минимальный пробег"),
    usekm_max: str = Query("", alias="usekm-max", description="Максимальный пробег"),
    fuel: str = Query("", description="Тип топлива"),
    mission: str = Query("", description="Коробка передач"),
    color: str = Query("", description="Цвет"),
    carNo: str = Query("", description="Номер автомобиля"),
    carPlateNumber: str = Query("", description="Номерной знак"),
    vehicle_model: str = Query(
        "", alias="vehicle-model", description="Модель транспортного средства"
    ),
    vehicle_dmodel: str = Query(
        "",
        alias="vehicle-dmodel",
        description="Детальная модель транспортного средства",
    ),
    vehicle_name: str = Query(
        "", alias="vehicle-name", description="Название транспортного средства"
    ),
    tab: str = Query("model", description="Вкладка"),
    detailSearch: str = Query("close", description="Детальный поиск"),
    type_: str = Query("", alias="type", description="Тип"),
):
    return fetch_cars(
        country,
        page,
        order,
        ascending,
        view,
        customSelect,
        carName,
        maker,
        model,
        dmodel,
        grade,
        dgrade,
        price_min,
        price_max,
        year_min,
        year_max,
        usekm_min,
        usekm_max,
        fuel,
        mission,
        color,
        carNo,
        carPlateNumber,
        vehicle_model,
        vehicle_dmodel,
        vehicle_name,
        tab,
        detailSearch,
        type_,
    )


@app.get("/car-details")
def car_details(carId: str = Query(..., description="ID автомобиля")):
    url = f"https://www.arkmotors.kr/search/detail/{carId}"
    headers = {
        "Content-Type": "text/html; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")
    # Получаем название автомобиля
    car_name_element = soup.select_one(".car_name p")
    carName = car_name_element.text.strip() if car_name_element else ""

    # Парсим таблицу с базовой информацией
    basic_info = soup.select_one(".info_wrap .basic-info")

    car_info = {}
    if basic_info:
        rows = basic_info.find_all("tr")
        for row in rows:
            columns = row.find_all(["th", "td"])
            if len(columns) == 4:
                key1 = columns[0].get_text(strip=True)
                value1 = columns[1].get_text(strip=True)
                key2 = columns[2].get_text(strip=True)
                value2 = columns[3].get_text(strip=True)
                car_info[key1] = value1
                car_info[key2] = value2
            elif len(columns) == 2:
                key = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                car_info[key] = value

    # Удаляем ненужное поле, если оно присутствует
    car_info.pop("사고유무", None)

    # Вытаскиываем цену автомобиля
    car_price = soup.select_one(".car_right_side .car_price")
    if car_price:
        car_price = re.sub(r"\D", "", car_price.text)
        car_price = int(car_price) * 10000

    car_info["price"] = car_price

    return {"carName": carName, "carData": car_info}


@app.get("/car-images")
def car_images(carId: str = Query(..., description="ID автомобиля")):
    url = "https://www.arkmotors.kr/search/imageList"
    payload = {"carNo": carId}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }
    response = requests.post(url, data=payload, headers=headers)
    content = response.json()
    images = [
        {"full": img.get("CarImageFullName"), "thumb": img.get("CarImageThumb")}
        for img in content.get("info", [])
    ]
    return {"images": images}
