import os
from doten.v import load_dotenv
from sqlalchemy import create_engine,select,insert,update,delete,func
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship,sessionmaker,declarative_base
import pandas as pd
import math

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


database_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(database_url)

Base=declarative_base()

#Model of Student table
class Student(Base): 
    __tablename__='student_details' 
    
    sid=Column(Integer,primary_key=True) 
    roll_no=Column(Integer,unique=True,nullable=False) 
    first_name=Column(String(15),nullable=False) 
    last_name=Column(String(15),nullable=False) 
    phone_no=Column(String(10),nullable=False) 
    
    std = relationship('Result',back_populates='res')

#Model of Result table
class Result(Base):
    __tablename__='result'
    
    rid=Column(Integer,primary_key=True)
    sid=Column(Integer,ForeignKey('student_details.sid'),unique=True,nullable=False)
    maths=Column(Integer,nullable=False)
    physics=Column(Integer,nullable=False)
    chemistry=Column(Integer,nullable=False)
    
    
    res=relationship('Student',back_populates='std')


Base.metadata.create_all(engine)

SessionLocal=sessionmaker(bind=engine)
session=SessionLocal()


def view(name): #Function to see table records
    if name=='Student':
        stmt=select(Student)
    elif name=='Result':
        stmt=select(Result)
    else:
        print("Table not available!")
        return
    
    result=session.execute(stmt)
    users=result.scalars().all()

    print("All users:")
    for o in result:
        print(o)
    data=[{c.name:getattr(user,c.name) for c in users[0].__table__.columns}for user in users]
    # print(data)
    df=pd.DataFrame(data,columns=users[0].__table__.columns.keys())
    df = df.reset_index(drop=True)
    print(df)
  
def insert(name):    #For inserting record in table  
    while True:
        global session
        print("\n1. Add Record")
        print("2. To go back")
        choice=input("Enter index of your choice: ")
        if choice=='2':
            return
        else:
            try:
                if(name=='Student'):
                    roll=int(input("Enter roll_no: "))
                    fn=input("Enter First name: ")
                    ln=input("Enter Last name: ")
                    phone=input("Enter Phone number: ")
                    record=Student(roll_no=roll,first_name=fn,last_name=ln,phone_no=phone)
                    session.add(record)
                    session.commit()
                elif(name=='Result'):
                    student_id=int(input("Enter student id: "))
                    m=int(input("Enter Maths marks: "))
                    p=int(input("Enter Physics marks: "))
                    c=int(input("Enter Chemistry marks: "))
                    record=Result(sid=student_id,maths=m,physics=p,chemistry=c)
                    session.add(record)
                    session.commit()
            except Exception as e:
                print(f"Error occured: {e}")
                session.rollback()

def update_result():    #For doing update in result table
    global session
    while True:
        print("\n1. Maths")
        print("2. Physics")
        print("3. Chemistry")
        print("4. To go back")
        choice=input("Enter your choice: ")
        if choice=='4':
            break
        
        try:
            if choice=='1':
                sid=int(input("Enter sid: "))
                value=int(input("\nEnter value: "))
                stmt=update(Result).where(Result.sid==sid).values(maths=value)
                session.execute(stmt)
                session.commit()
            elif choice=='2':
                sid=int(input("Enter sid: " ))
                value=int(input("\nEnter value: "))
                stmt=update(Result).where(Result.sid==sid).values(physics=value)
                session.execute(stmt)
                session.commit()
            elif choice=='3':
                sid=int(input("Enter sid: "))
                value=int(input("\nEnter value: "))
                stmt=update(Result).where(Result.sid==sid).values(chemistry=value)
                session.execute(stmt)
                session.commit()
            else:
                continue
        except Exception as e:
            print(f"Error occured: {e}")
            session.rollback()
        
        print("Record Updated Successfully")

