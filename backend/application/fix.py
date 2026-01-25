from flask import Blueprint, jsonify
from .postgres import db_open, db_close
# from psycopg2.extras import Json


bp = Blueprint("fix", __name__)

data = [
    {
        "date_created": "Thu, 11 Dec 2025 23:33:01 GMT",
        "files": [
            "http://127.0.0.1:5000/photo/item/e867236693c64a23a0310d6a43c70919_1120x928.jpg",
            "http://127.0.0.1:5000/photo/item/53d7aba69ef34fc3a386605db9faf9b9_500x500.jpg"
        ],
        "information": "**A timeless piece of craftsmanship, designed for the modern home.** The Heritage Oak Mantel Clock blends classic horology with clean, contemporary design. Hand-finished solid oak meets precise quartz movement, creating a functional centerpiece that warms any room with its natural elegance.\n\nPerfect for your living room mantle, home office shelf, or as a thoughtful gift, this clock is more than a timekeeper—it's a statement of refined taste.\n\n---\n\n## ✨ Key Features\n\n*   **Handcrafted Solid Oak Frame:** Each frame is cut, sanded, and finished by hand, showcasing the unique grain and warm character of sustainable oak.\n*   **Quiet High-Torque Movement:** Advanced quartz mechanism ensures accurate, reliable timekeeping with an inaudible tick—no distracting clicks or buzzes.\n*   **Crisp, Easy-Read Dial:** A matte white dial with bold, minimalist black numerals and hands offers exceptional clarity from across the room.\n*   **Protective Glass Crystal:** A beveled, clear glass cover protects the face while reducing glare and reflection.\n*   **Integrated Easy-Hang System:** A discreet, recessed hanging slot on the back allows for quick, level mounting. Also stands perfectly upright on any flat surface.\n\n---\n\n## 📐 Technical Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 30cm (W) x 20cm (H) x 5cm (D) / 11.8\" x 7.9\" x 2\" |\n| **Weight** | 1.2 kg / 2.65 lbs |\n| **Frame Material** | Solid European Oak, FSC-Certified |\n| **Finish** | Natural oak oil and protective wax |\n| **Dial & Numerals** | Matte white steel dial with printed Arabic numerals |\n| **Movement Type** | High-quality quartz (battery-operated) |\n| **Battery Required** | 1 x AA (1.5V) *Not Included* |\n| **Movement Accuracy** | ± 1 second per day |\n| **Glass** | Beveled clear acrylic crystal |\n| **Hanging Hardware** | Recessed slot for nail/hook (nail not included) |\n| **Warranty** | 2-Year Manufacturer's Warranty |\n\n---\n\n## 🏡 What's in the Box\n\n*   Heritage Oak Mantel Clock (1x)\n*   Quick-Start Care Guide (1x)\n*   Our wooden heritage and care pamphlet (1x)\n\n*Battery and hanging nail are not included.*\n\n---\n\n## ❤️ Why You'll Love It\n\n**For Your Home:** Its versatile, neutral design complements Scandinavian minimalism, rustic farmhouse, and modern industrial decor alike. The natural wood adds organic warmth to any space.\n\n**Built to Last:** Unlike mass-produced laminate or MDF pieces, this solid oak clock is an heirloom-quality item. It will age gracefully, developing a richer patina over time.\n\n**The Thoughtful Gift:** Presented in elegant, recycled packaging, it's the perfect gift for housewarmings, weddings, retirements, or anyone who appreciates craftsmanship and timeless style.\n\n**Shop with Confidence:** Backed by our 2-year warranty and 100% satisfaction guarantee. If you don't absolutely love the presence it brings to your home, we'll make it right.\n\n---\n\n**🛒 Add \"Heritage Oak Mantel Clock\" to your cart today. Measure your moments with quiet, enduring style.**\n\n*Free shipping on orders over $50. Please allow 2-3 business days for careful hand-packaging and dispatch.*",
        "name": "Heritage Oak Mantel Clock",
        "price": "134985",
        "price_old": "194985",
        "quantity": 10,
        "slug": "heritage-oak-mantel-clock-2",
        "specification": {},
        "status": "active",
        "tags": [
                "battery operated clock",
                "easy read dial",
                "fsc certified wood",
                "handcrafted clock",
                "heirloom quality",
                "heritage oak clock",
                "home decor",
                "home office decor",
                "housewarming gift",
                "living room decor",
                "mantel clock",
                "modern clock",
                "quartz clock",
                "quiet movement",
                "rustic decor",
                "scandinavian design",
                "solid oak clock",
                "wall clock",
                "wedding gift",
                "wooden frame clock"
        ],
        "variation": {
            "size": [
                "31",
                "32",
                "33",
                "34"
            ],
            "style": [
                "leather:brown",
                "suade:green"
            ]
        }
    },
    {
        "date_created": "Mon, 15 Dec 2025 14:22:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/nike_airmax_270_1.jpg"],
        "information": "**Revolutionary comfort meets iconic style.** Nike Air Max 270 delivers all-day comfort with the largest Air unit in Nike history. Engineered with breathable mesh and innovative cushioning.\n\n---\n\n## ✨ Key Features\n\n*   **Largest Nike Air Unit:** 32mm heel Air unit\n*   **Breathable Mesh Upper:** Lightweight fabric\n*   **Rubber Outsole:** Durable traction\n*   **Sock-like Fit:** Elastic collar for comfort\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight** | 310g (size 9) |\n| **Material** | Engineered mesh |\n| **Midsole** | Phylon with Air unit |\n| **Warranty** | 2-Year Warranty |",
        "name": "Nike Air Max 270",
        "price": "14999",
        "price_old": "17999",
        "quantity": 45,
        "slug": "nike-air-max-270",
        "specification": {},
        "status": "active",
        "tags": ["running shoes", "sneakers", "nike", "air max", "casual shoes"],
        "variation": {
                "size": ["7", "8", "9", "10", "11", "12"],
                "color": ["black:white", "white:black", "blue:white", "red:black"]
        }
    },
    {
        "date_created": "Wed, 17 Dec 2025 09:15:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/sony_wh1000xm5_1.jpg"],
        "information": "**Industry-leading noise cancellation meets exceptional sound.** Sony WH-1000XM5 wireless headphones feature best-in-class noise cancellation with 8 microphones for crystal-clear calls.\n\n---\n\n## ✨ Key Features\n\n*   **Best-in-class Noise Cancellation**\n*   **30-hour Battery Life**\n*   **Hi-Res Audio Support**\n*   **Multipoint Connection**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Battery Life** | Up to 30 hours |\n| **Bluetooth** | 5.2 |\n| **Weight** | 250g |\n| **Warranty** | 1-Year Warranty |",
        "name": "Sony WH-1000XM5 Headphones",
        "price": "34999",
        "price_old": "39999",
        "quantity": 28,
        "slug": "sony-wh1000xm5-headphones",
        "specification": {},
        "status": "active",
        "tags": ["noise cancelling", "wireless headphones", "bluetooth", "premium audio"],
        "variation": {
                "color": ["black", "silver", "blue"]
        }
    },
    {
        "date_created": "Tue, 16 Dec 2025 11:45:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/ergonomic_chair_1.jpg"],
        "information": "**Professional-grade comfort for extended work.** ErgoPro Executive Chair combines premium materials with advanced ergonomic design for all-day support.\n\n---\n\n## ✨ Key Features\n\n*   **12-Way Adjustability**\n*   **Breathable Mesh Back**\n*   **Memory Foam Seat**\n*   **4D Armrests**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight Capacity** | 150kg |\n| **Material** | Premium mesh |\n| **Warranty** | 5-Year Frame Warranty |",
        "name": "ErgoPro Executive Chair",
        "price": "42999",
        "price_old": "52999",
        "quantity": 15,
        "slug": "ergopro-executive-chair",
        "specification": {},
        "status": "active",
        "tags": ["ergonomic chair", "office chair", "gaming chair", "mesh chair"],
        "variation": {
                "color": ["black", "gray", "blue", "brown"]
        }
    },
    {
        "date_created": "Mon, 15 Dec 2025 16:30:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/leather_jacket_1.jpg"],
        "information": "**Timeless style meets modern craftsmanship.** Premium Lambskin Leather Jacket made from grade-A lambskin with classic motorcycle silhouette.\n\n---\n\n## ✨ Key Features\n\n*   **Grade-A Lambskin**\n*   **Hand-finished Details**\n*   **YKK Zippers**\n*   **Multiple Pockets**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | 100% Lambskin |\n| **Weight** | 1.8kg |\n| **Warranty** | 1-Year Warranty |",
        "name": "Premium Lambskin Leather Jacket",
        "price": "29999",
        "price_old": "39999",
        "quantity": 22,
        "slug": "premium-lambskin-jacket",
        "specification": {},
        "status": "active",
        "tags": ["leather jacket", "motorcycle jacket", "lambskin", "fashion"],
        "variation": {
                "size": ["S", "M", "L", "XL", "XXL"],
                "color": ["black", "brown", "cognac"]
        }
    },
    {
        "date_created": "Sun, 14 Dec 2025 13:20:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/ipad_pro_1.jpg"],
        "information": "**The ultimate iPad experience.** iPad Pro with M2 chip, Liquid Retina XDR display, and all-day battery life for creative professionals.\n\n---\n\n## ✨ Key Features\n\n*   **M2 Chip**\n*   **Liquid Retina XDR Display**\n*   **5G Capable**\n*   **Apple Pencil Hover**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Display** | 12.9\" 2732x2048 |\n| **Storage** | 128GB-2TB |\n| **Battery** | Up to 10 hours |\n| **Warranty** | 1-Year Warranty |",
        "name": "Apple iPad Pro 12.9\"",
        "price": "109999",
        "price_old": "129999",
        "quantity": 18,
        "slug": "apple-ipad-pro-12-9",
        "specification": {},
        "status": "active",
        "tags": ["ipad", "tablet", "apple", "m2 chip", "pro tablet"],
        "variation": {
                "storage": ["128gb", "256gb", "512gb", "1tb"],
                "color": ["space gray", "silver"]
        }
    },
    {
        "date_created": "Sat, 13 Dec 2025 10:10:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/kitchen_mixer_1.jpg"],
        "information": "**Professional performance for home kitchen.** KitchenMaster Stand Mixer with 1000W motor, 10-speed control, and 5.5-quart capacity.\n\n---\n\n## ✨ Key Features\n\n*   **1000W Motor**\n*   **10-Speed Control**\n*   **5.5-Quart Bowl**\n*   **10 Attachments Included**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Motor Power** | 1000W |\n| **Bowl Capacity** | 5.5 quarts |\n| **Warranty** | 5-Year Motor Warranty |",
        "name": "KitchenMaster Stand Mixer",
        "price": "39999",
        "price_old": "49999",
        "quantity": 12,
        "slug": "kitchenmaster-stand-mixer",
        "specification": {},
        "status": "active",
        "tags": ["stand mixer", "kitchen appliance", "baking", "cooking"],
        "variation": {
                "color": ["red", "black", "silver", "blue"]
        }
    },
    {
        "date_created": "Fri, 12 Dec 2025 08:45:00 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/running_shorts_1.jpg"],
        "information": "**Lightweight performance running shorts.** Ultra-breathable fabric with built-in liner for maximum comfort during workouts.\n\n---\n\n## ✨ Key Features\n\n*   **Moisture-Wicking Fabric**\n*   **Built-in Liner**\n*   **Zipper Pocket**\n*   **Reflective Details**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | 92% Polyester, 8% Spandex |\n| **Inseam** | 5 inches |\n| **Care** | Machine wash cold |",
        "name": "Performance Running Shorts",
        "price": "3499",
        "price_old": "4999",
        "quantity": 50,
        "slug": "performance-running-shorts",
        "specification": {},
        "status": "active",
        "tags": ["running shorts", "athletic wear", "workout clothes", "sports"],
        "variation": {
                "size": ["XS", "S", "M", "L", "XL"],
                "color": ["black", "navy", "gray", "red", "blue"]
        }
    },
    {
        "date_created": "Thu, 11 Dec 2025 19:30:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/gaming_monitor_1.jpg"],
        "information": "**Ultra-fast gaming monitor.** 27-inch 240Hz display with 1ms response time for competitive gaming advantage.\n\n---\n\n## ✨ Key Features\n\n*   **240Hz Refresh Rate**\n*   **1ms Response Time**\n*   **G-Sync Compatible**\n*   **HDR 400**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Size** | 27 inches |\n| **Resolution** | 2560x1440 |\n| **Refresh Rate** | 240Hz |\n| **Warranty** | 3-Year Warranty |",
        "name": "27\" Gaming Monitor",
        "price": "44999",
        "price_old": "54999",
        "quantity": 8,
        "slug": "27-gaming-monitor",
        "specification": {},
        "status": "active",
        "tags": ["gaming monitor", "240hz", "g-sync", "gaming"],
        "variation": {}
    },
    {
        "date_created": "Wed, 10 Dec 2025 15:20:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/coffee_table_1.jpg"],
        "information": "**Modern industrial coffee table.** Solid wood top with powder-coated steel frame for durable, stylish living room centerpiece.\n\n---\n\n## ✨ Key Features\n\n*   **Solid Wood Top**\n*   **Steel Frame**\n*   **Industrial Design**\n*   **Easy Assembly**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 120x60x45cm |\n| **Material** | Solid oak, Steel |\n| **Weight** | 25kg |\n| **Assembly** | Required |",
        "name": "Industrial Coffee Table",
        "price": "21999",
        "price_old": "28999",
        "quantity": 7,
        "slug": "industrial-coffee-table",
        "specification": {},
        "status": "active",
        "tags": ["coffee table", "furniture", "industrial", "living room"],
        "variation": {
                "finish": ["walnut", "oak", "black"]
        }
    },
    {
        "date_created": "Tue, 9 Dec 2025 12:10:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/smartwatch_1.jpg"],
        "information": "**Advanced health and fitness tracking.** Smartwatch with ECG, blood oxygen monitoring, and 7-day battery life.\n\n---\n\n## ✨ Key Features\n\n*   **ECG & SpO2 Monitoring**\n*   **7-Day Battery**\n*   **GPS Built-in**\n*   **Water Resistant**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Display** | 1.78\" AMOLED |\n| **Battery** | 7 days typical |\n| **Water Rating** | 5ATM |\n| **Warranty** | 2-Year Warranty |",
        "name": "Advanced Smartwatch",
        "price": "29999",
        "price_old": "35999",
        "quantity": 25,
        "slug": "advanced-smartwatch",
        "specification": {},
        "status": "active",
        "tags": ["smartwatch", "fitness tracker", "health monitoring", "wearable"],
        "variation": {
                "color": ["black", "silver", "rose gold"],
                "size": ["41mm", "45mm"]
        }
    },
    {
        "date_created": "Mon, 8 Dec 2025 14:45:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/backpack_1.jpg"],
        "information": "**Durable travel backpack.** Water-resistant fabric with laptop compartment and multiple organizational pockets.\n\n---\n\n## ✨ Key Features\n\n*   **Water-Resistant Fabric**\n*   **Laptop Compartment**\n*   **USB Charging Port**\n*   **TSA-Friendly Design**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 30L |\n| **Laptop Size** | Up to 17\" |\n| **Material** | 900D Polyester |\n| **Weight** | 1.2kg |",
        "name": "Travel Backpack Pro",
        "price": "8999",
        "price_old": "11999",
        "quantity": 35,
        "slug": "travel-backpack-pro",
        "specification": {},
        "status": "active",
        "tags": ["backpack", "travel", "laptop bag", "water resistant"],
        "variation": {
                "color": ["black", "gray", "navy", "green"]
        }
    },
    {
        "date_created": "Sun, 7 Dec 2025 10:30:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/desk_lamp_1.jpg"],
        "information": "**Adjustable LED desk lamp.** Color temperature control from warm to cool white with memory function.\n\n---\n\n## ✨ Key Features\n\n*   **Adjustable Color Temperature**\n*   **Memory Function**\n*   **Touch Controls**\n*   **USB Charging Port**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Light Source** | LED |\n| **Color Temp** | 2700K-6500K |\n| **Wattage** | 12W |\n| **Warranty** | 3-Year Warranty |",
        "name": "Adjustable LED Desk Lamp",
        "price": "5999",
        "price_old": "7999",
        "quantity": 42,
        "slug": "adjustable-led-desk-lamp",
        "specification": {},
        "status": "active",
        "tags": ["desk lamp", "led lamp", "office accessory", "adjustable"],
        "variation": {
                "color": ["white", "black", "silver"]
        }
    },
    {
        "date_created": "Sat, 6 Dec 2025 16:15:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/yoga_mat_1.jpg"],
        "information": "**Eco-friendly non-slip yoga mat.** Extra thick for joint comfort with alignment markers for proper positioning.\n\n---\n\n## ✨ Key Features\n\n*   **Non-Slip Surface**\n*   **Eco-Friendly Material**\n*   **Alignment Markers**\n*   **Extra Thick**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 183x61x0.6cm |\n| **Material** | TPE Eco-friendly |\n| **Weight** | 2.5kg |\n| **Thickness** | 6mm |",
        "name": "Premium Yoga Mat",
        "price": "3999",
        "price_old": "5499",
        "quantity": 60,
        "slug": "premium-yoga-mat",
        "specification": {},
        "status": "active",
        "tags": ["yoga mat", "fitness", "eco-friendly", "non-slip"],
        "variation": {
                "color": ["purple", "blue", "green", "gray"]
        }
    },
    {
        "date_created": "Fri, 5 Dec 2025 09:25:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/blender_1.jpg"],
        "information": "**High-performance blender.** 1500W motor with stainless steel blades for smoothies, soups, and nut butters.\n\n---\n\n## ✨ Key Features\n\n*   **1500W Motor**\n*   **Stainless Steel Blades**\n*   **Variable Speed Control**\n*   **Self-Cleaning Function**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Motor Power** | 1500W |\n| **Capacity** | 2L |\n| **Material** | BPA-Free Tritan |\n| **Warranty** | 7-Year Warranty |",
        "name": "Professional Blender",
        "price": "24999",
        "price_old": "31999",
        "quantity": 14,
        "slug": "professional-blender",
        "specification": {},
        "status": "active",
        "tags": ["blender", "kitchen appliance", "smoothie maker", "high power"],
        "variation": {
                "color": ["black", "red", "silver"]
        }
    },
    {
        "date_created": "Thu, 4 Dec 2025 13:40:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/winter_coat_1.jpg"],
        "information": "**Waterproof insulated winter coat.** Temperature rated to -20°C with detachable hood and multiple pockets.\n\n---\n\n## ✨ Key Features\n\n*   **Waterproof & Windproof**\n*   **Insulated to -20°C**\n*   **Detachable Hood**\n*   **Multiple Pockets**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | Polyester with membrane |\n| **Insulation** | 600 fill power down |\n| **Weight** | 1.5kg |\n| **Care** | Machine washable |",
        "name": "Insulated Winter Coat",
        "price": "18999",
        "price_old": "24999",
        "quantity": 20,
        "slug": "insulated-winter-coat",
        "specification": {},
        "status": "active",
        "tags": ["winter coat", "waterproof", "insulated", "cold weather"],
        "variation": {
                "size": ["S", "M", "L", "XL", "XXL"],
                "color": ["black", "navy", "red", "gray"]
        }
    },
    {
        "date_created": "Wed, 3 Dec 2025 11:15:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/bookshelf_1.jpg"],
        "information": "**Modular bookshelf system.** Expandable design with adjustable shelves to fit any space and storage needs.\n\n---\n\n## ✨ Key Features\n\n*   **Modular Design**\n*   **Adjustable Shelves**\n*   **Tool-Free Assembly**\n*   **Sturdy Construction**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 180x80x30cm |\n| **Material** | Engineered wood, Metal |\n| **Weight Capacity** | 30kg per shelf |\n| **Assembly** | Required |",
        "name": "Modular Bookshelf",
        "price": "16999",
        "price_old": "21999",
        "quantity": 9,
        "slug": "modular-bookshelf",
        "specification": {},
        "status": "active",
        "tags": ["bookshelf", "storage", "modular", "furniture"],
        "variation": {
                "color": ["white", "black", "walnut"],
                "size": ["small", "medium", "large"]
        }
    },
    {
        "date_created": "Tue, 2 Dec 2025 15:50:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/wireless_earbuds_1.jpg"],
        "information": "**True wireless earbuds with ANC.** Active noise cancellation, 8-hour battery, and wireless charging case.\n\n---\n\n## ✨ Key Features\n\n*   **Active Noise Cancellation**\n*   **8-Hour Battery**\n*   **Wireless Charging Case**\n*   **IPX4 Water Resistance**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Battery Life** | 8 hours (24 with case) |\n| **Bluetooth** | 5.3 |\n| **Water Rating** | IPX4 |\n| **Warranty** | 1-Year Warranty |",
        "name": "Wireless Earbuds Pro",
        "price": "14999",
        "price_old": "19999",
        "quantity": 38,
        "slug": "wireless-earbuds-pro",
        "specification": {},
        "status": "active",
        "tags": ["wireless earbuds", "bluetooth", "noise cancelling", "true wireless"],
        "variation": {
                "color": ["white", "black", "blue"]
        }
    },
    {
        "date_created": "Mon, 1 Dec 2025 10:25:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/office_desk_1.jpg"],
        "information": "**Height-adjustable standing desk.** Electric motor with memory presets for ergonomic workspace setup.\n\n---\n\n## ✨ Key Features\n\n*   **Electric Height Adjustment**\n*   **Memory Presets**\n*   **Anti-Collision System**\n*   **Spacious Work Surface**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 160x80cm |\n| **Height Range** | 65-130cm |\n| **Weight Capacity** | 120kg |\n| **Warranty** | 5-Year Warranty |",
        "name": "Electric Standing Desk",
        "price": "38999",
        "price_old": "48999",
        "quantity": 11,
        "slug": "electric-standing-desk",
        "specification": {},
        "status": "active",
        "tags": ["standing desk", "office furniture", "ergonomic", "height adjustable"],
        "variation": {
                "color": ["white", "black", "walnut"],
                "size": ["140cm", "160cm", "180cm"]
        }
    },
    {
        "date_created": "Sun, 30 Nov 2025 14:35:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/running_shoes_1.jpg"],
        "information": "**Lightweight running shoes.** Responsive cushioning with breathable upper for daily training and long runs.\n\n---\n\n## ✨ Key Features\n\n*   **Responsive Cushioning**\n*   **Breathable Upper**\n*   **Carbon Rubber Outsole**\n*   **Reflective Details**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight** | 250g (size 9) |\n| **Drop** | 8mm |\n| **Material** | Engineered mesh |\n| **Best For** | Road running |",
        "name": "Daily Trainer Running Shoes",
        "price": "12999",
        "price_old": "15999",
        "quantity": 55,
        "slug": "daily-trainer-running-shoes",
        "specification": {},
        "status": "active",
        "tags": ["running shoes", "athletic shoes", "road running", "training"],
        "variation": {
                "size": ["7", "8", "9", "10", "11", "12"],
                "color": ["black:yellow", "white:blue", "gray:orange"]
        }
    },
    {
        "date_created": "Sat, 29 Nov 2025 09:45:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/air_purifier_1.jpg"],
        "information": "**HEPA air purifier.** Covers up to 50m² with smart sensors and quiet operation for better indoor air quality.\n\n---\n\n## ✨ Key Features\n\n*   **True HEPA Filter**\n*   **Smart Air Quality Sensor**\n*   **Quiet Operation**\n*   **Auto Mode**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Coverage** | Up to 50m² |\n| **Filters** | Pre-filter, HEPA, Carbon |\n| **Noise Level** | 25-55 dB |\n| **Warranty** | 2-Year Warranty |",
        "name": "HEPA Air Purifier",
        "price": "21999",
        "price_old": "28999",
        "quantity": 16,
        "slug": "hepa-air-purifier",
        "specification": {},
        "status": "active",
        "tags": ["air purifier", "hepa", "air quality", "home appliance"],
        "variation": {
                "color": ["white", "black"]
        }
    },
    {
        "date_created": "Fri, 28 Nov 2025 17:20:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/kitchen_knife_1.jpg"],
        "information": "**Professional chef's knife.** German steel with ergonomic handle for precision cutting and durability.\n\n---\n\n## ✨ Key Features\n\n*   **German Stainless Steel**\n*   **Full Tang Construction**\n*   **Ergonomic Handle**\n*   **Laser-Cut Edge**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Blade Length** | 20cm |\n| **Material** | X50CrMoV15 Steel |\n| **Handle** | POM Polymer |\n| **Care** | Hand wash only |",
        "name": "Professional Chef's Knife",
        "price": "8999",
        "price_old": "12999",
        "quantity": 30,
        "slug": "professional-chef-knife",
        "specification": {},
        "status": "active",
        "tags": ["chef knife", "kitchen knife", "cutlery", "cooking tools"],
        "variation": {}
    },
    {
        "date_created": "Thu, 27 Nov 2025 12:10:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/gaming_chair_1.jpg"],
        "information": "**Ergonomic gaming chair.** Lumbar support, adjustable armrests, and premium PU leather for long gaming sessions.\n\n---\n\n## ✨ Key Features\n\n*   **Lumbar & Neck Support**\n*   **4D Armrests**\n*   **Recline to 180°**\n*   **Premium PU Leather**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight Capacity** | 150kg |\n| **Recline** | 90-180 degrees |\n| **Material** | PU Leather |\n| **Warranty** | 3-Year Warranty |",
        "name": "Premium Gaming Chair",
        "price": "32999",
        "price_old": "41999",
        "quantity": 13,
        "slug": "premium-gaming-chair",
        "specification": {},
        "status": "active",
        "tags": ["gaming chair", "ergonomic chair", "gaming setup", "office chair"],
        "variation": {
                "color": ["black:red", "black:blue", "white:pink", "all black"]
        }
    },
    {
        "date_created": "Wed, 26 Nov 2025 15:30:25 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/smart_scale_1.jpg"],
        "information": "**Smart body composition scale.** Measures weight, body fat, muscle mass, and syncs with fitness apps.\n\n---\n\n## ✨ Key Features\n\n*   **13 Body Measurements**\n*   **App Connectivity**\n*   **Unlimited User Profiles**\n*   **Auto Recognition**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight Capacity** | 180kg |\n| **Measurements** | 13 metrics |\n| **Connectivity** | Bluetooth, WiFi |\n| **Battery** | AAA x 4 (included) |",
        "name": "Smart Body Composition Scale",
        "price": "6999",
        "price_old": "9999",
        "quantity": 28,
        "slug": "smart-body-scale",
        "specification": {},
        "status": "active",
        "tags": ["smart scale", "body composition", "fitness tracker", "health"],
        "variation": {
                "color": ["black", "white", "glass"]
        }
    },
    {
        "date_created": "Tue, 25 Nov 2025 11:45:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/camping_tent_1.jpg"],
        "information": "**4-person camping tent.** Waterproof with aluminum poles, easy setup in 10 minutes, and excellent ventilation.\n\n---\n\n## ✨ Key Features\n\n*   **Waterproof 3000mm**\n*   **Aluminum Poles**\n*   **Easy 10-Minute Setup**\n*   **Ventilation System**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 4 persons |\n| **Weight** | 5.5kg |\n| **Waterproof** | 3000mm |\n| **Pack Size** | 60x20cm |",
        "name": "4-Person Camping Tent",
        "price": "14999",
        "price_old": "19999",
        "quantity": 18,
        "slug": "4-person-camping-tent",
        "specification": {},
        "status": "active",
        "tags": ["camping tent", "outdoor gear", "waterproof", "4 person"],
        "variation": {
                "color": ["green", "blue", "gray"]
        }
    },
    {
        "date_created": "Mon, 24 Nov 2025 14:20:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/mechanical_keyboard_1.jpg"],
        "information": "**Mechanical gaming keyboard.** Cherry MX switches, RGB backlighting, and aluminum frame for durability.\n\n---\n\n## ✨ Key Features\n\n*   **Cherry MX Switches**\n*   **RGB Backlighting**\n*   **Aluminum Frame**\n*   **N-Key Rollover**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Switch Type** | Cherry MX Red |\n| **Backlight** | 16.8M Color RGB |\n| **Material** | Aluminum |\n| **Warranty** | 2-Year Warranty |",
        "name": "Mechanical Gaming Keyboard",
        "price": "12999",
        "price_old": "16999",
        "quantity": 22,
        "slug": "mechanical-gaming-keyboard",
        "specification": {},
        "status": "active",
        "tags": ["mechanical keyboard", "gaming keyboard", "rgb", "cherry mx"],
        "variation": {
                "switch": ["red", "blue", "brown"],
                "color": ["black", "white"]
        }
    },
    {
        "date_created": "Sun, 23 Nov 2025 10:15:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/fitness_band_1.jpg"],
        "information": "**Advanced fitness tracker.** Heart rate monitoring, sleep tracking, and 14-day battery life for active lifestyles.\n\n---\n\n## ✨ Key Features\n\n*   **24/7 Heart Rate**\n*   **Sleep Tracking**\n*   **14-Day Battery**\n*   **Water Resistant**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Display** | 1.1\" AMOLED |\n| **Battery** | 14 days |\n| **Water Rating** | 5ATM |\n| **Warranty** | 1-Year Warranty |",
        "name": "Fitness Tracker Pro",
        "price": "7999",
        "price_old": "10999",
        "quantity": 40,
        "slug": "fitness-tracker-pro",
        "specification": {},
        "status": "active",
        "tags": ["fitness tracker", "heart rate monitor", "activity tracker", "wearable"],
        "variation": {
                "color": ["black", "pink", "blue", "green"],
                "size": ["small", "large"]
        }
    },
    {
        "date_created": "Sat, 22 Nov 2025 16:40:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/cast_iron_pan_1.jpg"],
        "information": "**Pre-seasoned cast iron skillet.** Even heat distribution, oven safe to 260°C, perfect for searing and baking.\n\n---\n\n## ✨ Key Features\n\n*   **Pre-Seasoned**\n*   **Even Heat Distribution**\n*   **Oven Safe to 260°C**\n*   **Durable Construction**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Diameter** | 30cm |\n| **Material** | Cast Iron |\n| **Weight** | 3.2kg |\n| **Oven Safe** | Up to 260°C |",
        "name": "Cast Iron Skillet",
        "price": "5999",
        "price_old": "8999",
        "quantity": 25,
        "slug": "cast-iron-skillet",
        "specification": {},
        "status": "active",
        "tags": ["cast iron", "skillet", "cookware", "kitchen"],
        "variation": {
                "size": ["25cm", "30cm", "35cm"]
        }
    },
    {
        "date_created": "Fri, 21 Nov 2025 13:25:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/bluetooth_speaker_1.jpg"],
        "information": "**Portable Bluetooth speaker.** 360° sound, IPX7 waterproof, and 12-hour battery for outdoor adventures.\n\n---\n\n## ✨ Key Features\n\n*   **360° Sound**\n*   **IPX7 Waterproof**\n*   **12-Hour Battery**\n*   **Built-in Microphone**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Battery Life** | 12 hours |\n| **Waterproof** | IPX7 |\n| **Bluetooth** | 5.3 |\n| **Weight** | 0.9kg |",
        "name": "Portable Bluetooth Speaker",
        "price": "8999",
        "price_old": "12999",
        "quantity": 32,
        "slug": "portable-bluetooth-speaker",
        "specification": {},
        "status": "active",
        "tags": ["bluetooth speaker", "portable speaker", "waterproof", "outdoor"],
        "variation": {
                "color": ["black", "blue", "red", "gray"]
        }
    },
    {
        "date_created": "Thu, 20 Nov 2025 09:50:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/dumbbell_set_1.jpg"],
        "information": "**Adjustable dumbbell set.** Quick-change weight system from 5kg to 25kg per dumbbell for home workouts.\n\n---\n\n## ✨ Key Features\n\n*   **Adjustable 5-25kg**\n*   **Quick-Change System**\n*   **Compact Storage**\n*   **Non-Slip Grip**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Weight Range** | 5-25kg each |\n| **Material** | Steel, Plastic |\n| **Set Includes** | 2 dumbbells, Stand |\n| **Warranty** | 2-Year Warranty |",
        "name": "Adjustable Dumbbell Set",
        "price": "19999",
        "price_old": "25999",
        "quantity": 12,
        "slug": "adjustable-dumbbell-set",
        "specification": {},
        "status": "active",
        "tags": ["dumbbells", "home gym", "fitness equipment", "weights"],
        "variation": {}
    },
    {
        "date_created": "Wed, 19 Nov 2025 17:10:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/office_supplies_1.jpg"],
        "information": "**Ergonomic mouse and keyboard set.** Wireless connectivity, quiet keys, and comfortable design for office use.\n\n---\n\n## ✨ Key Features\n\n*   **Wireless 2.4GHz**\n*   **Quiet Keys**\n*   **Ergonomic Design**\n*   **Long Battery Life**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Connection** | Wireless 2.4GHz |\n| **Battery** | 2xAA each |\n| **Range** | 10m |\n| **Warranty** | 1-Year Warranty |",
        "name": "Wireless Keyboard & Mouse Set",
        "price": "4999",
        "price_old": "6999",
        "quantity": 45,
        "slug": "wireless-keyboard-mouse-set",
        "specification": {},
        "status": "active",
        "tags": ["keyboard", "mouse", "wireless", "office supplies"],
        "variation": {
                "color": ["black", "white", "silver"]
        }
    },
    {
        "date_created": "Tue, 18 Nov 2025 12:35:25 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/bedding_set_1.jpg"],
        "information": "**Luxury cotton bedding set.** 100% Egyptian cotton, 800 thread count for ultimate comfort and durability.\n\n---\n\n## ✨ Key Features\n\n*   **100% Egyptian Cotton**\n*   **800 Thread Count**\n*   **Breathable & Soft**\n*   **Hypoallergenic**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | 100% Egyptian Cotton |\n| **Thread Count** | 800 |\n| **Set Includes** | Duvet cover, 2 pillowcases |\n| **Care** | Machine washable |",
        "name": "Egyptian Cotton Bedding Set",
        "price": "12999",
        "price_old": "17999",
        "quantity": 24,
        "slug": "egyptian-cotton-bedding",
        "specification": {},
        "status": "active",
        "tags": ["bedding", "sheets", "egyptian cotton", "luxury"],
        "variation": {
                "size": ["single", "double", "king", "super king"],
                "color": ["white", "cream", "gray", "blue"]
        }
    },
    {
        "date_created": "Mon, 17 Nov 2025 15:45:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/smart_lightbulb_1.jpg"],
        "information": "**Smart LED light bulbs.** App-controlled, color changing, compatible with voice assistants for smart home setup.\n\n---\n\n## ✨ Key Features\n\n*   **App & Voice Control**\n*   **16 Million Colors**\n*   **Energy Efficient**\n*   **Scheduling**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Wattage** | 9W (60W equivalent) |\n| **Lumens** | 800lm |\n| **Connectivity** | WiFi |\n| **Compatibility** | Alexa, Google Home |",
        "name": "Smart LED Light Bulbs (4-Pack)",
        "price": "3999",
        "price_old": "5999",
        "quantity": 50,
        "slug": "smart-led-light-bulbs",
        "specification": {},
        "status": "active",
        "tags": ["smart bulbs", "led lights", "smart home", "color changing"],
        "variation": {
                "type": ["color", "white", "ambiance"]
        }
    },
    {
        "date_created": "Sun, 16 Nov 2025 11:20:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/hiking_boots_1.jpg"],
        "information": "**Waterproof hiking boots.** Gore-Tex membrane, Vibram outsole for traction, and ankle support for rough terrain.\n\n---\n\n## ✨ Key Features\n\n*   **Gore-Tex Waterproof**\n*   **Vibram Outsole**\n*   **Ankle Support**\n*   **Breathable**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Waterproof** | Gore-Tex |\n| **Outsole** | Vibram |\n| **Weight** | 450g each |\n| **Best For** | Hiking, Trekking |",
        "name": "Waterproof Hiking Boots",
        "price": "15999",
        "price_old": "20999",
        "quantity": 20,
        "slug": "waterproof-hiking-boots",
        "specification": {},
        "status": "active",
        "tags": ["hiking boots", "waterproof", "outdoor shoes", "trekking"],
        "variation": {
                "size": ["7", "8", "9", "10", "11", "12"],
                "color": ["brown", "black", "green"]
        }
    },
    {
        "date_created": "Sat, 15 Nov 2025 14:55:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/rice_cooker_1.jpg"],
        "information": "**Multi-functional rice cooker.** Fuzzy logic technology, 10 cooking programs, and keep-warm function.\n\n---\n\n## ✨ Key Features\n\n*   **Fuzzy Logic Technology**\n*   **10 Cooking Programs**\n*   **Keep-Warm Function**\n*   **Non-Stick Bowl**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 1.8L (10 cups) |\n| **Power** | 700W |\n| **Programs** | 10 |\n| **Warranty** | 2-Year Warranty |",
        "name": "Multi-Functional Rice Cooker",
        "price": "8999",
        "price_old": "12999",
        "quantity": 30,
        "slug": "multi-functional-rice-cooker",
        "specification": {},
        "status": "active",
        "tags": ["rice cooker", "kitchen appliance", "cooking", "fuzzy logic"],
        "variation": {
                "color": ["white", "black", "silver"]
        }
    },
    {
        "date_created": "Fri, 14 Nov 2025 10:40:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/sunglasses_1.jpg"],
        "information": "**Polarized sunglasses.** UV400 protection, polarized lenses reduce glare, and lightweight frame for comfort.\n\n---\n\n## ✨ Key Features\n\n*   **Polarized Lenses**\n*   **UV400 Protection**\n*   **Lightweight Frame**\n*   **Scratch Resistant**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Lens Type** | Polarized |\n| **UV Protection** | 100% UV400 |\n| **Frame Material** | TR90 |\n| **Includes** | Case, Cloth |",
        "name": "Polarized Sunglasses",
        "price": "2999",
        "price_old": "4999",
        "quantity": 60,
        "slug": "polarized-sunglasses",
        "specification": {},
        "status": "active",
        "tags": ["sunglasses", "polarized", "uv protection", "accessories"],
        "variation": {
                "color": ["black", "tortoise", "blue", "gray"],
                "lens": ["gray", "brown", "green"]
        }
    },
    {
        "date_created": "Thu, 13 Nov 2025 16:25:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/desktop_pc_1.jpg"],
        "information": "**Gaming desktop PC.** RTX 4070, Intel i7, 32GB RAM, and 1TB SSD for high-performance gaming and work.\n\n---\n\n## ✨ Key Features\n\n*   **RTX 4070 Graphics**\n*   **Intel i7 Processor**\n*   **32GB RAM**\n*   **1TB SSD**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **CPU** | Intel i7-13700K |\n| **GPU** | NVIDIA RTX 4070 12GB |\n| **RAM** | 32GB DDR5 |\n| **Warranty** | 3-Year Warranty |",
        "name": "Gaming Desktop PC",
        "price": "189999",
        "price_old": "229999",
        "quantity": 6,
        "slug": "gaming-desktop-pc",
        "specification": {},
        "status": "active",
        "tags": ["gaming pc", "desktop computer", "rtx 4070", "gaming"],
        "variation": {
                "storage": ["1tb", "2tb"],
                "ram": ["32gb", "64gb"]
        }
    },
    {
        "date_created": "Wed, 12 Nov 2025 13:15:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/yoga_pants_1.jpg"],
        "information": "**High-waisted yoga pants.** Four-way stretch fabric, moisture-wicking, and squat-proof for confidence during workouts.\n\n---\n\n## ✨ Key Features\n\n*   **Four-Way Stretch**\n*   **Moisture-Wicking**\n*   **High-Waisted**\n*   **Squat-Proof**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | 88% Nylon, 12% Spandex |\n| **Length** | 7/8 (ankle length) |\n| **Care** | Machine wash cold |\n| **Features** | Phone pocket |",
        "name": "High-Waisted Yoga Pants",
        "price": "4999",
        "price_old": "6999",
        "quantity": 55,
        "slug": "high-waisted-yoga-pants",
        "specification": {},
        "status": "active",
        "tags": ["yoga pants", "leggings", "workout clothes", "athletic wear"],
        "variation": {
                "size": ["XS", "S", "M", "L", "XL"],
                "color": ["black", "gray", "navy", "burgundy", "green"]
        }
    },
    {
        "date_created": "Tue, 11 Nov 2025 09:30:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/electric_scooter_1.jpg"],
        "information": "**Foldable electric scooter.** 25km range, 25km/h top speed, and portable design for urban commuting.\n\n---\n\n## ✨ Key Features\n\n*   **25km Range**\n*   **25km/h Top Speed**\n*   **Foldable Design**\n*   **App Connectivity**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Range** | 25km |\n| **Max Speed** | 25km/h |\n| **Weight** | 15kg |\n| **Charge Time** | 4 hours |",
        "name": "Foldable Electric Scooter",
        "price": "59999",
        "price_old": "79999",
        "quantity": 9,
        "slug": "foldable-electric-scooter",
        "specification": {},
        "status": "active",
        "tags": ["electric scooter", "commuter", "foldable", "eco transport"],
        "variation": {
                "color": ["black", "white", "red"]
        }
    },
    {
        "date_created": "Mon, 10 Nov 2025 17:45:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/desk_organizer_1.jpg"],
        "information": "**Minimalist desk organizer.** Bamboo construction with compartments for pens, phone, and notebooks.\n\n---\n\n## ✨ Key Features\n\n*   **Bamboo Construction**\n*   **Multiple Compartments**\n*   **Minimalist Design**\n*   **Natural Finish**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Dimensions** | 30x20x10cm |\n| **Material** | Solid bamboo |\n| **Weight** | 0.8kg |\n| **Finish** | Natural oil |",
        "name": "Bamboo Desk Organizer",
        "price": "2999",
        "price_old": "4499",
        "quantity": 40,
        "slug": "bamboo-desk-organizer",
        "specification": {},
        "status": "active",
        "tags": ["desk organizer", "bamboo", "office accessory", "storage"],
        "variation": {
                "style": ["with drawer", "without drawer"]
        }
    },
    {
        "date_created": "Sun, 9 Nov 2025 12:20:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/security_camera_1.jpg"],
        "information": "**Wireless security camera.** 2K resolution, night vision, two-way audio, and cloud storage options.\n\n---\n\n## ✨ Key Features\n\n*   **2K Resolution**\n*   **Color Night Vision**\n*   **Two-Way Audio**\n*   **Motion Detection**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Resolution** | 2K (2560x1440) |\n| **Field of View** | 130° |\n| **Connectivity** | WiFi |\n| **Power** | Battery or wired |",
        "name": "Wireless Security Camera",
        "price": "8999",
        "price_old": "12999",
        "quantity": 25,
        "slug": "wireless-security-camera",
        "specification": {},
        "status": "active",
        "tags": ["security camera", "home security", "wireless", "surveillance"],
        "variation": {
                "type": ["battery", "wired"],
                "color": ["white", "black"]
        }
    },
    {
        "date_created": "Sat, 8 Nov 2025 15:10:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/hand_mixer_1.jpg"],
        "information": "**Powerful hand mixer.** 5-speed control, includes beaters, dough hooks, and whisk for versatile kitchen tasks.\n\n---\n\n## ✨ Key Features\n\n*   **5-Speed Control**\n*   **Includes 5 Attachments**\n*   **Compact Storage**\n*   **Easy-Clean Design**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Power** | 250W |\n| **Speeds** | 5 + turbo |\n| **Attachments** | 5 pieces |\n| **Warranty** | 2-Year Warranty |",
        "name": "5-Speed Hand Mixer",
        "price": "3999",
        "price_old": "5999",
        "quantity": 35,
        "slug": "5-speed-hand-mixer",
        "specification": {},
        "status": "active",
        "tags": ["hand mixer", "kitchen appliance", "baking tools", "mixing"],
        "variation": {
                "color": ["red", "white", "black"]
        }
    },
    {
        "date_created": "Fri, 7 Nov 2025 10:55:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/board_game_1.jpg"],
        "information": "**Strategy board game for adults.** 2-4 players, 60-90 minute playtime, and high-quality components.\n\n---\n\n## ✨ Key Features\n\n*   **2-4 Players**\n*   **60-90 Minute Playtime**\n*   **Strategy Focused**\n*   **High-Quality Components**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Players** | 2-4 |\n| **Age** | 14+ |\n| **Playtime** | 60-90 minutes |\n| **Components** | Board, cards, pieces |",
        "name": "Strategy Board Game",
        "price": "4999",
        "price_old": "6999",
        "quantity": 30,
        "slug": "strategy-board-game",
        "specification": {},
        "status": "active",
        "tags": ["board game", "strategy game", "family game", "tabletop"],
        "variation": {}
    },
    {
        "date_created": "Thu, 6 Nov 2025 14:40:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/water_bottle_1.jpg"],
        "information": "**Insulated stainless steel bottle.** Keeps drinks cold 24 hours, hot 12 hours, and leak-proof design.\n\n---\n\n## ✨ Key Features\n\n*   **24-Hour Cold Retention**\n*   **12-Hour Hot Retention**\n*   **Leak-Proof Lid**\n*   **BPA-Free**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 1L |\n| **Material** | 18/8 Stainless Steel |\n| **Insulation** | Double-wall vacuum |\n| **Weight** | 0.4kg |",
        "name": "Insulated Water Bottle",
        "price": "2999",
        "price_old": "4499",
        "quantity": 65,
        "slug": "insulated-water-bottle",
        "specification": {},
        "status": "active",
        "tags": ["water bottle", "insulated", "stainless steel", "hydration"],
        "variation": {
                "size": ["500ml", "750ml", "1L"],
                "color": ["black", "white", "blue", "green", "pink"]
        }
    },
    {
        "date_created": "Wed, 5 Nov 2025 11:25:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/laundry_basket_1.jpg"],
        "information": "**Collapsible laundry basket.** Foldable design for space-saving storage, sturdy handles, and breathable fabric.\n\n---\n\n## ✨ Key Features\n\n*   **Collapsible Design**\n*   **Sturdy Handles**\n*   **Breathable Fabric**\n*   **Easy to Clean**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 60L |\n| **Material** | Polyester, Steel frame |\n| **Collapsed Height** | 8cm |\n| **Weight** | 1.2kg |",
        "name": "Collapsible Laundry Basket",
        "price": "1999",
        "price_old": "2999",
        "quantity": 50,
        "slug": "collapsible-laundry-basket",
        "specification": {},
        "status": "active",
        "tags": ["laundry basket", "storage", "collapsible", "home organization"],
        "variation": {
                "color": ["gray", "white", "blue", "beige"]
        }
    },
    {
        "date_created": "Tue, 4 Nov 2025 16:15:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/gaming_mouse_1.jpg"],
        "information": "**Wireless gaming mouse.** 16000 DPI, 70-hour battery, lightweight design for competitive gaming.\n\n---\n\n## ✨ Key Features\n\n*   **16000 DPI Sensor**\n*   **70-Hour Battery**\n*   **Lightweight (69g)**\n*   **6 Programmable Buttons**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Sensor** | Optical 16000 DPI |\n| **Battery** | 70 hours |\n| **Weight** | 69g |\n| **Warranty** | 2-Year Warranty |",
        "name": "Wireless Gaming Mouse",
        "price": "7999",
        "price_old": "10999",
        "quantity": 28,
        "slug": "wireless-gaming-mouse",
        "specification": {},
        "status": "active",
        "tags": ["gaming mouse", "wireless mouse", "gaming accessory", "mouse"],
        "variation": {
                "color": ["black", "white", "pink"],
                "connectivity": ["wireless", "wired"]
        }
    },
    {
        "date_created": "Mon, 3 Nov 2025 13:30:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/plant_stand_1.jpg"],
        "information": "**Tiered plant stand.** Indoor/outdoor use, holds 5 plants, made from weather-resistant materials.\n\n---\n\n## ✨ Key Features\n\n*   **Holds 5 Plants**\n*   **Indoor/Outdoor Use**\n*   **Weather Resistant**\n*   **Easy Assembly**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Height** | 120cm |\n| **Material** | Steel, Wood |\n| **Weight Capacity** | 15kg total |\n| **Assembly** | Required |",
        "name": "Tiered Plant Stand",
        "price": "6999",
        "price_old": "9999",
        "quantity": 22,
        "slug": "tiered-plant-stand",
        "specification": {},
        "status": "active",
        "tags": ["plant stand", "indoor plants", "home decor", "gardening"],
        "variation": {
                "color": ["black", "white", "wood finish"]
        }
    },
    {
        "date_created": "Sun, 2 Nov 2025 10:45:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/power_bank_1.jpg"],
        "information": "**High-capacity power bank.** 26800mAh with 65W fast charging for laptops, phones, and tablets.\n\n---\n\n## ✨ Key Features\n\n*   **26800mAh Capacity**\n*   **65W Fast Charging**\n*   **3 Output Ports**\n*   **LCD Display**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 26800mAh |\n| **Output** | 65W Max |\n| **Ports** | 2x USB-C, 1x USB-A |\n| **Weight** | 0.5kg |",
        "name": "26800mAh Power Bank",
        "price": "5999",
        "price_old": "8999",
        "quantity": 45,
        "slug": "26800mah-power-bank",
        "specification": {},
        "status": "active",
        "tags": ["power bank", "portable charger", "fast charging", "battery"],
        "variation": {
                "color": ["black", "white", "blue"]
        }
    },
    {
        "date_created": "Sat, 1 Nov 2025 17:20:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/cooking_utensils_1.jpg"],
        "information": "**Silicone cooking utensil set.** Heat resistant to 260°C, non-scratch, and dishwasher safe for easy cleaning.\n\n---\n\n## ✨ Key Features\n\n*   **Heat Resistant to 260°C**\n*   **Non-Scratch**\n*   **Dishwasher Safe**\n*   **BPA-Free Silicone**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Set Includes** | 5 utensils |\n| **Material** | Food-grade silicone |\n| **Max Temperature** | 260°C |\n| **Care** | Dishwasher safe |",
        "name": "Silicone Cooking Utensil Set",
        "price": "2999",
        "price_old": "4499",
        "quantity": 60,
        "slug": "silicone-cooking-utensils",
        "specification": {},
        "status": "active",
        "tags": ["cooking utensils", "silicone", "kitchen tools", "non-scratch"],
        "variation": {
                "color": ["gray", "black", "multicolor"]
        }
    },
    {
        "date_created": "Fri, 31 Oct 2025 12:35:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/foot_massager_1.jpg"],
        "information": "**Electric foot massager.** Shiatsu massage with heat function for relaxation and pain relief.\n\n---\n\n## ✨ Key Features\n\n*   **Shiatsu Massage**\n*   **Heat Function**\n*   **Adjustable Intensity**\n*   **Remote Control**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Modes** | 3 massage modes |\n| **Heat** | Adjustable |\n| **Timer** | 15-minute auto-off |\n| **Warranty** | 1-Year Warranty |",
        "name": "Electric Foot Massager",
        "price": "8999",
        "price_old": "12999",
        "quantity": 18,
        "slug": "electric-foot-massager",
        "specification": {},
        "status": "active",
        "tags": ["foot massager", "massage", "relaxation", "shiatsu"],
        "variation": {
                "color": ["black", "beige"]
        }
    },
    {
        "date_created": "Thu, 30 Oct 2025 15:50:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/hammock_1.jpg"],
        "information": "**Portable camping hammock.** Includes straps, supports up to 200kg, and packs into small carrying bag.\n\n---\n\n## ✨ Key Features\n\n*   **Includes Straps**\n*   **200kg Capacity**\n*   **Compact & Lightweight**\n*   **Quick Setup**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 200kg |\n| **Weight** | 0.6kg |\n| **Material** | Nylon |\n| **Pack Size** | 15x10cm |",
        "name": "Portable Camping Hammock",
        "price": "3999",
        "price_old": "5999",
        "quantity": 35,
        "slug": "portable-camping-hammock",
        "specification": {},
        "status": "active",
        "tags": ["hammock", "camping", "outdoor", "portable"],
        "variation": {
                "color": ["blue", "green", "gray", "camouflage"]
        }
    },
    {
        "date_created": "Wed, 29 Oct 2025 11:25:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/coffee_maker_1.jpg"],
        "information": "**Programmable coffee maker.** 12-cup capacity, programmable timer, and pause & serve feature.\n\n---\n\n## ✨ Key Features\n\n*   **12-Cup Capacity**\n*   **Programmable Timer**\n*   **Pause & Serve**\n*   **Auto Shut-Off**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 1.8L (12 cups) |\n| **Power** | 900W |\n| **Features** | Programmable, Filter |\n| **Warranty** | 2-Year Warranty |",
        "name": "Programmable Coffee Maker",
        "price": "6999",
        "price_old": "9999",
        "quantity": 28,
        "slug": "programmable-coffee-maker",
        "specification": {},
        "status": "active",
        "tags": ["coffee maker", "coffee machine", "programmable", "kitchen"],
        "variation": {
                "color": ["black", "stainless steel", "white"]
        }
    },
    {
        "date_created": "Tue, 28 Oct 2025 14:40:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/office_supplies_set_1.jpg"],
        "information": "**Desk organizer set.** Includes pen holder, document tray, and phone stand in matching minimalist design.\n\n---\n\n## ✨ Key Features\n\n*   **3-Piece Set**\n*   **Minimalist Design**\n*   **Non-Slip Base**\n*   **Easy Assembly**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Set Includes** | 3 pieces |\n| **Material** | ABS Plastic |\n| **Dimensions** | Various sizes |\n| **Weight** | 1kg total |",
        "name": "Desk Organizer Set",
        "price": "2499",
        "price_old": "3999",
        "quantity": 50,
        "slug": "desk-organizer-set",
        "specification": {},
        "status": "active",
        "tags": ["desk organizer", "office supplies", "storage", "minimalist"],
        "variation": {
                "color": ["white", "black", "gray", "wood grain"]
        }
    },
    {
        "date_created": "Mon, 27 Oct 2025 09:55:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/ice_maker_1.jpg"],
        "information": "**Portable ice maker.** Produces 12kg ice per day, 2 ice sizes, and automatic shutdown when full.\n\n---\n\n## ✨ Key Features\n\n*   **12kg Ice Per Day**\n*   **2 Ice Sizes**\n*   **Auto Shut-Off**\n*   **Portable Design**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Ice Production** | 12kg/24h |\n| **Ice Size** | Small/Large |\n| **Water Tank** | 2L |\n| **Warranty** | 1-Year Warranty |",
        "name": "Portable Ice Maker",
        "price": "12999",
        "price_old": "16999",
        "quantity": 15,
        "slug": "portable-ice-maker",
        "specification": {},
        "status": "active",
        "tags": ["ice maker", "portable", "appliance", "kitchen"],
        "variation": {
                "color": ["black", "silver"]
        }
    },
    {
        "date_created": "Sun, 26 Oct 2025 17:30:25 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/face_cream_1.jpg",
                  "http://127.0.0.1:5000/photo/item/face_cream_2.jpg"],
        "information": "**Anti-aging face cream.** With hyaluronic acid and vitamin C for hydration and brightening, suitable for all skin types.\n\n---\n\n## ✨ Key Features\n\n*   **Hyaluronic Acid**\n*   **Vitamin C**\n*   **Non-Comedogenic**\n*   **Cruelty-Free**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Volume** | 50ml |\n| **Skin Type** | All types |\n| **Key Ingredients** | HA, Vit C |\n| **Made In** | South Korea |",
        "name": "Anti-Aging Face Cream",
        "price": "4999",
        "price_old": "6999",
        "quantity": 80,
        "slug": "anti-aging-face-cream",
        "specification": {},
        "status": "active",
        "tags": ["face cream", "skincare", "anti-aging", "hyaluronic acid"],
        "variation": {
                "size": ["30ml", "50ml", "100ml"]
        }
    },
    {
        "date_created": "Sat, 25 Oct 2025 13:45:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/puzzle_1.jpg"],
        "information": "**1000-piece jigsaw puzzle.** Premium quality pieces, vibrant artwork, and includes reference poster.\n\n---\n\n## ✨ Key Features\n\n*   **1000 Pieces**\n*   **Premium Quality**\n*   **Includes Reference Poster**\n*   **Vibrant Artwork**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Pieces** | 1000 |\n| **Finished Size** | 68x49cm |\n| **Material** | Recycled cardboard |\n| **Age** | 12+ |",
        "name": "1000-Piece Jigsaw Puzzle",
        "price": "1999",
        "price_old": "2999",
        "quantity": 42,
        "slug": "1000-piece-jigsaw-puzzle",
        "specification": {},
        "status": "active",
        "tags": ["jigsaw puzzle", "1000 pieces", "games", "entertainment"],
        "variation": {
                "design": ["landscape", "cityscape", "animals", "art"]
        }
    },
    {
        "date_created": "Fri, 24 Oct 2025 10:20:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/salad_spinner_1.jpg"],
        "information": "**Large capacity salad spinner.** Push-button operation, non-slip base, and easy-to-clean design.\n\n---\n\n## ✨ Key Features\n\n*   **Push-Button Operation**\n*   **Non-Slip Base**\n*   **Large Capacity**\n*   **Dishwasher Safe**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 5L |\n| **Material** | BPA-Free Plastic |\n| **Operation** | Push-button |\n| **Care** | Dishwasher safe |",
        "name": "Salad Spinner",
        "price": "2999",
        "price_old": "4499",
        "quantity": 38,
        "slug": "salad-spinner",
        "specification": {},
        "status": "active",
        "tags": ["salad spinner", "kitchen tool", "food prep", "vegetables"],
        "variation": {
                "color": ["white", "green", "clear"]
        }
    },
    {
        "date_created": "Thu, 23 Oct 2025 16:15:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/hair_dryer_1.jpg"],
        "information": "**Professional hair dryer.** 2000W, ionic technology for frizz reduction, and includes concentrator nozzle.\n\n---\n\n## ✨ Key Features\n\n*   **2000W Motor**\n*   **Ionic Technology**\n*   **3 Heat/2 Speed Settings**\n*   **Cool Shot Button**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Power** | 2000W |\n| **Settings** | 3 heat, 2 speed |\n| **Technology** | Ionic |\n| **Warranty** | 2-Year Warranty |",
        "name": "Professional Hair Dryer",
        "price": "8999",
        "price_old": "12999",
        "quantity": 25,
        "slug": "professional-hair-dryer",
        "specification": {},
        "status": "active",
        "tags": ["hair dryer", "hair care", "ionic", "beauty"],
        "variation": {
                "color": ["white", "pink", "black"]
        }
    },
    {
        "date_created": "Wed, 22 Oct 2025 12:30:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/umbrella_1.jpg"],
        "information": "**Windproof travel umbrella.** Automatic open/close, compact size, and water-repellent fabric.\n\n---\n\n## ✨ Key Features\n\n*   **Windproof Design**\n*   **Automatic Open/Close**\n*   **Compact Size**\n*   **Water-Repellent**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Open Diameter** | 100cm |\n| **Folded Length** | 30cm |\n| **Ribs** | 8 fiberglass |\n| **Weight** | 0.4kg |",
        "name": "Windproof Travel Umbrella",
        "price": "1999",
        "price_old": "2999",
        "quantity": 70,
        "slug": "windproof-travel-umbrella",
        "specification": {},
        "status": "active",
        "tags": ["umbrella", "windproof", "travel", "compact"],
        "variation": {
                "color": ["black", "blue", "red", "transparent"],
                "size": ["compact", "large"]
        }
    },
    {
        "date_created": "Tue, 21 Oct 2025 09:40:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/bath_towel_set_1.jpg"],
        "information": "**Egyptian cotton bath towels.** Highly absorbent, soft, and includes 2 bath towels, 2 hand towels, 2 washcloths.\n\n---\n\n## ✨ Key Features\n\n*   **Highly Absorbent**\n*   **Soft & Durable**\n*   **6-Piece Set**\n*   **Machine Washable**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | 100% Egyptian Cotton |\n| **Set Includes** | 6 pieces |\n| **GSM Weight** | 600 |\n| **Care** | Machine washable |",
        "name": "Egyptian Cotton Towel Set",
        "price": "6999",
        "price_old": "9999",
        "quantity": 40,
        "slug": "egyptian-cotton-towel-set",
        "specification": {},
        "status": "active",
        "tags": ["towels", "bath towels", "egyptian cotton", "bathroom"],
        "variation": {
                "color": ["white", "gray", "blue", "beige"],
                "size": ["bath set", "guest set"]
        }
    },
    {
        "date_created": "Mon, 20 Oct 2025 15:25:15 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/electric_blanket_1.jpg"],
        "information": "**Double electric blanket.** 3 heat settings, auto shut-off, and machine washable for cozy warmth.\n\n---\n\n## ✨ Key Features\n\n*   **3 Heat Settings**\n*   **Auto Shut-Off**\n*   **Machine Washable**\n*   **Overheat Protection**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Size** | 150x130cm (Double) |\n| **Heat Settings** | 3 |\n| **Power** | 100W |\n| **Warranty** | 2-Year Warranty |",
        "name": "Electric Blanket",
        "price": "5999",
        "price_old": "8999",
        "quantity": 22,
        "slug": "electric-blanket",
        "specification": {},
        "status": "active",
        "tags": ["electric blanket", "heating", "bedding", "winter"],
        "variation": {
                "size": ["single", "double", "king"],
                "color": ["gray", "cream", "blue"]
        }
    },
    {
        "date_created": "Sun, 19 Oct 2025 11:50:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/wireless_charger_1.jpg"],
        "information": "**Fast wireless charger.** 15W charging, compatible with most smartphones, and includes cooling fan.\n\n---\n\n## ✨ Key Features\n\n*   **15W Fast Charging**\n*   **Universal Compatibility**\n*   **Cooling Fan**\n*   **LED Indicator**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Output** | 15W Max |\n| **Compatibility** | Qi-enabled devices |\n| **Input** | USB-C |\n| **Weight** | 0.2kg |",
        "name": "15W Fast Wireless Charger",
        "price": "2999",
        "price_old": "4999",
        "quantity": 55,
        "slug": "15w-fast-wireless-charger",
        "specification": {},
        "status": "active",
        "tags": ["wireless charger", "fast charging", "phone accessory", "qi"],
        "variation": {
                "color": ["black", "white", "blue"],
                "type": ["stand", "pad"]
        }
    },
    {
        "date_created": "Sat, 18 Oct 2025 14:35:25 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/grill_pan_1.jpg"],
        "information": "**Cast iron grill pan.** Creates perfect grill marks, oven safe, and pre-seasoned for non-stick cooking.\n\n---\n\n## ✨ Key Features\n\n*   **Creates Grill Marks**\n*   **Oven Safe**\n*   **Pre-Seasoned**\n*   **Even Heat Distribution**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Size** | 30x25cm |\n| **Material** | Cast Iron |\n| **Weight** | 3.5kg |\n| **Oven Safe** | Up to 260°C |",
        "name": "Cast Iron Grill Pan",
        "price": "4999",
        "price_old": "7499",
        "quantity": 28,
        "slug": "cast-iron-grill-pan",
        "specification": {},
        "status": "active",
        "tags": ["grill pan", "cast iron", "cookware", "grilling"],
        "variation": {
                "size": ["small", "medium", "large"]
        }
    },
    {
        "date_created": "Fri, 17 Oct 2025 10:15:30 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/phone_case_1.jpg"],
        "information": "**Protective phone case.** Shock-absorbent, raised edges for screen protection, and wireless charging compatible.\n\n---\n\n## ✨ Key Features\n\n*   **Shock-Absorbent**\n*   **Raised Edges**\n*   **Wireless Charging Compatible**\n*   **Precise Cutouts**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Material** | TPU + Polycarbonate |\n| **Drop Protection** | Up to 2m |\n| **Compatibility** | Model specific |\n| **Warranty** | 1-Year Warranty |",
        "name": "Protective Phone Case",
        "price": "1999",
        "price_old": "2999",
        "quantity": 150,
        "slug": "protective-phone-case",
        "specification": {},
        "status": "active",
        "tags": ["phone case", "protective case", "phone accessory", "mobile"],
        "variation": {
                "model": ["iphone 15", "samsung s23", "pixel 7"],
                "color": ["black", "clear", "blue", "pink", "green"]
        }
    },
    {
        "date_created": "Thu, 16 Oct 2025 16:40:45 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/steamer_basket_1.jpg"],
        "information": "**Silicone steamer basket.** Expandable design fits most pots, heat resistant, and dishwasher safe.\n\n---\n\n## ✨ Key Features\n\n*   **Expandable Design**\n*   **Heat Resistant**\n*   **Dishwasher Safe**\n*   **BPA-Free Silicone**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Diameter** | Adjustable 15-25cm |\n| **Material** | Food-grade silicone |\n| **Max Temperature** | 230°C |\n| **Care** | Dishwasher safe |",
        "name": "Silicone Steamer Basket",
        "price": "1499",
        "price_old": "2499",
        "quantity": 65,
        "slug": "silicone-steamer-basket",
        "specification": {},
        "status": "active",
        "tags": ["steamer basket", "kitchen tool", "healthy cooking", "silicone"],
        "variation": {
                "color": ["gray", "green", "red"]
        }
    },
    {
        "date_created": "Wed, 15 Oct 2025 13:25:20 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/digital_photo_frame_1.jpg"],
        "information": "**10-inch digital photo frame.** WiFi connectivity, cloud storage support, and auto-rotate for portrait/landscape.\n\n---\n\n## ✨ Key Features\n\n*   **10-inch Display**\n*   **WiFi Connectivity**\n*   **Cloud Storage Support**\n*   **Auto-Rotate**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Display** | 10\" 1280x800 |\n| **Storage** | 16GB internal |\n| **Connectivity** | WiFi, USB |\n| **Warranty** | 1-Year Warranty |",
        "name": "Digital Photo Frame",
        "price": "9999",
        "price_old": "14999",
        "quantity": 20,
        "slug": "digital-photo-frame",
        "specification": {},
        "status": "active",
        "tags": ["digital photo frame", "photo display", "smart frame", "gift"],
        "variation": {
                "size": ["8 inch", "10 inch", "15 inch"],
                "color": ["black", "white", "wood"]
        }
    },
    {
        "date_created": "Tue, 14 Oct 2025 09:50:35 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/cable_organizer_1.jpg"],
        "information": "**Cable management kit.** Includes clips, ties, and sleeves to organize cables at home or office.\n\n---\n\n## ✨ Key Features\n\n*   **Includes 50+ Pieces**\n*   **Reusable Cable Ties**\n*   **Adhesive Clips**\n*   **Cable Sleeves**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Kit Includes** | 50+ pieces |\n| **Material** | Nylon, PVC |\n| **Colors** | Black, White |\n| **Reusable** | Yes |",
        "name": "Cable Management Kit",
        "price": "1499",
        "price_old": "2499",
        "quantity": 85,
        "slug": "cable-management-kit",
        "specification": {},
        "status": "active",
        "tags": ["cable management", "organizer", "cables", "office supplies"],
        "variation": {
                "size": ["small kit", "large kit"],
                "color": ["black", "white"]
        }
    },
    {
        "date_created": "Mon, 13 Oct 2025 17:30:10 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/essential_oils_set_1.jpg"],
        "information": "**6 essential oils set.** 100 % pure therapeutic grade oils, includes lavender, peppermint, eucalyptus, etc.\n\n---\n\n## ✨ Key Features\n\n*   **100% Pure Therapeutic Grade**\n*   **6 Popular Oils**\n*   **Glass Bottles with Droppers**\n*   **Includes Guidebook**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Oils Included** | 6 x 10ml |\n| **Total Volume** | 60ml |\n| **Bottles** | Amber glass |\n| **Usage** | Aromatherapy, topical |",
        "name": "Essential Oils Set",
        "price": "3999",
        "price_old": "5999",
        "quantity": 45,
        "slug": "essential-oils-set",
        "specification": {},
        "status": "active",
        "tags": ["essential oils", "aromatherapy", "natural", "wellness"],
        "variation": {
                "set": ["6 oils", "12 oils", "beginner set"]
        }
    },
    {
        "date_created": "Sun, 12 Oct 2025 12:45:25 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/wine_rack_1.jpg"],
        "information": "**Wall-mounted wine rack.** Holds 6 bottles, minimalist metal design, and easy installation.\n\n---\n\n## ✨ Key Features\n\n*   **Holds 6 Bottles**\n*   **Wall-Mounted**\n*   **Minimalist Design**\n*   **Easy Installation**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Capacity** | 6 bottles |\n| **Material** | Powder-coated steel |\n| **Dimensions** | 60x15x15cm |\n| **Installation** | Wall mounting required |",
        "name": "Wall-Mounted Wine Rack",
        "price": "2999",
        "price_old": "4499",
        "quantity": 30,
        "slug": "wall-mounted-wine-rack",
        "specification": {},
        "status": "active",
        "tags": ["wine rack", "wine storage", "wall mounted", "home bar"],
        "variation": {
                "capacity": ["6 bottles", "12 bottles", "18 bottles"],
                "color": ["black", "white", "bronze"]
        }
    },
    {
        "date_created": "Sat, 11 Oct 2025 15:20:40 GMT",
        "files": ["http://127.0.0.1:5000/photo/item/baking_sheet_set_1.jpg"],
        "information": "**Non-stick baking sheet set.** 3-piece set including half sheet, quarter sheet, and cooling rack.\n\n---\n\n## ✨ Key Features\n\n*   **Non-Stick Coating**\n*   **3-Piece Set**\n*   **Even Heat Distribution**\n*   **Dishwasher Safe**\n\n---\n\n## 📐 Specifications\n\n| Category | Specification |\n| :--- | :--- |\n| **Set Includes** | 3 pieces |\n| **Material** | Carbon steel |\n| **Coating** | Non-stick |\n| **Oven Safe** | Up to 230°C |",
        "name": "Non-Stick Baking Sheet Set",
        "price": "3999",
        "price_old": "5999",
        "quantity": 35,
        "slug": "non-stick-baking-sheet-set",
        "specification": {},
        "status": "active",
        "tags": ["baking sheets", "non-stick", "baking", "kitchen"],
        "variation": {
                "set": ["3 piece", "5 piece"]
        }
    }
]


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE item
        ALTER COLUMN quantity SET DEFAULT 10;
    """)

    # cur.execute("""
    #     ALTER TABLE item
    #     ADD COLUMN specification JSONB DEFAULT '{}'::JSONB;
    # """)

    # columns = list(data[0].keys())

    # values_list = []
    # for row in data:
    #     values = []
    #     for column in columns:
    #         if type(row[column]) is dict:
    #             row[column] = Json(row[column])
    #         values.append(row[column])
    #     values_list.append(tuple(values))

    # cur.executemany(f"""
    #     INSERT INTO item ({', '.join(columns)})
    #     VALUES ({', '.join(['%s'] * len(columns))});
    # """, values_list)

    # cur.execute("""
    #     UPDATE "user" SET access=%s WHERE email = %s;
    # """, (
    #     [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]],
    #     os.environ["MAIL_USERNAME"]
    # ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
