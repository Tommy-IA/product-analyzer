import json

def margin(price, cost):
    if price <= 0.0:
        raise ValueError("Price must be greater than 0.0")
    return ((price - cost) / price) * 100

margin_dict = {
    "tool_name":"margin",
    "description": "Calculate margin with price, cost",
    "parameters":{
        "type":"object",
        "properties":{"price":{"type":"number"},"cost":{"type":"number"}}
    },
    "required" : ["price","cost"]}


def food_cost(cost, price):
    if price <= 0.0:
        raise ValueError("Price must be greater than 0.0")
    return (cost/price)*100

food_cost_dict = {
    "tool_name":"food_cost",
    "description":"calculate food cost based by cost, price",
    "parameters":{
        "type":"object",
        "properties":{
            "cost":{"type":"number"},
            "price":{"type":"number"}
        }
    },
    "required":["cost","price"]
}

def markUp(cost, price):
    if cost <= 0.0:
        raise ValueError("Cost must be greater than 0.0")
    return ((price-cost) / cost) *100

markUp_dict = {
    "tool_name":"markUp",
    "description":"calculate markUP based by cost, price",
    "parameters":{
        "type":"object",
        "properties":{
            "cost":{"type":"number"},
            "price":{"type":"number"}
        }
    },
    "required":["cost","price"]
}


RESTAURANT_RANGES = {
    "markup":{
        "red_low": 50,
        "green_low":100,
        "green_high":300,
        "red_high":400
    },
    "food_cost":{
        "red_low":20,
        "green_low":25,
        "green_high":35,
        "red_high":40
    },
    "margin": {
        "red_low":55,
        "green_low":65,
        "green_high":75,
        "red_high":80
    }
}


def alert_function(value, metric_type):
    if metric_type not in RESTAURANT_RANGES:
        raise ValueError(f"Invalid metric type: {metric_type}")
    ranges = RESTAURANT_RANGES[metric_type]
    if value < ranges["red_low"] or value >= ranges["red_high"]:
        return "🔴 PROBLEM range out of limits for standard business"
    elif ranges["green_low"] <= value <= ranges["green_high"]:
        return "🟢 PERFECT range on line with limits for standard business"
    else:
        return "🟡 ATTENTION range going out of limits for standard business"
    
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
        if item.get("Current price") is None:
            continue
        else:
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
                if current_profit != 0:
                    record["Increase percentage"] = (difference / current_profit) * 100
                else:
                    record["Increase percentage"] = 0
            profit.append(record)
    return profit

