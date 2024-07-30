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
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect(
    "Choose upto 5 ingredients", 
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(fruityvice_response.json() , use_container_width=True)
        #st.write (ingredients_string)
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_Order)
                 values ('""" + ingredients_string + """','"""+Name_on_Order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered, ' + Name_on_Order + '!', icon="✅")
    import requests
    
   
    
