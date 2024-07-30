# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)
Name_on_Order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be",Name_on_Order )
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_List = st.multiselect(
    "Choose upto 5 Ingredients", 
    my_dataframe
)
if Ingredients_List:
   Ingredients_string=''
for fruit_chosen in Ingredients_List:
    Ingredients_string += fruit_chosen

#st.write (Ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_Order)
                 values ('""" + Ingredients_string + """','"""+Name_on_Order+"""')"""

st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
   session.sql(my_insert_stmt).collect()
   st.success('Your Smoothie is ordered, ' + Name_on_Order + '!', icon="✅")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
