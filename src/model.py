#################################################
# Imports
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Class variables
#################################################
__base_db_path = "sqlite:///hawaii.sqlite"
#################################################
# new and init
#################################################

# new setup session factory.

# A Egine class to create engine to be used. 
class Engine:   
      
    # init method or constructor    
    def __init__(self, ref):   
        self.engine = create_engine(ref)
        # try using ref if it does not work use the base path
      
    # Get the sql alchemy engine   
    def get_engine(self):   
        return self. engine