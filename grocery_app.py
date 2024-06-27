import cohere
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from utils import get_nutrient_info, generate_idea_v2, generate_name, validate_nutrition
import time

# The front end code starts here

st.title("Cuisine Idea Generator")

form = st.form(key="user_settings")
with form:
  st.write("Enter a description of what you're feeling [Example: Light seasoned southern food, Japanese style, anything with beef] ")
  # User input - Industry name
  appetite_input = st.text_input("Cuisine Idea", key = "appetite_input")
  tdee = st.number_input("Total Daily Energy Expenditure (TDEE) in calories", min_value=1000, max_value=5000, value=2000)
  goal = st.selectbox("Physique Goal", ["Cutting", "Maintenance", "Bulking"])
  num_meals = st.number_input("Number of meals to prep", min_value=1, max_value=10, value=3)

  # # Create a two-column view
  # col1, col2 = st.columns(2)
  # with col1:
  #     # User input - The number of ideas to generate
  #     num_input = st.slider(
  #       "Number of ideas", 
  #       value = 3, 
  #       key = "num_input", 
  #       min_value=1, 
  #       max_value=10,
  #       help="Choose to generate between 1 to 10 ideas")
  # with col2:
  #     # User input - The 'temperature' value representing the level of creativity
  #     creativity_input = st.slider(
  #       "Creativity", value = 0.5, 
  #       key = "creativity_input", 
  #       min_value=0.1, 
  #       max_value=0.9,
  #       help="Lower values generate more “predictable” output, higher values generate more “creative” output")  
  # Submit button to start generating ideas
  generate_button = form.form_submit_button("Generate Idea")

  if generate_button:
    if appetite_input == "":
        st.error("Cuisine field cannot be blank")
    else:
        my_bar = st.progress(0.05)
        st.subheader("Meal Prep Ideas:")

        is_valid = 0
        while not is_valid:
            st.markdown("""---""")
            meal_idea = generate_idea_v2(appetite_input, tdee, goal, num_meals)
            
            # Validate the nutritional information
            is_valid, message = validate_nutrition(meal_idea, tdee, goal)
            
            if is_valid:
                st.write(meal_idea)
                st.success(message)
            else:
                time.sleep(2)