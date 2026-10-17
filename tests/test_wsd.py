import unittest
from wsd_engine import inventory, disambiguate
class TestWSD(unittest.TestCase):
    def test_inventory(self):
        self.assertGreaterEqual(len(inventory('bank')['senses']),2)
    def test_financial_bank(self):
        self.assertEqual(disambiguate('She deposited money at the bank before going home.','bank')['best']['id'],'bank.n.01')
    def test_river_bank(self):
        self.assertEqual(disambiguate('The fisherman sat on the bank of the river.','bank')['best']['id'],'bank.n.02')
    def test_unknown(self):
        self.assertIsNone(disambiguate('The quasar is distant','quasar')['best'])
    def test_fallback(self):
        self.assertTrue(disambiguate('xyz bank abc','bank')['fallback'])
if __name__=='__main__': unittest.main()
