import modules.database as db

try :
    db.initial_table_creation()

except Exception as e :
    print("Error : ", e)