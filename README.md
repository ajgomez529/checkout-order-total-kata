# checkout-order-total-kata
Python module implementing business logic for grocery point-of-sale system

Based on the following: https://github.com/PillarTechnology/kata-checkout-order-total

## Requirements
Tested in Python 3.5+.
No additional dependencies required for use.

## Installation
Place `checkout.py` in your project directory. To run the test suite, ensure `checkout.py` and `test_suite_checkout.py` are in the same directory.
## Usage
```python
import checkout

checkout_system = checkout.CheckoutSystem()  # create checkout system

checkout_system.register_item('soup', 1.99)  # add item sold by unit
checkout_system.register_item('onion', 1.00, 'lb')  # add item sold by lb

checkout_system.markdown('soup', 0.50)  # $0.50 markdown on soup
checkout_system.n_for_x('onion', 3, 2.00)  # buy 3 lbs of onions for $2.00

order = checkout.Order(checkout_system)  #initialize order using checkout_system

order.scan_item('soup')  # scan unit of soup
order.scan_item('onion', 4.0)  # scan 4 lb of onions
order.remove_item_qty('onion', 1.0)  # remove 1 lb of onion
print (order.return_total())  # returns order total - 3.49
# onion - 3 lb for $2.00
# soup - $1.99 - $0.50 markdown
```

## Testing

To run the full testing suite, run the following command in the project directory:
```
python3 test_suite_checkout.py
```

To test a class of test cases, run the following command (replace as needed):
```
python3 test_suite_checkout.py ItemSetUp
```
To run a single test case, run the following command (replace as needed):
```
python3 test_suite_checkout.py ItemSetUp.test_remove_item
```


The test suite is also run in Python 3.5-3.8 upon push to the repository, generating a coverage report.

This Github Actions workflow requires pytest and pytest-cov. To produce the coverage report locally, run the following commands to install the required packages:

```
pip install pytest
pip install pytest-cov
```

Run this command in the project directory to generate the coverage report:

```
pytest --cov-report term-missing --cov=checkout test_suite_checkout.py
```

The output should appear in the terminal:

```
----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
checkout.py     123      0   100%
-------------------------------------------
TOTAL           123      0   100%
```

