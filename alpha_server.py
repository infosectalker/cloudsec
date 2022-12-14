#!/usr/bin/env python3
import mysql.connector
import socket
import sys
import select

def initiate_db_connection(user_name, password, host_name):
    try:
        cnx = mysql.connector.connect(user=user_name,
                                    password=password,
                                    host=host_name)
        print("MySQL connection succeeded.\n")
        return cnx
    except mysql.connector.Error as err:
        print("MySQL connection error %s" %str(err))

def close_db_connection(cnx):
    try:
        cnx.close()
        print("Database connection closed successfully.\n")
    except mysql.connector.Error as err:
        print("Error closing db connection %s" %str(err))
        sys.exit(1)

def db_execute(cnx,sql,select=False):
    try:
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql)
        if select:
            response = cursor.fetchall()
            print("Select query executed successfully.\n")
            return response
        else:
            cnx.commit()
            print("Update or Insert query executed successfully.\n")

    except mysql.connector.Error as err:
        print("Error executing query %s" %str(err))
        sys.exit(1)

def update_database(node_name,attempt_count):
    db_user = '{{ mysql_username  }}'
    db_password = '{{ mysql_password  }}'
    db_name = 'ssh_access_reports'
    db_host = 'localhost'
    db_table = 'report'

    print("Connecting to mysql.")
    connection = initiate_db_connection(db_user,db_password,db_host)

    print("Creating databse if not existing.")
    query = 'CREATE DATABASE IF NOT EXISTS %s' %db_name
    db_execute(connection,query)

    print("Creating table if not existing.")
    query = 'CREATE TABLE IF NOT EXISTS %s.%s ( ID int(16) NOT NULL AUTO_INCREMENT, NodeName varchar(255), AttemptCount int, PRIMARY KEY (ID) );' %(db_name, db_table)
    db_execute(connection,query)

    print("Checking if %s exist in the database" %node_name)
    query = 'SELECT COUNT(*) FROM %s.%s WHERE NodeName = "%s"' %(db_name,db_table,node_name)
    response = db_execute(connection,query,True)
    for row in response:
        host_exist = row[0]
        break
    if host_exist == 0:
        print("Inserting data data.")
        query = 'INSERT INTO %s.%s (NodeName, AttemptCount) VALUES ("%s", %d);' %(db_name, db_table, node_name,attempt_count)
        db_execute(connection,query)
    else:
        print("Updating data data.")
        query = 'UPDATE %s.%s SET AttemptCount = AttemptCount+%d WHERE NodeName="%s";' %(db_name, db_table, attempt_count, node_name)
        db_execute(connection,query)
    print("Closing database connection.")
    close_db_connection(connection) 

def main():
    HOST = '127.0.0.1'   
    PORT = {{ server_port }}
 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
 
    try:
        s.bind((HOST, PORT))
    except socket.error as err:
        print('Bind failed. Error Code : ' + str(err[0]) + ' Message ' + err[1])
        sys.exit()
     
    print('Socket bind complete')
    s.listen(5)

    print('Socket now listening')
 
    while 1:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                attempt = int(client.recv(4096))
                client_ip = addr[0]
                update_database(client_ip,attempt)
        except KeyboardInterrupt:
            print()
            print("Keyboard Interrupt. Exiting.")
            break
        except socket.error as msg:
            print("Socket closed %s" % str(msg))
            break
    s.close()
    
if __name__ == "__main__":
    main()
