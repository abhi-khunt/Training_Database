import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()
host=os.getenv("DB_HOST")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_NAME")

#Database connection
try:
    mydb=mysql.connector.connect(
        host,
        user,
        password,
        database,
    )
    if mydb.is_connected():
        print("Database connected successfully")
except:
    print("Sorry! Connection Failed")

cursor=mydb.cursor()


cursor.execute("DELETE FROM user_details WHERE UID = 'UID0001'")
mydb.commit()

def delete(name,cols_name): #For deleting record from table
    global cursor
    status=True
    while status!=False:
        print("\n1.Delete")
        print("2.To go back")
        choice=input("Enter index number of your choice: ")
        match choice:
            case '1':
                print("\nWhich record you want to Delete")
                row=input(f"Enter Row ID {cols_name[0]}: ")
                try:
                    cursor.execute(f"DELETE FROM {name}  WHERE {cols_name[0]} = '{row}'")
                    mydb.commit()
                except mysql.connector.Error as err:
                    print("Something went wrong: {}".format(err))
                    mydb.rollback()
            case '2':
                status=False
            case _:
                print("Please Enter valid choice")
    
       
def update(name,cols_name): #For updating record in table
    global cursor
    status=True
    while True:
        print("\nNon Primary Column Names.")
        for i in range(1,len(cols_name)):
            print(i,".",cols_name[i])
        print(len(cols_name),"To go back")
        print("\nWhich field you want to make changes")
        col_no=int(input("Enter index number: "))
        if (col_no==len(cols_name)):
            break
        value=input("Enter new value: ")
        row=input(f"Enter Row ID {cols_name[0]}: ")
        try:
            cursor.execute(f"UPDATE {name} SET {cols_name[col_no]} = '{value}' WHERE {cols_name[0]} = '{row}'")
            mydb.commit()
        except mysql.connector.IntegrityError as e:
            print(f"Integrity Error : {e}")
            mydb.rollback()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            mydb.rollback()
            

def insert(name,cols_name): #For inserting record in table
    global cursor
    status=True
    while status!=False:
        print("\n1.Add Record")
        print("2.Go back")
        choice=int(input("Please Select Option"))
        match choice:
            case 1:
                record=[]
                for i in range(len(cols_name)):
                    value=input(f"Enter {cols_name[i]}: ")
                    record.append(value)
                colmuns=",".join(x for x in cols_name)
                placeholder=",".join("%s" for i in range(len(cols_name)))
                try:
                    sql=f"INSERT INTO {name} ({colmuns} ) Values ({placeholder})"
                    val=tuple(record)
                    cursor.execute(sql,val)
                    mydb.commit()
                except mysql.connector.IntegrityError as e:
                    print(f"Integrity Error occured: {e}")
                    mydb.rollback()
                except mysql.connector.Error as err:
                    print("Something went wrong: {}".format(err))
                    mydb.rollback()

            case 2:
                status=False
            case _:
                print("Please Select Correct Choice")
    

def view(name,cols_name): #For viewing records in table
    global cursor
    cursor.execute(f"SELECT * FROM {name}")
    result=list(cursor.fetchall())
    df=pd.DataFrame(result,columns=cols_name)
    print(df)


    
def table(name): #For choosing operation on table
    global cursor
    cursor.execute(f"SHOW COLUMNS FROM {name}")
    result=cursor.fetchall()
    cols_name=[x[0] for x in result]
    
    print(f"\nTable Selected : {name}")
    status =True
    while status!=False:
        print("\nPlease Choose Index of Operation")
        print("1.View")
        print("2.Insert")
        print("3.Update")
        print("4.Delete")
        print("5.To go back")
        choice=input()
        match choice:
            case '1':
                view(name,cols_name)
            case '2':
                insert(name,cols_name)
            case '3':
                update(name,cols_name)
            case '4':
                delete(name,cols_name)
            case '5':
                status=True
            case _:
                print("Please Enter Valid Choice")

def show_tables(): #For viewing and selecting table present in database
    cursor.execute("SHOW TABLES")
    tablelist=cursor.fetchall()
    
    status=True
    while status!=False:
        print("\n--Tables Available--")
        for i in range(len(tablelist)):
            print(i+1,".",tablelist[i][0])
        print(len(tablelist)+1,'.','To go Back')
        
        print("-Please Select The Index-")
        index=int(input())
        
        if(index == len(tablelist)+1):
            status=False
        else:
            table(tablelist[index-1][0])

def create_table(): #For creating table with limited functionalities
    global cursor
    print("Enter this datatypes only: INT, VARCHAR(12)")
    print("Enter this constraints only: NOT NULL")
    name=input("Enter the table name")
    num=int(input("Enter no. of Columns: "))
    field=[]
    for i in range(num):
        temp=[]
        temp.append(input("Enter column name: "))
        temp.append(input("Enter data type:"))
        temp.append(input("Enter the constraint:"))
        str=" ".join(temp)
        field.append(str)
    schema=",".join(x for x in field)
    primary=input("Please Enter the field you want to make Primary Key")
    try:
        sql=f"CREATE TABLE {name} ({schema},PRIMARY KEY({primary}))"
        print(sql)
        cursor.execute(sql)
        mydb.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
            
#Starting point of the system
print("---- Welcome to User Management System ----")
status=True
while status!=False:
    print("\n Main Menu")
    print("1.Tables Available")
    print("2.Create Table")
    print("3.Enter \'Exit\' to exit the system")
    choice=str(input("Enter Your Choice: "))
    match choice:
        case '1':
            show_tables()
        case '2':
            create_table()
        case 'Exit':
            status=False
        case _:
            print("Please Enter a valid choice")
