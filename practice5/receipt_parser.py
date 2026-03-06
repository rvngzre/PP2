import re
import json

def parse_receipt(text):

    product_pattern = r"\d+\.\s*\n(.+)"
    products = re.findall(product_pattern, text)

    price_pattern = r"Стоимость\s*\n([\d ]+,\d{2})"
    prices = re.findall(price_pattern, text)

    total_pattern = r"ИТОГО:\s*\n?([\d ]+,\d{2})"
    total_match = re.search(total_pattern, text)
    total = total_match.group(1) if total_match else None

    datetime_pattern = r"Время:\s*([\d\.]+\s[\d:]+)"
    datetime_match = re.search(datetime_pattern, text)
    datetime = datetime_match.group(1) if datetime_match else None

    payment_pattern = r"(Банковская карта|Наличные)"
    payment_match = re.search(payment_pattern, text)
    payment = payment_match.group(1) if payment_match else None

    return {
        "products": products,
        "prices": prices,
        "total": total,
        "datetime": datetime,
        "payment_method": payment
    }


def main():

    with open("raw.txt", "r", encoding="utf-8") as file:
        text = file.read()

    data = parse_receipt(text)

    print("\n----- RECEIPT DATA -----\n")
    print("Products:")
    for p in data["products"]:
        print("-", p)

    print("\nPrices:")
    for pr in data["prices"]:
        print("-", pr)

    print("\nTotal:", data["total"])
    print("Date & Time:", data["datetime"])
    print("Payment Method:", data["payment_method"])

    print("\n----- JSON OUTPUT -----\n")
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()