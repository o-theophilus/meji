axis_map = {
    "island_core": {
        "label": "Island Core",
        "areas": [
            "Victoria Island", "Ikoyi", "Lekki Phase 1", "Oniru"
        ]
    },
    "island_extended": {
        "label": "Lekki Axis",
        "areas": [
            "Lekki Phase 2", "Chevron", "Agungi", "Osapa London", "Ajah"
        ]
    },
    "island_far": {
        "label": "Epe / Ibeju Axis",
        "areas": [
            "Sangotedo", "Abijo", "Awoyaya", "Lakowe", "Epe", "Ibeju Lekki"
        ]
    },
    "mainland_inner": {
        "label": "Bridge Close Mainland",
        "areas": [
            "Yaba", "Surulere", "Maryland", "Gbagada", "Ilupeju"
        ]
    },
    "mainland_mid": {
        "label": "Central Mainland",
        "areas": [
            "Ikeja", "Ogba", "Ojodu", "Ketu", "Ojota", "Oshodi", "Isolo"
        ]
    },
    "ikorodu_axis": {
        "label": "Ikorodu Axis",
        "areas": [
            "Ikorodu", "Igbogbo", "Imota"
        ]
    },
    "alimosho_axis": {
        "label": "Alimosho Axis",
        "areas": [
            "Egbeda", "Ipaja", "Ayobo", "Ikotun", "Igando", "Iyana Ipaja",
            "Command"
        ]
    },
    "badagry_axis": {
        "label": "Badagry Axis (Far West)",
        "areas": [
            "Badagry", "Ojo", "Satellite Town"
        ]
    }
}

price_map = {
    "island_core": {
        "island_core": {"price": 3000, "express": 4500},
        "island_extended": {"price": 3000, "express": 5000},
        "island_far": {"price": 4000, "express": 6000},
        "mainland_inner": {"price": 5000, "express": 7000},
        "mainland_mid": {"price": 6000, "express": 8000},
        "alimosho_axis": {"price": 7000, "express": 9000},
        "ikorodu_axis": {"price": 8000, "express": 10000},
        "badagry_axis": {"price": 9000, "express": 11000}
    },

    "island_extended": {
        "island_core": {"price": 3000, "express": 5000},
        "island_extended": {"price": 3000, "express": 4500},
        "island_far": {"price": 3000, "express": 4500},
        "mainland_inner": {"price": 4500, "express": 6500},
        "mainland_mid": {"price": 5500, "express": 7500},
        "alimosho_axis": {"price": 6500, "express": 8500},
        "ikorodu_axis": {"price": 7500, "express": 9500},
        "badagry_axis": {"price": 8500, "express": 10500}
    },

    "island_far": {
        "island_core": {"price": 4000, "express": 6000},
        "island_extended": {"price": 3000, "express": 4500},
        "island_far": {"price": 3000, "express": 4500},
        "mainland_inner": {"price": 5000, "express": 7000},
        "mainland_mid": {"price": 4500, "express": 6500},
        "alimosho_axis": {"price": 6000, "express": 8000},
        "ikorodu_axis": {"price": 7000, "express": 9000},
        "badagry_axis": {"price": 8500, "express": 10500}
    },

    "mainland_inner": {
        "island_core": {"price": 5000, "express": 7000},
        "island_extended": {"price": 4500, "express": 6500},
        "island_far": {"price": 5000, "express": 7000},
        "mainland_inner": {"price": 3000, "express": 4500},
        "mainland_mid": {"price": 3000, "express": 4500},
        "alimosho_axis": {"price": 4000, "express": 6000},
        "ikorodu_axis": {"price": 5000, "express": 7000},
        "badagry_axis": {"price": 8000, "express": 10000}
    },

    "mainland_mid": {
        "island_core": {"price": 6000, "express": 8000},
        "island_extended": {"price": 5500, "express": 7500},
        "island_far": {"price": 4500, "express": 6500},
        "mainland_inner": {"price": 3000, "express": 4500},
        "mainland_mid": {"price": 3000, "express": 4500},
        "alimosho_axis": {"price": 3500, "express": 5000},
        "ikorodu_axis": {"price": 4500, "express": 6500},
        "badagry_axis": {"price": 7500, "express": 9500}
    },

    "alimosho_axis": {
        "island_core": {"price": 7000, "express": 9000},
        "island_extended": {"price": 6500, "express": 8500},
        "island_far": {"price": 6000, "express": 8000},
        "mainland_inner": {"price": 4000, "express": 6000},
        "mainland_mid": {"price": 3500, "express": 5000},
        "alimosho_axis": {"price": 3000, "express": 4500},
        "ikorodu_axis": {"price": 5000, "express": 7000},
        "badagry_axis": {"price": 7000, "express": 9000}
    },

    "ikorodu_axis": {
        "island_core": {"price": 8000, "express": 10000},
        "island_extended": {"price": 7500, "express": 9500},
        "island_far": {"price": 7000, "express": 9000},
        "mainland_inner": {"price": 5000, "express": 7000},
        "mainland_mid": {"price": 4500, "express": 6500},
        "alimosho_axis": {"price": 5000, "express": 7000},
        "ikorodu_axis": {"price": 3000, "express": 4500},
        "badagry_axis": {"price": 6000, "express": 9000}
    },

    "badagry_axis": {
        "island_core": {"price": 9000, "express": 11000},
        "island_extended": {"price": 8500, "express": 10500},
        "island_far": {"price": 8500, "express": 10500},
        "mainland_inner": {"price": 8000, "express": 10000},
        "mainland_mid": {"price": 7500, "express": 9500},
        "alimosho_axis": {"price": 7000, "express": 9000},
        "ikorodu_axis": {"price": 6000, "express": 9000},
        "badagry_axis": {"price": 3000, "express": 4500}
    }
}


def get_areas():
    areas = [area for data in axis_map.values() for area in data["areas"]]
    return sorted(areas)


def get_axis_from_area(area):
    if not area:
        return None

    area = area.strip().lower()

    for axis, data in axis_map.items():
        for a in data["areas"]:
            if a.lower() == area:
                return axis
    return None


def get_delivery_price(items, to_area, delivery_type=None):

    pickup_areas = []
    total_weight = 0
    total_volume = 0
    for x in items:
        for _ in range(x["quantity"]):
            total_weight += x["package"].get("weight", 0)
            total_volume += (
                x["package"].get("length", 0)
                * x["package"].get("breadth", 0)
                * x["package"].get("height", 0)
            )
            area = x["package"].get("area", "igando")
            if area not in pickup_areas:
                pickup_areas.append(area)

    to_axis = get_axis_from_area(to_area)

    price = 0
    for x in pickup_areas:
        from_axis = get_axis_from_area(x)
        route = price_map[from_axis][to_axis]
        _price = route[
            "express"] if delivery_type == "express" else route["price"]
        if _price > price:
            price = _price

    volumetric_weight = total_volume / 5000
    chargeable_weight = max(total_weight, volumetric_weight)

    print("price :", price)
    print("total_weight :", total_weight)
    print("total_volume :", total_volume)
    print("volumetric_weight :", volumetric_weight)
    print("chargeable_weight :", chargeable_weight)

    if chargeable_weight > 5:
        price += (chargeable_weight - 5) * 500

    print("price :", price)

    if total_volume > 200000:
        price += 1000

    print("price :", price)
    return int(price)