def write_doc(report, file_name):
    with open (file_name,"w") as f:
        json.dump(report, f, indent= 4)


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
        if price is None:
            suggested_price = suggest_price_one(cost, target_margin)
            markupNP = markUp(cost, suggested_price)
            foodcostNP = food_cost(cost, suggested_price)
            profit = suggested_price - cost
            checkNP = alert_function(markupNP,"markup")
            checkFCNP = alert_function(foodcostNP,"food_cost")
            report.append({
                "Product": product,
                "Initial cost": cost,
                "Target margin %": target_margin,
                "Potential profit": profit,
                "Suggested price": suggested_price,
                "MarkUP by suggeested price in % " : markupNP,
                "Check Markup with suggested price" : checkNP,
                "FoodCost by suggested price in %" : foodcostNP,
                "Check FoodCost with suggested price" : checkFCNP
            })
        else:
            m = margin(price, cost)
            markupYP = markUp(cost, price)
            foodcostYP = food_cost(cost, price)
            checkMPYP = alert_function(markupYP,"markup")
            checkFCYP = alert_function(foodcostYP,"food_cost")
            checkME = alert_function(m,"margin")
            if m < target_margin:
                suggested_price = suggest_price_one(cost, target_margin)
            else:
                suggested_price = None
            report.append({
                "Product": product,
                "Initial cost": cost,
                "Current price": price,
                "Margin %": m,
                "Check Margin":checkME,
                "Suggested price": suggested_price,
                "MarkUP by original price in % " : markupYP,
                "Check MarkUP with original price" : checkMPYP,
                "FoodCost by original price in %" : foodcostYP,
                "Check FoodCost with original price" : checkFCYP
            })
            if suggested_price is not None:
                markupSG = markUp(cost,suggested_price)
                foodcostSG = food_cost(cost, suggested_price)
                checkNPs = alert_function(markupSG,"markup")
                checkFCNPs = alert_function(foodcostSG,"food_cost")
                report[-1]["MArkUP by suggested price in %"] = markupSG
                report[-1]["Check MarkUP by suggested price"] = checkNPs
                report[-1]["FoodCost by suggested price in %"] = foodcostSG
                report[-1]["Check FoodCost by suggested price"] = checkFCNPs
    profit = profit_analysis(report)
    for product in report:
        for profit_item in profit:
            if profit_item["Product"] == product["Product"]:
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
        if item.get("Current price") is None:
            final_prices.append(item["Suggested price"])
        else:
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
            while True:
                price_get = input(f"Do you have the initial price for {product} (Y/N): ").strip().lower()
                if price_get != "y" and price_get != "n":
                    print("Please answer Y or N")
                    continue
                if price_get == "y":
                        cost_input = input_float(f"Enter the initial cost for {product}: ")
                        list_cost.append(cost_input)
                        price_input = input_float(f"Enter the current price for {product}: ")
                        list_price.append(price_input)
                        break
                else:
                        cost_input = input_float(f"Enter the cost for {product}: ")
                        list_cost.append(cost_input)
                        list_price.append(None)
                        break
        filtered_price = []
        filtered_cost = []
        for price, cost in zip (list_price, list_cost):
            if price is not None:
                filtered_price.append(price)
                filtered_cost.append(cost)
        if len(filtered_cost) == 0:
            average_m = None
        else:
            average_m = average_margin(filtered_price, filtered_cost)
        report = analyze_menu(list_products, list_price, list_cost, target_margin)
        final_prices = build_final_prices(report)
        average_nm = average_margin(final_prices, list_cost)
        print("\n" + "=" * 70)
        print("RESTAURANT MENU FINANCIAL REPORT")
        print("=" * 70)
        print(f"Target margin selected: {target_margin:.2f}%")
        for item in report:
            print("\n" + "-" * 70)
            print(f"PRODUCT: {item['Product']}")
            print("-" * 70)
            if item.get("Current price") is None:
                print("FINANCIAL OVERVIEW")
                print(f"Initial cost: £{item['Initial cost']:.2f}")
                print(f"Current selling price: Not provided")
                print(f"Target margin: {item['Target margin %']:.2f}%")
                print(f"Potential profit at suggested price: £{item['Potential profit']:.2f}")
                print("\nRECOMMENDED PRICE POSITION")
                print(f"Suggested selling price: £{item['Suggested price']:.2f}")
                print(f"Markup at suggested price: {item['MarkUP by suggeested price in % ']:.2f}%")
                print(f"Markup status: {item['Check Markup with suggested price']}")
                print(f"Food cost at suggested price: {item['FoodCost by suggested price in %']:.2f}%")
                print(f"Food cost status: {item['Check FoodCost with suggested price']}")
            else:
                if "Potential profit" in item:
                    print("CURRENT PERFORMANCE")
                    print(f"Initial cost: £{item['Initial cost']:.2f}")
                    print(f"Current selling price: £{item['Current price']:.2f}")
                    print(f"Current margin: {item['Margin %']:.2f}%")
                    print(f"Margin status: {item['Check Margin']}")
                    print(f"Current profit per sale: £{item['Current profit']:.2f}")
                    print("\nPRICE IMPROVEMENT OPPORTUNITY")
                    print(f"Suggested selling price: £{item['Suggested price']:.2f}")
                    print(f"Potential profit per sale: £{item['Potential profit']:.2f}")
                    print(f"Extra profit per sale: £{item['Profit difference']:.2f}")
                    print(f"Required price increase: +{item['Increase percentage']:.2f}%")
                    print("\nCURRENT PRICE METRICS")
                    print(f"Markup: {item['MarkUP by original price in % ']:.2f}%")
                    print(f"Markup status: {item['Check MarkUP with original price']}")
                    print(f"Food cost: {item['FoodCost by original price in %']:.2f}%")
                    print(f"Food cost status: {item['Check FoodCost with original price']}")
                    print("\nSUGGESTED PRICE METRICS")
                    print(f"Markup: {item['MArkUP by suggested price in %']:.2f}%")
                    print(f"Markup status: {item['Check MarkUP by suggested price']}")
                    print(f"Food cost: {item['FoodCost by suggested price in %']:.2f}%")
                    print(f"Food cost status: {item['Check FoodCost by suggested price']}")
                else:
                    print("CURRENT PERFORMANCE")
                    print(f"Initial cost: £{item['Initial cost']:.2f}")
                    print(f"Current selling price: £{item['Current price']:.2f}")
                    print(f"Current margin: {item['Margin %']:.2f}%")
                    print(f"Margin status: {item['Check Margin']}")
                    print(f"Current profit per sale: £{item['Current profit']:.2f}")
                    print("\nPRICING DECISION")
                    print("No price increase is currently needed.")
                    print("\nCURRENT PRICE METRICS")
                    print(f"Markup: {item['MarkUP by original price in % ']:.2f}%")
                    print(f"Markup status: {item['Check MarkUP with original price']}")
                    print(f"Food cost: {item['FoodCost by original price in %']:.2f}%")
                    print(f"Food cost status: {item['Check FoodCost with original price']}")
        print("\n" + "=" * 70)
        print("PORTFOLIO SUMMARY")
        print("=" * 70)
        if len(filtered_price) > 0:
            print(f"Average current margin across priced products: {average_m:.2f}%")
        if any("Potential profit" in item for item in report):
            print(f"Average final margin after suggested pricing: {average_nm:.2f}%")
        print("=" * 70)
    except ValueError as e:
        print(f"\nCannot calculate, error: {e}")


if __name__ == "__main__":
    main()
