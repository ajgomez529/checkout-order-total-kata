class Item:
    """Stores information for single item used in checkout

    Attributes:
        name: item name as string (e.g. 'soup').
        price: price in USD as float (e.g. 2.99).
        soldBy: how the item is sold as string (e.g. 'lbs').
        special: init as None; stores parameters for special savings on
          item. Only one special can be applied at a time.
    """

    def __init__(self, name, price, soldBy):
        self.name = name
        self.price = price
        self.soldBy = soldBy
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
        """

        self.items.pop(name)

    def update_price(self, name, price):
        """Updates price of an existing item

        Args:
            name: item name as string (e.g. 'soup').
            price: new price in USD as float (e.g. 2.99).
        """

        self.items[name].price = price

    def markdown(self, name, discount, limit=None):
        """Applies a markdown special to an existing item.

        When a markdown is applied to an item, the item price will be reduced
        by {discount}. The savings can be applied to a max of {limit} units.

        This function sets the Item class attribute 'special' for the named
        item to the following array: [1, discount, limit]
        The first entry, 1, identifies the type of special. 


        Args:
            name: item name as string (e.g. 'soup').
            discount: price reduction in USD as float (e.g. 0.50). Value
              should not exceed price of item.
            limit: Optional; int representing the maximum number of units the
              discount may be applied to
        """

        self.items[name].special = [1, discount, limit]

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
        """
        self.items[name].special = [3, N, M, X, limit]
    
    def remove_special(self, name):
        """Removes an existing special applied to an item.

        Args:
            name: item name as string (e.g. 'soup')
        """
        self.items[name].special = None

    def remove_all_specials(self):
        """Removes all specials applied to all items.

        Args: none
        """
        for item in self.items.values():
            item.special = None

    def calculate_price(self, name, qty):
        """Calculates the price for a given item and quantity.

        Computes price for a given item and quantity. If the item has a
        special applied, calculate_price will call calculate_special to
        determine the discount pricing

        Args:
            name: item name as string (e.g. 'soup')
            qty: float or int representing the number of units of the item
             to price

        Returns:
            A float representing the total price for {qty} units of an item
        """

        item = self.items[name]
        if item.special == None:
            return item.price * qty
        else:
            params = item.special
            limit = params[-1]
            if qty > limit: 
                return item.price * (qty-limit) + \
                    self.calculate_special(params, item.price, limit)
            else:
                return self.calculate_special(params, item.price, qty)



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
        # markdown special
        if params[0] == 1:
            discount = params[1]
            return (price - discount) * qty

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
            else:
                return price * qty
