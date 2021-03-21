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


if __name__ == '__main__':
    unittest.main()