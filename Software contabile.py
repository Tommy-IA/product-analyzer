def margin(price, cost):
    if price <= 0.0:
        raise ValueError("Price must be greater than 0.0")
    return ((price - cost) / price) * 100


def average_margin(list_price, list_cost):
    if len(list_price) == 0:
        raise ValueError("The list must contain one or more prices")
    if len(list_cost) == 0:
        raise ValueError("The list must contain one or more costs")
    if len(list_price) != len(list_cost):
        raise ValueError("The lists must have the same number of elements")
    total_margin = 0
    for price, cost in zip(list_price, list_cost):
        total_margin += margin(price, cost)
    return total_margin / len(list_price)


def suggest_price_one(cost, target_margin):
    return cost / (1 - (target_margin / 100))


def suggest_price(list_cost, target_margin) -> list[float]:
    if len(list_cost) == 0:
        raise ValueError("The list must contain one or more costs")
    if not (0 < target_margin < 100):
        raise ValueError("The target margin must be between 0 and 100, e.g. 60")
    suggested_prices = []
    for cost in list_cost:
        suggested_prices.append(suggest_price_one(cost, target_margin))
    return suggested_prices


def profit_analysis(report):
    profit = []
    for item in report:
        product_name = item["Product"]
        current_price = item["Current price"]
        cost = item["Initial cost"]
        suggested_price = item["Suggested price"]
        current_profit = current_price - cost
        if suggested_price is not None and suggested_price >= current_price:
            final_price = suggested_price
        else:
            final_price = current_price
        potential_profit = final_price - cost
        record = {
            "Product": product_name,
            "Current profit": current_profit
        }
        if final_price != current_price:
            record["Potential profit"] = potential_profit
            difference = potential_profit - current_profit
            record["Profit difference"] = difference
            record["Increase percentage"] = (difference / current_profit) * 100
        profit.append(record)
    return profit


def analyze_menu(list_products, list_price, list_cost, target_margin):
    report = []
    if len(list_price) == 0:
        raise ValueError("The list must contain one or more prices")
    if len(list_cost) == 0:
        raise ValueError("The list must contain one or more costs")
    if len(list_price) != len(list_cost):
        raise ValueError("The lists must contain the same number of elements")
    if len(list_products) == 0:
        raise ValueError("The list must contain one or more products")
    if len(list_price) != len(list_products):
        raise ValueError("The lists must contain the same number of elements")
    for product, price, cost in zip(list_products, list_price, list_cost):
        m = margin(price, cost)
        if m < target_margin:
            suggested_price = suggest_price_one(cost, target_margin)
        else:
            suggested_price = None
        report.append({
            "Product": product,
            "Initial cost": cost,
            "Current price": price,
            "Margin %": m,
            "Suggested price": suggested_price,
        })
    profit = profit_analysis(report)
    for product, profit_item in zip(report, profit):
        product["Current profit"] = profit_item["Current profit"]
        if "Potential profit" in profit_item:
            product["Potential profit"] = profit_item["Potential profit"]
            product["Profit difference"] = profit_item["Profit difference"]
            product["Increase percentage"] = profit_item["Increase percentage"]
    return report


def clean_input(text):
    text_clean = text.strip().lower()
    result = ""
    for c in text_clean:
        if c == "," or c.isdigit() or c == ".":
            result += c
    return result.replace(",", ".")


def input_percentage(prompt):
    while True:
        value = input(prompt).strip()
        value_clean = clean_input(value)
        if value_clean == "":
            print("Please enter a valid numeric value")
            continue
        try:
            value_float = float(value_clean)
        except ValueError:
            print("Please enter a valid numeric value")
            continue
        if value_float <= 0.00 or value_float >= 100:
            print("The value must be greater than 0 and less than 100")
            continue
        return value_float


def input_float(prompt):
    while True:
        value = input(prompt).strip()
        value_clean = clean_input(value)
        if value_clean == "":
            print("Please enter a valid numeric value")
            continue
        try:
            value_float = float(value_clean)
        except ValueError:
            print("Please enter a valid numeric value")
            continue
        if value_float <= 0.00:
            print("The value cannot be negative or zero")
            continue
        return value_float


def build_final_prices(report):
    final_prices = []
    for item in report:
        if item["Suggested price"] is not None and item["Suggested price"] >= item["Current price"]:
            final_prices.append(item["Suggested price"])
        else:
            final_prices.append(item["Current price"])
    return final_prices


def main():
    try:
        target_margin = input_percentage("Enter the target margin (e.g. 60%): ")
        list_products = []
        list_price = []
        list_cost = []
        while True:
            product = input("Enter a product name (or 'done' to finish): ")
            if product.lower() == 'done':
                break
            if not product:
                print("Please enter a valid product name.")
                continue
            list_products.append(product)
        for product in list_products:
            cost_input = input_float(f"Enter the initial cost for {product}: ")
            list_cost.append(cost_input)
            price_input = input_float(f"Enter the current price for {product}: ")
            list_price.append(price_input)
        report = analyze_menu(list_products, list_price, list_cost, target_margin)
        average_m = average_margin(list_price, list_cost)
        final_prices = build_final_prices(report)
        average_nm = average_margin(final_prices, list_cost)
        print("\n-- Report --")
        print(f"Target margin: {target_margin:.2f}%")
        for item in report:
            if "Potential profit" in item:
                print(f"\nProduct: {item['Product']}")
                print(f"Initial cost: £{item['Initial cost']:.2f}\n"
                      f"Current price: £{item['Current price']:.2f}\n"
                      f"Current margin: {item['Margin %']:.2f}%\n"
                      f"Current profit: £{item['Current profit']:.2f}\n"
                      f"Potential profit: £{item['Potential profit']:.2f}\n"
                      f"Profit difference: £{item['Profit difference']:.2f}\n")
            else:
                print(f"\nProduct: {item['Product']}")
                print(f"Initial cost: £{item['Initial cost']:.2f}\n"
                      f"Current price: £{item['Current price']:.2f}\n"
                      f"Margin: {item['Margin %']:.2f}%\n"
                      f"Profit: £{item['Current profit']:.2f}\n"
                      "No increase expected")
            if item["Suggested price"] is None or item["Current price"] >= item["Suggested price"]:
                print("Suggested price: No change needed")
            else:
                print(f"Suggested price with target margin: £{item['Suggested price']:.2f}")
                print(f"Increase percentage: {item['Increase percentage']:.2f}%")
        print(f"\nAverage initial margin for all products: {average_m:.2f}%")
        if any("Potential profit" in item for item in report):
            print(f"Average final margin with suggested prices: {average_nm:.2f}%")
    except ValueError as e:
        print(f"\nCannot calculate, error: {e}")


if __name__ == "__main__":
    main()