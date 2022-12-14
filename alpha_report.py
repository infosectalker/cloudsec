#!/usr/bin/env python3
import mysql.connector
import sys
import alpha_server

def main():
    db_user = '{{ mysql_username  }}'
    db_password = '{{ mysql_password  }}'
    db_name = 'ssh_access_reports'
    db_host = '{{ server_address  }}'
    db_table = 'report'

    print("Connecting to mysql.")
    connection = alpha_server.initiate_db_connection(db_user,db_password,db_host)

    print("Getting data from database")
    query = 'SELECT * FROM %s.%s' %(db_name,db_table)
    response = alpha_server.db_execute(connection,query,True)
    print(" -----------------------------------------")
    print("| Simple Metrics for ssh log-in attempts |")
    print("|----------------------------------------|")
    for row in response:
        print("| * %s had %d attempt" %(row[1],row[2]))

    print(" ----------------------------------------")

if __name__ == "__main__":
    main()
