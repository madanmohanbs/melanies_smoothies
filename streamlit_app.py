# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw:  Customize your Smoothies")
st.write(
  """
  **Choose your fruits in your Smooties** .
  """
)

name_of_order = st.text_input('Order Name')
st.write('Name of order: '+ name_of_order)


#session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingrediants = st.multiselect('Choose upto 5 fruits',my_dataframe,max_selections=5)
if ingrediants:
    #st.write(ingrediants)
    #st.text(ingrediants)
    
    ingredients_string=''
    for fruit in ingrediants:
        ingredients_string += fruit+ ' '
        
    st.write(ingredients_string) 

    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients,name_on_order)
            values ('{ingredients_string}','{name_of_order}')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
    #st.write(my_insert_stmt)
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!'+name_of_order, icon="✅")
