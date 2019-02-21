import pymysql.cursors
#from settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

class Connection(object):
    """
       This class provides the database connection methods
    """
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.port = DB_PORT
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = pymysql.connect(host = self.host,
                                        port = self.port,
                                        db = self.name,
                                        user = self.user,
                                        passwd = self.password,
                                        cursorclass=pymysql.cursors.DictCursor)
        return self.conn
    
    def _do_primary_checks(self):
        if self.conn is None:
            print("Parking Lot not created")
            return False
        return True

    def get_parking_status(self):
        """Method to get nearest parking lot
        """
        try:
            with self.conn.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `reg_no`, `color`, `slot_no` FROM `car_lot`"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as ex:
            print(f"Error while executing query {ex}")

    def create_parking_lot(self, reg_no=None, color=None, is_available=True, slot_no=None):
        """Method to create parking lot
            Input: colour - String Type optional
            Input: reg_no - String Type optional
            Input: slot_no - Integer Type
        """
        if slot_no is None:
            print("Invalid Slot Number")
            return

        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO `car_lot` (`reg_no`, `color`, `is_available`, `slot_no`) VALUES (%s, %s, True, %s)"
                cursor.execute(sql, (reg_no, color, slot_no))
            self.conn.commit()
            return True
        except Exception as ex:
            return False
            print(f"Error while executing query {ex}")
    
    def get_next_available_slot(self):
        """Method to get nearest parking lot
        """
        if self.conn is None:
            print("No Connection available")

        try:
            with self.conn.cursor() as cursor:
                # get the first record where slot is available
                sql = "SELECT `id`, `slot_no` FROM `car_lot` WHERE `is_available`=%s ORDER BY slot_no ASC limit 1"
                cursor.execute(sql, (True,))
                result = cursor.fetchone()

                slot_no = result.get("slot_no", None) if result is not None else None
                print(slot_no)
                return slot_no

        except Exception as ex:
            print(f"Error in executing query {ex}")

    def registration_numbers_for_cars_with_color(self, color):
        """Method to find registration numbers for cars with given color in
        parking.
        Input: color - String Type
        """
        if not self._do_primary_checks():
            return

        try:
            with self.conn.cursor() as cursor:
                # get the first record where slot is available
                sql = "SELECT `reg_no` FROM `car_lot` WHERE `color`=%s and `is_available`=%s"
                cursor.execute(sql, (color, False))
                result = cursor.fetchall()
                reg_nos = result if result is not None else None
                print(result)
                return result

        except Exception as ex:
            print(f"Error in executing query {ex}")

    def slot_numbers_for_cars_with_color(self, color):
        """Method to find slot numbers for cars with given color in
        parking.
        Input: color - String Type
        """
        if not self._do_primary_checks():
            return

        try:
            with self.conn.cursor() as cursor:
                # get the first record where slot is available
                sql = "SELECT `slot_no` FROM `car_lot` WHERE `color`=%s and `is_available`=%s"
                cursor.execute(sql, (color, False))
                result = cursor.fetchall()
                slot_nos = result if result is not None else None
                print(result)
                return result

        except Exception as ex:
            print(f"Error in executing query {ex}")

    def slot_number_for_registration_number(self, reg_no):
        """Method to find slot numbers for cars with given registration number in
        parking.
        Input: reg_no - String Type
        """
        if not self._do_primary_checks():
            return

        try:
            with self.conn.cursor() as cursor:
                # get the first record where slot is available
                sql = "SELECT `slot_no` FROM `car_lot` WHERE `reg_no`=%s"
                cursor.execute(sql, (reg_no))
                result = cursor.fetchall()
                slot_no = result if result is not None else None
                print(result)
                return result

        except Exception as ex:
            print(f"Error in executing query {ex}")

    def allocate_parking_lot(self, slot_no=None, reg_no=None, color=None):
        """Method to allocate parking for car
        Input: colour - String Type
        Input: slot_no - Integer Type
        Input: reg_no - String Type
        """

        if self.conn is None or slot_no is None:
            print("please try again")
            return
        else:
            try:
                with self.conn.cursor() as cursor:
                    # update details of parking
                    sql = "UPDATE car_lot SET `reg_no`=%s, `is_available`= %s, `color`=%s WHERE `slot_no`=%s"
                    cursor.execute(sql, (reg_no, False, color, slot_no))
                self.conn.commit()

            except Exception as ex:
                print(f"Error in executing query {ex}")

    def deallocate_parking_lot(self, reg_no):
        """Method to deallocate parking for car
        Input: reg_no - String Type
        """
        if self.conn is None:
            print("No Connection exist")
            return
        else:
            try:
                with self.conn.cursor() as cursor:
                    # update details of parking
                    sql = "UPDATE car_lot SET `reg_no`=%s, `is_available`= %s, `color`=%s WHERE `reg_no`=%s"
                    cursor.execute(sql, ("", True, "", reg_no))
                self.conn.commit()

            except Exception as ex:
                print(f"Error in executing query {ex}")
    
    def clear_parking_lot(self):
        """Method to clear parking lot
        """
        if self.conn is None:
            print("No Connection exist")
            return
        else:
            try:
                with self.conn.cursor() as cursor:
                    # update details of parking
                    sql = "delete from car_lot"
                    cursor.execute(sql)
                self.conn.commit()

            except Exception as ex:
                print(f"Error in executing query {ex}")


    def close_connection(self):
        self.conn.close()


# connect = Connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
# conn = connect.get_conn()
# connect.get_parking_status()
# connect.clear_parking_lot()
# connect.create_parking_lot(slot_no=1)
# connect.create_parking_lot(slot_no=2)
# connect.create_parking_lot(slot_no=3)
# connect.create_parking_lot(slot_no=4)
# connect.allocate_parking_lot(reg_no="ABDSFC", color="White", slot_no=1)
# connect.allocate_parking_lot(reg_no="ABDSFC1", color="Blue", slot_no=2)
# connect.allocate_parking_lot(reg_no="ABDSFC2", color="White", slot_no=3)
# connect.deallocate_parking_lot("ABDSFC1")
# slot_available = connect.get_next_available_slot()
# if slot_available is None:
#     print("No slot is found")
# else:
#     print(slot_available)
#     connect.allocate_parking_lot(reg_no="ABDSFC4", color="White", slot_no=slot_available)
# #connect.get_parking_status()
# connect.registration_numbers_for_cars_with_color("White")
# connect.slot_numbers_for_cars_with_color("White")
# connect.slot_number_for_registration_number("ABDSFC2")
# connect.close_connection()