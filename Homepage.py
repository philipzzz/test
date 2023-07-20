import psycopg2
import streamlit as st
#import streamlit_authenticator as stauth

# Establish a connection to Postgresql Server

# Connect to the PostgreSQL database
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
cursor=conn.cursor()
print("Connection Established")

def create_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            Name TEXT NOT NULL,
            Email  TEXT NOT NULL
        )
        """
    )
    conn.commit()

# Create Streamlit App

def main():
    st.title("CRUD Operations With MySQL");

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Select an Operation",("Create","Read","Update","Delete"))
    # Perform Selected CRUD Operations
    if option=="Create":
        st.subheader("Create a Record")
        name=st.text_input("Enter Name")
        email=st.text_input("Enter Email")
        if st.button("Create"):
            sql= "insert into users(name,email) values(%s,%s)"
            val= (name,email)
            cursor.execute(sql,val)
            conn.commit()
            st.success("Record Created Successfully!!!")



    elif option=="Read":
        st.subheader("Read Records")
        cursor.execute("select * from users")
        result = cursor.fetchall()
        for row in result:
            st.write(row)



    elif option=="Update":
        st.subheader("Update a Record")
        id=st.number_input("Enter ID",min_value=1)
        name=st.text_input("Enter New Name")
        email=st.text_input("Enter New Email")
        if st.button("Update"):
            sql="update users set name=%s, email=%s where id =%s"
            val=(name,email,id)
            cursor.execute(sql,val)
            conn.commit()
            st.success("Record Updated Successfully!!!")




    elif option=="Delete":
        st.subheader("Delete a Record")
        id=st.number_input("Enter ID",min_value=1)
        if st.button("Delete"):
            sql="delete from users where id =%s"
            val=(id,)
            cursor.execute(sql,val)
            conn.commit()
            st.success("Record Deleted Successfully!!!")


if __name__ == "__main__":
    main()
