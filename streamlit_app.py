import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError #Is case snsitive

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list=pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list=my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#Create the repeatable code block (called a function)
def get_fruityvise_data(this_fruit_choice):
  fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else: 
      #streamlit.write('The user entered ', fruit_choice)
      #fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #streamlit.text(fruityvice_response.json()) #Just writes the JSON data to the screen
      #Take the JSON version of the response and normalize it. 
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #Output the normalized data to the screen as table
      #streamlit.dataframe(fruityvice_normalized)
      back_from_function = get_fruityvise_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except urlerror as e:
    streamlit.error()

streamlit.stop()


streamlit.header("The fuit load list contains:")
#snowflake replated functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        retrun mycur


#Add a button to load the fruit
if(streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

##Allow the end user to add a fruit to the fruit list
add_my_fruit = streamlit.text_input('What fruit would you like to add your fruit list?','Kiwi')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into  fruit_load_list values('from_stream_lit')")
