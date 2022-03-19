import unittest
import innova_factory_store as ifs
import util as u
import testutil as tu

class TestIFS(unittest.TestCase):
    def test_get_posts(self):
        featured = u.get_prev_featured(site_key)
        no_new_drops = u.get_new_drops(featured, featured, ifs.get_disc_info)
        self.assertFalse(bool(no_new_drops))
        prev_featured = ts.simulate_new_drop(featured)
        new_drops = u.get_new_drops(prev_featured, featured, ifs.get_disc_info)
        self.assertEqual(len(new_drops.keys()), 1)
