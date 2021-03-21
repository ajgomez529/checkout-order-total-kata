import unittest
import checkout

class ItemSetUp(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
    
    # add weighted item and verify values
    def test_add_weighed_item(self):
        self.co_sys.register_item('steak', 7.99, 'lbs')
        item = self.co_sys.items['steak']
        self.assertEqual(item.name, 'steak')
        self.assertEqual(item.price, 7.99)
        self.assertEqual(item.soldBy, 'lbs')

    # add unit item and verify values
    def test_add_unit_item(self):
        self.co_sys.register_item('soup', 1.50)
        item = self.co_sys.items['soup']
        self.assertEqual(item.name, 'soup')
        self.assertEqual(item.price, 1.50)
        self.assertEqual(item.soldBy, 'unit')
    
    # add and remove item
    def test_remove_item(self):
        self.co_sys.register_item('soup', 1.50)
        self.co_sys.unregister_item('soup')
        self.assertEqual(self.co_sys.items.get('soup'), None)
    
    # attempt to remove nonexistant item produces KeyError
    def test_remove_nonexistant_item(self):
        self.assertRaises(KeyError, self.co_sys.unregister_item, 'ham')

    # set price then change price
    def test_price_update(self):
        self.co_sys.register_item('bread', 1.25)
        item = self.co_sys.items['bread']
        self.assertEqual(item.price, 1.25)
        self.co_sys.update_price('bread', 2.00)
        self.assertEqual(item.price, 2.00)

class MarkdownTest(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
        self.co_sys.register_item('onion', 1.00, 'lbs')
        self.co_sys.register_item('soda', 1.00)

    # add markdown with no limit (default = None)
    def test_add_markdown_no_limit(self):
        self.co_sys.markdown('soda', 0.50)
        item = self.co_sys.items['soda']
        self.assertEqual(item.special, [1, 0.50, None])
    
    # add markdown with limit
    def test_add_markdown_limit(self):
        self.co_sys.markdown('soda', 0.25, 5)
        item = self.co_sys.items['soda']
        self.assertEqual(item.special, [1, 0.25, 5])

    # calculate price w/ markdown, unit item, no limit
    def test_calc_markdown_no_limit(self):
       self.co_sys.markdown('soda', 0.50)
       self.assertEqual(self.co_sys.calculate_price('soda', 20), 10.00)
    
    # calculate price w/ markdown, unit item, limit
    def test_calc_markdown_limit(self):
        self.co_sys.markdown('soda', 0.50, 5)
        self.assertEqual(self.co_sys.calculate_price('soda', 10), 7.50)
    
    #calculate price w/ markdown, weighed item, no limit
    def test_calc_markdown_weight(self):
        self.co_sys.markdown('onion', 0.50)
        self.assertEqual(self.co_sys.calculate_price('onion', 1.50), 0.75)
    
    # calculate price w/markdown, weighed item, limit
    def test_calc_markdown_weight_limit(self):
        self.co_sys.markdown('onion', 0.50, 5)
        self.assertEqual(self.co_sys.calculate_price('onion', 7.50), 5.00)

class NforXTest(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
        self.co_sys.register_item('onion', 1.00, 'lbs')
        self.co_sys.register_item('soda', 1.00)

    # add NforX special, no limit
    def test_add_NforX_no_limit(self):
        self.co_sys.NforX('soda', 3, 2.00)
        item = self.co_sys.items['soda']
        self.assertEqual(item.special, [2, 3, 2.00, None])
    
    # add NforX special, limit
    def test_add_NforX_limit(self):
        self.co_sys.NforX('onion', 2, 1.50, 3)
        item = self.co_sys.items['onion']
        self.assertEqual(item.special, [2, 2, 1.50, 3])

    # calc price with NforX special, no limit
    def test_calc_NforX_no_limit(self):
        self.co_sys.NforX('soda', 3, 2.00)
        self.assertEqual(self.co_sys.calculate_price('soda', 10), 7.00)
    
    # calc price with NforX special, limit
    def test_calc_NforX_limit(self):
        self.co_sys.NforX('soda', 5, 3.50, 10)
        self.assertEqual(self.co_sys.calculate_price('soda', 15), 12.00)

    # calc weighed item price with NforX special, no limit
    def test_calc_NforX_weighed_no_limit(self):
        self.co_sys.NforX('onion', 2, 1.50)
        self.assertEqual(self.co_sys.calculate_price('onion', 5.5), 4.5)
    
    # calc weighed item price with NforX special, limit
    def test_calc_NforX_weighed_limit(self):
        self.co_sys.NforX('onion', 10, 5.00, 10)
        self.assertEqual(self.co_sys.calculate_price('onion', 20), 15.00)
    
    # calc NforX when qty < N
    def test_calc_NforX_low_qty(self):
        self.co_sys.NforX('soda', 4, 2.00)
        self.assertEqual(self.co_sys.calculate_price('soda', 2), 2.00)

class buyNgetMatXoffTest(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
        self.co_sys.register_item('onion', 1.00, 'lbs')
        self.co_sys.register_item('soda', 1.00)

    # add special, no limit
    def test_add_buyNMX_no_limit(self):
        self.co_sys.buyNgetMatXoff('soda', 1, 1, 100)
        item = self.co_sys.items['soda']
        self.assertEqual(item.special, [3, 1, 1, 100, None])

    # add special, limit
    def test_add_buyNMX_limit(self):
        self.co_sys.buyNgetMatXoff('soda', 1, 1, 100, 4)
        item = self.co_sys.items['soda']
        self.assertEqual(item.special, [3, 1, 1, 100, 4])
    
    # calc special, no limit
    def test_calc_buyNMX_no_limit(self):
        self.co_sys.buyNgetMatXoff('soda', 1, 1, 100)
        self.assertEqual(self.co_sys.calculate_price('soda', 10), 5.00)
    
    # calc special, limit
    def test_calc_buyNMX_limit(self):
        self.co_sys.buyNgetMatXoff('soda', 2, 2, 50, 8)
        self.assertEqual(self.co_sys.calculate_price('soda', 12), 10)

    # calc special, weighed item, no limit
    def test_calc_buyNMX_weighed_no_limit(self):
        self.co_sys.buyNgetMatXoff('onion', 2, 1, 50)
        self.assertEqual(self.co_sys.calculate_price('onion', 4.75), 4.25)

    # calc special, weighed item, limit
    def test_calc_buyNMX_weighed_limit(self):
        self.co_sys.buyNgetMatXoff('onion', 4, 4, 100, 16)
        self.assertEqual(self.co_sys.calculate_price('onion', 20), 12.00)
    
    #calc special, qty < N
    def test_calc_buyNMX_low_qty(self):
        self.co_sys.buyNgetMatXoff('soda', 10, 10, 100)
        self.assertEqual(self.co_sys.calculate_price('soda', 9), 9.00)

if __name__ == '__main__':
    unittest.main()