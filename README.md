# product-analyzer
This short software helps a business insert a target margin,  the cost and the price for a product and calculates the actual margin, the actual profit, and if under the target, suggests a new price, calculating the potential profit, the difference from the original price and the average margin.
The user only needs to insert a target margin, the initial cost and the base price for each product. 
It will print an easy to read report.

## Output
Here a example of a output using 2 items in a pawn shops, using a computer and a smarthphone:

Enter the target margin (e.g. 60%): 60
Enter a product name (or 'done' to finish): Laptop
Enter a product name (or 'done' to finish): Smartphone
Enter a product name (or 'done' to finish): done
Enter the initial cost for Laptop: 200
Enter the current price for Laptop: 350£
Enter the initial cost for Smartphone: 120
Enter the current price for Smartphone: 200

-- Report --
Target margin: 60.00%

Product: Laptop
Initial cost: £200.00
Current price: £350.00
Current margin: 42.86%
Current profit: £150.00
Potential profit: £300.00
Profit difference: £150.00

Suggested price with target margin: £500.00
Increase percentage: 100.00%

Product: Smartphone
Initial cost: £120.00
Current price: £200.00
Current margin: 40.00%
Current profit: £80.00
Potential profit: £180.00
Profit difference: £100.00

Suggested price with target margin: £300.00
Increase percentage: 125.00%

Average initial margin for all products: 41.43%
Average final margin with suggested prices: 60.00%

## ## Features for V2.0
- Markup calculation and alerts
- Option to skip the initial price for a direct suggested price
- Save data to CSV/JSON for history and generate reports 
  with alerts for underperforming products
- Restaurant features such as plate cost calculation 
  from ingredient weight and price

## Requirements
- Python 3.13
- No external libraries needed

## Author
**Tommaso Marras**  
<a href="https://github.com/Tommy-IA" target="_blank">
<img src="https://raw.githubusercontent.com/Tommy-IA/tesla-game-stock-analysis/main/logo.png" width="35">
</a>
[LinkedIn](https://www.linkedin.com/in/tommaso-marras-a681252ba) · [GitHub](https://github.com/Tommy-IA)
