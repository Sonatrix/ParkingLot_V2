CREATE TABLE `car_lot` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `color` varchar(25),
  `reg_no` varchar(25),
  `is_available` BOOLEAN,
  `slot_no` INT(1)
);
