class Item:
    """Stores information for single item used in checkout

    Attributes:
        name: item name as string (e.g. 'soup').
        price: price in USD as float (e.g. 2.99).
        soldBy: how the item is sold as string (e.g. 'lbs').
        markdown: float representing discount off regular price
        special: init as None; stores parameters for special savings on
          item. Only one special can be applied at a time.
    """

    def __init__(self, name, price, soldBy):
        self.name = name
        self.price = price
        self.soldBy = soldBy
        self.markdown = None
        self.special = None

class CheckoutSystem:
    """A checkout system that maintains a list of items and calculates prices

    Attributes: 
        items: dictionary holding Item objects. Item name is stored as key;
          Item object is stored as value. 
    """

    def __init__(self):
        self.items = {}

    def register_item(self, name, price, soldBy='unit'):
        """Adds item to checkout system.

        Creates Item object and stores in checkout system.

        Args:
            name: item name as string (e.g. 'soup').
            price: price in USD as float (e.g. 2.99).
            soldBy: optional; how the item is sold as string (e.g. 'lbs').
              if not provided, 'unit' is assumed.
        """
        item = Item(name, price, soldBy)
        self.items[name] = item

    def unregister_item(self, name):
        """Removes item from checkout system.

        Removes existing Item object stored in checkout system.

        Args:
            name: item name as string (e.g. 'soup').

        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """

        self.items.pop(name)

    def update_price(self, name, price):
        """Updates price of an existing item

        Args:
            name: item name as string (e.g. 'soup').
            price: new price in USD as float (e.g. 2.99).
        
        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """

        self.items[name].price = price

    def markdown(self, name, discount):
        """Applies a markdown to an existing item.

        When a markdown is applied to an item, the item price will be reduced
        by {discount}.

        This function sets the Item class attribute 'markdown' for the named
        item to the discount value.

        Args:
            name: item name as string (e.g. 'soup').
            discount: price reduction in USD as float (e.g. 0.50). Value
              should not exceed price of item.

        Raises:
            ValueError if discount is less than 0 or greater than the item price
            KeyError if item name does not exist in CheckoutSystem
        """
        if discount < 0 or discount > self.items[name].price:
            raise ValueError('Discount cannot be less than 0 or more than the item price')
        else:
            self.items[name].markdown = discount
    
    def remove_markdown(self, name):
        """Removes a markdown from an existing item.

        This function sets the Item class attribute for the named item to
        None. 

        Args:
            name: item name as string (e.g 'soup')

        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """

        self.items[name].markdown = None

    def remove_all_markdowns(self):
        """Removes markdown from all items in checkout system.

        This function sets the Item class atrribute for all all items
        to None.

        Args: None
        """
        for item in self.items.values():
            item.markdown = None

    def NforX(self, name, N, X, limit=None):
        """Applies a N for $X special to an existing item.

        When applied to an item, {N} units of that item may be purchased for
        the total price of ${X} dollars. For example, "3 cans for $5.00" or
        "2 lbs of ground beef for $6". The special can be limited to a 
        maximum of {limit} units. Applies to items sold by unit and weight.

        This function sets the Item class attribute 'special' for the named
        item to the following array: [2, N, X, limit]
        The first entry, 2, identifies the type of special. 
        

        Args:
            name: item name as string (e.g. 'soup').
            N: int representing the number of units
            X: total price for N units as float
            limit: optional; int representing the maximum number of units 
              eligible under the special. value must be a multiple of N
        
        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """

        self.items[name].special = [2, N, X, limit]

    def buyNgetMatXoff(self, name, N, M, X, limit=None):
        """Applies a buy N, get M for X% off special to an existing item.

        When applied to an item, after purchasing {N} units at regular price,
        an additioanl {M} units may be purchased for X% off each. For example,
        "Buy 1, get 1 free (X=100 % off). The special can be limited to a
        a maximum of {limit} units. Applies to items sold by unit and weight.

        This function sets the Item class attribute 'special' for the named
        item to the following array: [3, N, M, X, limit]
        The first entry, 3, identifies the type of special. 

        Args:
            name: item name as string (e.g. 'soup')
            N: int representing the number of units that must be purchased at
              full price to quality for discount
            M: int representing the number of units after N units that may
              receive the discounted price
            X: float representing the discount as a percent. For example, a
              value of 100 indicates that M items may be purchased at a 100%
              discount (i.e. free).
            limit: optional; int representing the maximum number of units
              eligible under the special. value must be a multiple of N+M

        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """
        self.items[name].special = [3, N, M, X, limit]
    
    def remove_special(self, name):
        """Removes an existing special applied to an item.

        This function sets the Item class attribute 'special' for the named
        item to None.

        Args:
            name: item name as string (e.g. 'soup')
        
        Raises:
            KeyError if item name does not exist in CheckoutSystem
        """
        self.items[name].special = None

    def remove_all_specials(self):
        """Removes all specials applied to all items.

        This function sets the Item class attribute 'special' for all items
        in the CheckoutSystem to None.

        Args: none
        """
        for item in self.items.values():
            item.special = None

    def calculate_price(self, name, qty):
        """Calculates the price for a given item and quantity.

        Computes price for a given item and quantity. If the item has a
        special applied, calculate_price will call calculate_special to
        determine the discount pricing. 

        Args:
            name: item name as string (e.g. 'soup')
            qty: float or int representing the number of units of the item
             to price

        Returns:
            A float representing the total price for {qty} units of an item
        """

        item = self.items[name]
        if item.special is None and item.markdown is None:
            return item.price * qty
        elif item.special is None and item.markdown is not None:
            return (item.price - item.markdown) * qty
        elif item.special is not None:
            params = item.special
            limit = params[-1]
            price = item.price
            if item.markdown is not None:
                price -= item.markdown
            if limit is not None and qty > limit: 
                return price * (qty-limit) + \
                    self.calculate_special(params, price, limit)
            else:
                return self.calculate_special(params, price, qty)



    def calculate_special(self, params, price, qty):
        """Calculates the special price for a given item and quantity.

        Args:
            params: array defining the parameters of the special
            price: float representing regular price of item in USD
            qty: float or int representing the number of units of the item
             to price

        Returns:
            A float representing the total price for {qty} units of an item
            with appropriate special applied. 
        """

        # N for X Special
        if params[0] == 2:
            N = params[1]
            X = params[2]
            if qty >= N:
                return (qty // N) * X + (qty % N) * price
            else:
                return price * qty

        # Buy N, Get M at X% off special
        if params[0] == 3:
            N = params[1]
            M = params[2]
            X = 1 - params[3] / 100

            if qty > N:
                total = 0
                m_price = price * X
                special_price = (N * price) + (M * m_price)
                
                special_count = qty // (N + M)
                total += special_count * special_price

                rem = qty % (N + M)
                if rem > N:
                    total += (N * price) + ((rem - N) * m_price)
                else:
                    total += rem * price
                return total
            else:
                return price * qty

class Order():
    """Creates a checkout session for scanning items and returning total.

    Attributes:
        scanned_items: a dictionary containing the scanned item and quantity.
          the item name is stored as the key; the quantity is stored as the
          value.
        __checkout_sys: required; a CheckoutSystem object to be used for 
          accessing item information and computing totals. This attribute is
          'private' and should not be accessed directly outside of class
          methods. 
        total: stores the current total price of the order. the total will
          update when new items are scanned/removed or the calculate_total
          function is called. otherwise, prices are considered 'locked in'.
          for example, if a special is added to an item and the total
          is requested, the special will not be applied unless an action is
          triggered to recalculate the total. 

    """
    def __init__(self, checkout_sys):
        self.scanned_items = {}
        self.__checkout_sys = checkout_sys
        self.total = 0

    def scan_item(self, name, qty=1):
        """Adds an item to the order and recalculates total

        Args:
            name: item name as a string (e.g. 'soup')
            qty: optional; float or int representing the amount of the item 
              being purchased in its 'soldBy' field. for items sold by unit,
              an integer value must be provided for qty
        Raises:
            KeyError if item name does not exist in checkout_sys
        """

        if name in self.scanned_items:
            self.scanned_items[name] += qty
        else:
            item = self.__checkout_sys.items[name]
            if item.soldBy == 'unit' and not isinstance(qty, int):
                raise ValueError('Qty for unit item must be an integer')
            else:
                self.scanned_items[name] = qty

        self.calculate_total()

    def remove_item_qty(self, name, qty=1):
        """Removes an item from the order and recalculates total

        Args:
            name: item name as a string (e.g. 'soup')
            qty: optional; float or int representing the amount of the item
              being purchased in its 'soldBy' field. for items sold by unit,
              an integer value must be provided for qty
              
        Raises:
            ValueError if item name not in order
        """

        if name not in self.scanned_items:
            raise ValueError("Item not in order")
        else:
            item = self.__checkout_sys.items[name]
            if item.soldBy == 'unit' and not isinstance(qty, int):
                raise ValueError('Qty must be integer value for item sold by unit')
            elif qty >= self.scanned_items[name]:  # allow larger qty
                self.scanned_items.pop(name)
            else:
                self.scanned_items[name] -= qty

        self.calculate_total()
    
    def calculate_total(self):
        """Calculates total of items in scanned_items.

        Calculate_total calls the CheckoutSytem method calculate_price() and
        sums the prices for each item name/qty pair stored in scanned_items.
        The class attribute total is then updated with the new value. 

        Args: None
        """
        newTotal = 0
        for k, v in self.scanned_items.items():
            newTotal += self.__checkout_sys.calculate_price(k, v)
        self.total = newTotal

    def return_total(self):
        """Returns current order total"""
        return self.total

    
          
          

