import sqlite3
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
conn=sqlite3.connect("LaptopData.db")
df=pd.read_sql("select * from laptop_techno",conn)
cols=st.columns(4)
for i,row in df.iterrows():
    with cols[i%4]:
        st.image(row["image_url"])
        st.write(row["description"])
        st.write(row["price"])
        st.link_button("View",row["link"])
        

st.set_page_config(page_title="Mobile Scraper", layout="wide")

st.title("Mobile Products")
st.write("Etelaat mobile haye Technolife")

conn = sqlite3.connect("LaptopData.db")

df = pd.read_sql_query(
    "SELECT title, description, brand, storage, ram, color, rating, link FROM mobile_techno",
    conn
)

conn.close()

if df.empty:
    st.warning("Hich mahsooli peyda nashod. Aval scraper ra ejra kon.")
else:
    search = st.text_input("Jostجو bar asas name mobile")

    if search:
        df = df[df["title"].str.contains(search, case=False, na=False)]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "link": st.column_config.LinkColumn("Link mahsool")
        }
    )

    st.subheader("Mahsoolat")

    for _, row in df.iterrows():
        with st.container(border=True):
            st.subheader(row["title"])
            st.write("Tozih:", row["description"])
            st.write("Brand:", row["brand"])
            st.write("Hafeze:", row["storage"])
            st.write("RAM:", row["ram"])
            st.write("Rang:", row["color"])
            st.write("Emtiaz:", row["rating"])

            if row["link"]:
                st.link_button("Moshaahede mahsool", row["link"])
        
        