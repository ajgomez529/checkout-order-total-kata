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

    # update price of nonexistant item produces KeyError
    def test_update_price_no_item(self):
        self.assertRaises(KeyError, self.co_sys.update_price, 'dfsd', 1.50)
    
class MarkdownTest(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
        self.co_sys.register_item('onion', 1.00, 'lbs')
        self.co_sys.register_item('soda', 1.00)

    # add markdown 
    def test_add_markdown_no_limit(self):
        self.co_sys.markdown('soda', 0.50)
        item = self.co_sys.items['soda']
        self.assertEqual(item.markdown, 0.50)

    # calculate price w/ markdown, unit item
    def test_calc_markdown_no_limit(self):
       self.co_sys.markdown('soda', 0.50)
       self.assertEqual(self.co_sys.calculate_price('soda', 20), 10.00)
    
    # calculate price w/ markdown, weighed item
    def test_calc_markdown_weight(self):
        self.co_sys.markdown('onion', 0.50)
        self.assertEqual(self.co_sys.calculate_price('onion', 1.50), 0.75)
    
    # ValueError if markdown is less than 0
    def test_negative_markdown(self):
        self.assertRaises(ValueError, self.co_sys.markdown, 'onion', -0.50)
    
    # ValueError if markdown is greater than item price
    def test_too_large_markdown(self):
        self.assertRaises(ValueError, self.co_sys.markdown, 'onion', 1.50)

    # KeyError if item does not exist
    def test_markdown_no_item(self):
        self.assertRaises(KeyError, self.co_sys.markdown, 'onion1', 2.00)
    
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

    # KeyError if no item
    def test_NforX_no_item(self):
        self.assertRaises(KeyError, self.co_sys.NforX, "pop", 4, 3, 4)

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
    
    # calc special, qty < N
    def test_calc_buyNMX_low_qty(self):
        self.co_sys.buyNgetMatXoff('soda', 10, 10, 100)
        self.assertEqual(self.co_sys.calculate_price('soda', 9), 9.00)

    # KeyError if no item
    def test_buyNMX_no_item(self):
        self.assertRaises(KeyError, self.co_sys.buyNgetMatXoff, "pop", 10, 10, 100)


class OrderTest(unittest.TestCase):
    def setUp(self):
        self.co_sys = checkout.CheckoutSystem()
        self.co_sys.register_item('onion', 1.00, 'lbs')
        self.co_sys.register_item('soda', 1.00)
        self.order = checkout.Order(self.co_sys)

    # scan unit item
    def test_scan_item(self):
        self.order.scan_item('soda')
        self.assertEqual(self.order.scanned_items['soda'], 1)
    
    # ValueError if scanning unit item with non int value
    def test_scan_unit_item_bad_qty(self):
        self.assertRaises(ValueError, self.order.scan_item, 'soda', 1.5)
    
    # scan unit item in integer qty > 1
    def test_scan_many_unit_items(self):
        self.order.scan_item('soda')
        self.order.scan_item('soda', 2)
        self.assertEqual(self.order.scanned_items['soda'], 3)
    
    # KeyError if item not in CheckoutSystem
    def test_scan_bad_item_name(self):
        self.assertRaises(KeyError, self.order.scan_item, 'pepsi', 1)
    
    # scan weighed item
    def test_scan_weighed_item(self):
        self.order.scan_item('onion', 4.5)
        self.assertEqual(self.order.scanned_items['onion'], 4.5)
    
    # remove item
    def test_remove_item(self):
        self.order.scan_item('onion', 2.5)
        self.order.remove_item_qty('onion', 1)
        self.assertEqual(self.order.scanned_items['onion'], 1.5)

    # ValueError if attempting to remove item not in cart
    def test_remove_no_item(self):
        self.assertRaises(ValueError, self.order.remove_item_qty, 'pop', 1)
    
    # calculate single item total
    def test_item_total(self):
        self.order.scan_item('onion', 4.5)
        self.assertEqual(self.order.return_total(), 4.50)
    
    # calculate multi item total
    def test_multi_item_total(self):
        self.order.scan_item('soda')
        self.order.scan_item('soda')
        self.order.scan_item('onion', 4.5)
        self.assertEqual(self.order.return_total(), 6.50) 
        
    # ValueError if removing unit item in non-integer value
    def test_remove_unit_item_bad_qty(self):
        self.assertRaises(ValueError,self.order.remove_item_qty, "soda", 1.5)

 


            
if __name__ == '__main__':
    unittest.main()