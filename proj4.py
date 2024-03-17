# Full Project

testProducts = { #use this dictionary to test functions quickly
    "ABC": {
        "categories": ["food", "electronics"],
        "name": "laptop",
        "weight": 5.0,
        "price": 650.00,
	    "currency" : "USD",
        "notes": "lots of features"
    },
    "DEF": {
        "categories": ["electronics"],
        "name": "TV",
        "weight": 15.0,
        "price": 550.00,
	    "currency" : "USD",
        "notes": "lots of features"
    }
}

cart = {
    "products": {},
    "productsTotalCost": 0.00,
    "productsTotalWeight": 0.00,
    "deliveryState": "",
    "taxAmount": 0.00, 
    "deliveryMethod": "",   
    "deliveryCost": 0.00,
	"deliveryDaysEstimate": 0,
	"cartTotal": 0.00
}



def getProductsBySearch (testProducts, searchTerm):
    ''' 
    searches name and notes for presence of searchTerm
    search is case-insensitive
    returns a list of product codes, or an empty list 
    '''
    product_code = []
    for code, product_info in testProducts.items():
        name = product_info.get('name').lower()
        notes = product_info.get('notes').lower()

        if searchTerm.lower() in name or searchTerm.lower() in notes:
            product_code.append(code)

    return product_code


def getProductsByCategory(testProducts, categoryName):
    ''' returns a list of product codes for the category name, or an empty list '''
    code_list = []
    for code, productinfo in testProducts.items():
        if categoryName in productinfo['categories']:
            code_list.append(code)
    return code_list

def getProductCategories(testProducts):
    ''' returns a list of category names, sorted '''
    product_list = []
    for product in testProducts.values():
        product_list.extend(product['categories'])
    return sorted(set(product_list))

import requests

def getExchangeRate(currencyCode):
    ''' 
    retrieve current exchange rate
   
        return -1 if code is invalid
    
	   usage:
		returned value is divisor to get USD value
		e.g. if price is in CAD, 
			price / getExchangeRate("CAD") is the USD price

    '''
   
    # default to a value that will indicate an error
    exchangeRate = -1
   
    if (currencyCode == "USD"):
        # don't need to make API call
        exchangeRate = 1
    else:
        # address for API that returns exchange rate data
        url = "https://v6.exchangerate-api.com/v6/add9f6398d00f2d51dc0511b/latest/USD"
       
        # make the request
        response = requests.get(url)

        # convert the response from JSON to Python object(s)
        data = response.json()

        rates = data["conversion_rates"]

        if (currencyCode in rates):
            exchangeRate = float(rates[currencyCode])

    return exchangeRate

def getProductPrice(testProducts, productCode):
    ''' return price in USD as float 
        uses getExchangeRate function to extract the currency exchange rate
    '''
    if productCode in testProducts:
        price = testProducts[productCode]['price']
        curr_code = testProducts[productCode]['currency']
        ex_rate = getExchangeRate(curr_code)

    return round(price / ex_rate, 1) # always returns price in USD

def setCartItemQuantity(cart, productCode, quantity):
    ''' 
    update cart products dictionary
    quantity is the new quantity, not the change in quantity
    quantity value <= 0 should remove productCode from dictionary
    productsTotalCost, productsTotalWeight, cartTotal are set to 0
    returns count of productCodes in the cart 
    '''
    q_total = 0
    if quantity <= 0:
        if productCode in cart['products']:
            del cart['products'][productCode]

    else:
        cart['products'][productCode] = quantity

    # Total quantity of items in 'products' (optional)
    for quantity in cart['products'].values():
        q_total += quantity

    return len(cart['products'])


def updateCartTotals(testProducts, cart):
    ''' 
    update productsTotalCost, productsTotalWeight, cartTotal
    return cartTotal 
    '''
    total_cost = 0
    total_weight = 0

    for product_code, quantity in cart['products'].items():
        if product_code in testProducts.keys():
            product = testProducts[product_code]
            price = getProductPrice(testProducts, product_code) # Get price from getProductPrice function
            weight =product['weight'] # Get weight

            total_cost += price * quantity # Update total cost
            total_weight += weight * quantity # Update total weights

    cart['productsTotalCost'] = total_cost # Update cart with total cost
    cart['productsTotalWeight'] = total_weight # Update cart with total weight

    cart['cartTotal'] = total_cost + cart['taxAmount'] + cart['deliveryCost'] # Add tax and delicery costs
    
    return round(cart['cartTotal'], 1)

import data
import csv

filename = r'shippingRatesAndTimes.csv' # Change with your file path  

def read_shipping_rates(filename):
    '''
    Function to read data from shippingRatesAndTimes.csv file
    '''
    shipping_rates = []
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row 
        for row in csv_reader:
            shipping_rates.append(row)

    return shipping_rates



# User Interface (Removed)


def getInformationHeader(title):
	# accepts a string
	# returns a string of the header, as described in the design document
    header = f"\n{'=' * 60}\n {title.upper()}\n{'=' * 60}\n"
    return header


def getFormattedPrompt(prompt):
	# accepts a string
	# returns a string of the formatted prompt, as described in the design document
    formatted_prompt = f"\n{'*' * 60}\n{prompt}\n"
    return formatted_prompt


def displayProductCategories(productCategories):
	# accepts a list of product categories
	# prints as described in the design document
    print(getInformationHeader("Product Categories"))
    print("{:>3} {:<52}".format("#", "Name"))
    for index, category in enumerate(productCategories, start=1):
        print("{:>3} {:<52}".format(index, category))


def displayProducts(products, productCodes):
	# accepts the products dictionary and list of product codes
	# prints as described in the design document
    print(getInformationHeader("Products"))
    print("{:>3} {:<52}".format("#", "Name"))
     # Iterate over product codes
    for index, code in enumerate(productCodes, start=1):
        product = products.get(code)
        if product:
            name = product['name']
            print("{:>3} {:<52}".format(index, name))


def displayCartItems(products, cart):
	# accepts the products dictionary and the cart
	# prints as described in the design document
    print(getInformationHeader("Cart Items List"))
    print("{:>3} {:<20} {:>5} {:>10} {:>15}".format("#", "Name", "Qty", "Price", "Total"))
    
    index = 1
    for product_code, quantity in cart['products'].items():
        product = products.get(product_code)
        if product:
            name = product['name'] if len(product['name']) <= 20 else product['name'][:17] + "..."
            price = product['price']
            total_price = price * quantity
            print("{:>3} {:<20} {:>5} {:>10.2f} {:>15.2f}".format(index, name, quantity, price, total_price))
            index += 1

    # Print footer
    print("-" * 60)
    print("{:>8} {:<37} {:>15.2f}".format("", "Products Total", cart['productsTotalCost']))



def displayCartTotals(products, cart):
	# accepts the products dictionary and the cart
	# prints the cart tax, shipping and grand total, as described in the design document

    displayCartItems(products, cart)

    # Print footer
    print("-" * 60)
    print("{:<8} {:<37} {:>15.2f}".format("", "Products Total", cart['productsTotalCost']))
    print("{:<8} {:<37} {:>15.2f}".format("", "Sales Tax (MD @ 5.0%)", cart['taxAmount']))
    print("{:<8} {:<37} {:>15.2f}".format("", "Shipping  (MD - Overnight)", cart['deliveryCost']))
    print("-" * 60)
    print("{:<8} {:<37} {:>15.2f}".format("", "Total", cart['cartTotal']))



