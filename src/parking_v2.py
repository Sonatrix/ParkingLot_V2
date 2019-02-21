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

    def status(self):
        """Method to get nearest parking lot
        """
        try:
            print("Slot No\tRegistration No\tColour")
            with self.conn.cursor() as cursor:
                # Read a single record
                sql = "SELECT `slot_no`, `reg_no`, `color`  FROM `car_lot`"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                for parking in result:
                    print("{slot_no}\t{reg_no}\t{color}".format(**parking))

                return result
        except Exception as ex:
            print(f"Error while executing query {ex}")
    
    def create_parking_lot(self, no_of_slots):
        """This method will create parking lot if not present already with given
        number of slots.
        Input: no_of_slots - Integer Type
        """
        self.clear_parking_lot()

        no_of_slots = int(no_of_slots)

        if no_of_slots > 0:
            for i in range(1, no_of_slots+1):
                self.create_parking(slot_no=i,
                                    is_available=True)
            print(f"Created a parking lot with {no_of_slots} slots")
            return True
        else:
            print("Invalid slot number is provided. Please enter valid slot number")
        return

    def create_parking(self, reg_no=None, color=None, is_available=True, slot_no=None):
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
    
    def get_nearest_available_slot(self):
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
                reg_nos = " ".join([i['reg_no'] for i in result]) if result is not None else None
                print(reg_nos)
                return reg_nos

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
                slot_nos = " ".join([str(i['slot_no']) for i in result]) if result is not None else "Not Found"
                print(slot_nos)
                return slot_nos

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
                result = cursor.fetchone()
                slot_no = result['slot_no'] if result is not None else "Not Found"
                print(slot_no)
                return slot_no
        
        except Exception as ex:
            print(f"Error in executing query {ex}")

    def park(self, reg_no, color):
        """Method to allocate parking for car
        Input: color - String Type
        Input: reg_no - String Type
        """

        if not self._do_primary_checks():
            return
        else:
            available_slot = self.get_nearest_available_slot()
            if available_slot is None:
                print("Sorry, parking lot is full")
                return "Sorry, parking lot is full"

            try:
                with self.conn.cursor() as cursor:
                    # update details of parking
                    sql = "UPDATE car_lot SET `reg_no`=%s, `is_available`= %s, `color`=%s WHERE `slot_no`=%s"
                    cursor.execute(sql, (reg_no, False, color, available_slot))
                    print(f"Allocated slot number: {available_slot}")
                    return f"Allocated slot number: {available_slot}"
                self.conn.commit()

            except Exception as ex:
                print(f"Error in executing query {ex}")
                return f"Error in executing query {ex}"

    def leave(self, slot_no):
        """Method to deallocate parking for car
        Input: slot_no - String Type
        """
        if self.conn is None:
            print("No Connection exist")
            return
        else:
            try:
                with self.conn.cursor() as cursor:
                    # update details of parking
                    sql = "UPDATE car_lot SET `reg_no`=%s, `is_available`= %s, `color`=%s WHERE `slot_no`=%s"
                    cursor.execute(sql, ("", True, "", slot_no))
                self.conn.commit()
                print(f"Slot number {slot_no} is free")

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
# connect.status()
# connect.create_parking_lot(4)
# connect.park("ABDSFC", "White")
# connect.park("ABDSFC1","Blue")
# connect.park("ABDSFC2", "White")
# connect.leave(2)
# connect.park("ABDSFC4", "White")
# connect.status()
# connect.registration_numbers_for_cars_with_color("White")
# connect.slot_numbers_for_cars_with_color("White")
# connect.slot_number_for_registration_number("ABDSFC2")
# connect.close_connection()