import unittest
import os
import env
from src import parking

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

class TestParkingLot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parking = parking.Connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        cls.conn = cls.parking.get_conn()
        cls.allocated_slot = 1

    def test_a_create_parking_lot(self):
        parking_slots = 1
        mess = self.parking.create_parking_lot(parking_slots)
        self.assertEqual(mess, True, msg="Wrong parking lot created")

    def test_b_park(self):
        reg_no = "MH12FF2017"
        color = "Black"
        self.parking.park(reg_no, color)
        self.assertFalse(self.parking.get_nearest_available_slot(), msg="Park failed.")

    def test_c_leave(self):
        isTrue = self.parking.leave(self.allocated_slot)
        self.assertTrue(isTrue, msg="Leave failed.")

    @classmethod
    def tearDownClass(cls):
        cls.parking.close_connection()

if __name__ == '__main__':
    unittest.main()