def update_student():   #For doing update in student table
    global session
    while True:
        print("\n1. First name")
        print("2. Last name")
        print("3. Phone_no")
        print("4. To go Back")
        choice=input("Enter your choice: ")
        if choice=='4':
            break
        
        try:
            if choice=='1':
                value=input("\nEnter value: ")
                roll_no=int(input("Enter roll_no: "))
                stmt=update(Student).where(Student.roll_no==roll_no).values(first_name=value)
                session.execute(stmt)
                session.commit()
            elif choice=='2':
                value=input("\nEnter value: ")
                roll_no=int(input("Enter roll_no: "))
                stmt=update(Student).where(Student.roll_no==roll_no).values(last_name=value)
                session.execute(stmt)
                session.commit()
            elif choice=='3':
                value=input("\nEnter value: ")
                roll_no=int(input("Enter roll_no: "))
                stmt=update(Student).where(Student.roll_no==roll_no).values(phone_no=value)
                session.execute(stmt)
                session.commit()
            else:
                continue
        except Exception as e:
            print(f"Error occured: {e}")
            session.rollback()
        print("Record updated successfully")
        
def delete_student():  #For deleting record in student table
    global session
    while True:
        print("\n1. Delete")
        print("2. To go back")
        choice=input("Enter index of your choice: ")
        if choice=="1":
            roll_no=int(input("Enter roll_no: "))
            try:
                stmt=delete(Student).where(Student.roll_no==roll_no)
                session.execute(stmt)
                session.commit()
            except Exception as e:
                print(f"Error occured: {e}")
                session.rollback()
            print("Record Deleted successfully")
        elif choice=="2":
            break
        else:
            print("Enter valid choice")
            
def delete_result(): #for deleting record in result table
    global session
    while True:
        print("\n1. Delete")
        print("2. To go back")
        choice=input("Enter index of your choice: ")
        if choice=="1":
            sid=int(input("Enter sid: "))
            try:
                stmt=delete(Result).where(Result.sid==sid)
                session.execute(stmt)
                session.commit()
            except Exception as e:
                print(f"Error occured: {e}")
                session.rollback()
            print("Record Deleted successfully")
        elif choice=="2":
            break
        else:
            print("Enter valid choice")    
            


def operation(name): #Selecting operation on table
    while True:
        print("\nOperations")
        print("1. View")
        print("2. Insert")
        print("3. Update")
        print("4. Delete")
        print("5. To go back")
        choice=input("Enter index of your choice: ")
        match choice:
            case '1':
                view(name)
            case '2':
                insert(name)
            case '3':
                if name=='Student':
                    update_student()
                elif name=="Result":
                    update_result()
                else:
                    print("Unable to do operation on table")
            case '4':
                if name=="Student":
                    delete_student()
                elif name=="Result":
                    delete_result()
                else:
                    print("Unable to do this operation on table")
            case '5':
                return
            case _:
                print("Enter valid choice!")
                
                
def student_results(): #To see studen name and its result using join query
    global session
    stmt=select(func.count(func.distinct(Student.sid)))
    count=session.execute(stmt).scalar()
    total_page=math.ceil(count/10)
    print(total_page)
    current_page=1
    while True:
        offset=(current_page-1)*10
        stmt=select(Student.roll_no,Student.first_name,Student.last_name,Result.maths,Result.physics,Result.chemistry).join(Result,Student.sid==Result.sid).limit(10).offset(offset).order_by(Student.roll_no)
        data = session.execute(stmt).mappings().all()
        df=pd.DataFrame(data,columns=['roll_no','first_name','last_name','maths','physics','chemistry'])
        print(df)
        if(current_page==1):
            print("1.Next Page")
            print("2.To go back")
            choice=input("Enter index of your choice: ")
            if choice=='1':
                current_page+=1
            elif choice=='2':
                break
            else:
                print("Please enter a valid choice")
        elif(1<current_page<total_page):
            print("1.Next Page")
            print("2.Prev page")
            print("3.To go back")
            
            choice=input("Enter index of your choice: ")
            if choice=='1':
                current_page+=1
            elif choice=='2':
                current_page-=1
            elif choice=='3':
                break
            else:
                print("Please enter a valid choice")
        elif(current_page==total_page):
            print("1. Prev page")
            print("2. To go back")
            choice=input("Enter index of your choice: ")
            if choice=='1':
                current_page-=1
            elif choice=='2':
                break
            else:
                print("Please enter a valid choice")
        else:
            break

#Starting point of System
print("----Welcome to User Management System----\n")
while True:
    print("\n--Tables Available--")
    print("1.Student")
    print("2.Result")
    print("4.Show Student Results")
    print("3.Exit")
    choice= input("Enter index of your choice: ")
    match  choice:
        case '1':
            operation('Student')
        case '2':
            operation('Result')
        case '4':
            student_results()
        case '3':
            break
        case _:
            print("Enter valid choice!")