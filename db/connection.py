from errno import errorcode
import os
from dotenv import load_dotenv
import mysql.connector 


# Load the stored environment variables
load_dotenv()

# Obtain connection string information from the portal
config = {
  'host': os.getenv('HOST_MYSQL'),
  'user': os.getenv('USER_MYSQL'),
  'password':os.getenv('PASSWORD_MYSQL'),
  'database':os.getenv('DATABASE_MYSQL'),
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor(dictionary=True)