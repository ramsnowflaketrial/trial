import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents are now healthy diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🍌Omega 3 & Blueberry Oatmeal')
streamlit.text('🥭Kale, Spinach & Rocket Smoothie')
streamlit.text('🥝Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        streamlit.write('The user entered ', fruit_choice)
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # write your own comment -what does the next line do? 
        #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
        back_from_function= get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()



streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor as my_cur:
        my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
        return my_cur.fetchall()

    if streamlit.button('Get fruit load list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_row = get_fruit_load_list()
streamlit.text("The Fruit Load List Contains:")
streamlit.dataframe(my_data_row)

streamlit.stop()
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_my_fruit)
my_cnx.cursor().execute("Insert into FRUIT_LOAD_LIST values (" +add_my_fruit +")" )

#sql = "Insert into FRUIT_LOAD_LIST values";
#my_cnx.cursor().execute(sql,add_my_fruit)
