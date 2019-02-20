from sqlalchemy import *

db = create_engine('sqlite:///parking.db')

db.echo = False  # Try changing this to True and see what happens

metadata = BoundMetaData(db)
