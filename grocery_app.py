import cohere
import streamlit as st
import os
import textwrap
import json
import dotenv
from dotenv import load_dotenv, find_dotenv

# Set up Cohere client
_ = load_dotenv(find_dotenv())
co = cohere.Client(os.environ["COHERE_API_KEY"]) # Your Cohere API key

def generate_idea(cuisine, temperature):
  """
  Generate grocery plan given cuisine style
  Arguments:
    cuisine(str): the cuisine name
    temperature(str): the Generate model `temperature` value
  Returns:
    response(str): the grocery shopping route
  """
  prompt = f"""
Generate a meal prep idea given the cuisine style for meal prep for gym goers couple with following body stats:
  Male:
    177 cm, 167 lb, 16% body fat, TDEE estimate: 2691
  Female:
    160 cm, 125 lb, 25% body fat, TDEE estimate: 1800
Calculate the required serviings for at least 6 meals for this couple(which means in total 12 meal boxes) with the diet goal of lean bulking, which means all the recipe needs to be high in protein, low enough in fat and carb as long as it doesn't affect the flavour.
Return the cuisine, required ingredients, and recipe step by step without additional commentary.
    

## Examples
Appetite Description:
  A flavorful stew recipe that takes minimum amount of effort to make
Cuisine: 
  Beer Chicken
Ingredients: 
  Olive Oil: For cooking the chicken. I recommend a lighter olive oil as they tend to take the heat better than extra-virgin. 
  Chicken: This recipe uses 7 to 8 boneless, skinless chicken thighs.
  Herbs & Spices: You'll need half a teaspoon each of dried oregano, dried thyme, garlic powder and smoked or sweet paprika.
  Salt & Pepper: To taste.
  Shallots: Peel and thinly slice two shallots.
  Garlic: You'll need one clove of garlic, minced or pressed.
  Beer: For this recipe, I use half a cup of beer. This is a great use for an unfinished beer, since it doesn't matter if it's flat.
  Soy Sauce: A couple of tablespoons of low-sodium soy sauce give a great depth of flavor to the chicken.
  Whole Grain Mustard: Grainy mustard is such an underused ingredient! I love it on just about everything, and in this sauce it really complements the beer.
  Honey: You'll need just one tablespoon of your favorite honey.
  Parsley: Chopped fresh, for garnish.
Recipe:
  1. Prep Chicken: Heat your olive oil in a 12-inch skillet set over medium heat. In the meantime, season the chicken thighs well with oregano, thyme, garlic powder, paprika, salt and pepper. 
  2. Cook First Side of Chicken: Add the chicken thighs to the heated skillet and cook for 5 minutes, or until golden brown.
  3. Cook Second Side: Flip the chicken over and continue to cook for 6 to 8 more minutes, or until done. The internal temperature of the chicken should register at 165˚F.
  4. Reserve Chicken & Sauté Aromatics: Remove the cooked thighs from the skillet and set aside. Return the skillet to the burner, and turn the heat up to medium-high. Add the shallots to the skillet and cook for 1 minute. Stir in the garlic and cook for 20 seconds more.
  5. Whisk in Liquids: Whisk or stir in the beer, soy sauce, mustard and honey; bring the sauce  mixture to a boil, while scraping up all the browned bits from the bottom of the skillet.
  6. Reduce Sauce & Coat Chicken: Continue to cook the sauce for 3 minutes, or until it is reduced. Then return the chicken thighs to the skillet, and coat them with the sauce. Remove from the heat and serve.

Appetite Description:
  Seafood based, easily put protein, carb into the meal. Full of garlic.
Cuisine:
  Spaghetti with Clams and Garlic
Ingredients:
  1 pound spaghetti
  Kosher salt
  1/4 cup extra-virgin olive oil
  4 garlic cloves, minced
  1/2 teaspoon crushed red pepper
  2 dozen littleneck clams, scrubbed
  1/4 cup water
  1/4 cup finely chopped parsley
  Freshly ground black pepper
Recipe:
  1. In a large pot of boiling salted water, cook the spaghetti until just al dente, then drain the pasta well.
  2. Meanwhile, in a large, deep skillet, heat the olive oil. Add the minced garlic and crushed red pepper and cook over moderately high heat, stirring occasionally, until the garlic is lightly browned, about 1 1/2 minutes. Add the clams and water, cover, and simmer until the clams open and are just cooked through, 5 to 8 minutes. Discard any clams that don't open.
  3. Add the spaghetti and the chopped parsley to the clams in the skillet and season with pepper. Toss over moderately high heat just until the spaghetti absorbs some of the juices, about 1 minute. Transfer the spaghetti and clams to shallow bowls and serve right away.

Appetite Description:
  Classic Taiwanese cuisines with strong aroma and stir fried aromatics like scallion, garlic, and ginger.
Cuisine:
  Three Cups Chicken
Ingredients:
  3 tablespoons sesame oil
  1 2-to-3-inch piece of ginger, peeled and sliced into coins, approximately 12
  12 cloves of garlic, peeled
  4 whole scallions, trimmed and cut into 1-inch pieces
  3 dried red peppers or 1 teaspoon red-pepper flakes
  2 pounds chicken thighs, boneless or bone-in, cut into bite-size pieces
  1 tablespoon unrefined or light brown sugar
  1/2 cup rice wine
  1/4 cup light soy sauce
  2 cups fresh Thai basil leaves or regular basil leaves
Recipe:
  1. Heat a wok over high heat and add 2 tablespoons sesame oil. When the oil shimmers, add the ginger, garlic, scallions and peppers, and cook until fragrant, approximately 2 minutes.
  2. Scrape the aromatics to the sides of the wok, add remaining oil and allow to heat through. Add the chicken, and cook, stirring occasionally, until it is browned and crisping at the edges, approximately 5 to 7 minutes.
  3. Add sugar and stir to combine, then add the rice wine and soy sauce, and bring just to a boil. Lower the heat, then simmer until the sauce has reduced and started to thicken, approximately 15 minutes.
  4. Turn off the heat, add the basil and stir to combine. Serve with white rice.
  

## Your Task
Appetite Description: {cuisine}
Cuisine:
Ingredients:
Recipe:
"""

  # Call the Cohere Chat endpoint
  response = co.chat( 
    message=prompt,
    model='command-r', 
    temperature=temperature,
    preamble="")
  
  return response.text

def generate_name(appetite_description, temperature):
  """
  Generate cuisine name given an appetite description
  Arguments:
    appetite_description(str): the appetite description
    temperature(str): the Generate model `temperature` value
  Returns:
    response(str): the cuisine name
  """
  prompt= f"""
Generate a cuisine name given the appetite description. Return the cuisine name and without additional commentary.

## Examples
cuisine Idea: A flavorful stew recipe that takes minimum amount of effort to make
cuisine Name: Beer chicken

cuisine Idea: Seafood based, easily put protein, carb into the meal. Full of garlic.
cuisine Name: Spaghetti with Clams and Garlic 

cuisine Idea: Classic Taiwanese cuisines with strong aroma and stir fried aromatics like scallion, garlic, and ginger.
cuisine Name: Three Cups Chicken

cuisine Idea: Sour and sweet and bold in seasoning stir fired thai noodle dish
cuisine Name: Pad Thai

## Your Task
cuisine Idea: {appetite_description}
cuisine Name:"""
  # Call the Cohere Chat endpoint
  response = co.chat( 
    message=prompt,
    model='command-r',
    temperature=temperature,
    preamble="")

  return response.text

# The front end code starts here

st.title("Cuisine Idea Generator")

form = st.form(key="user_settings")
with form:
  st.write("Enter a description of what you're feeling [Example: Light seasoned southern food, Japanese style, anything with beef] ")
  # User input - Industry name
  appetite_input = st.text_input("Cuisine Idea", key = "appetite_input")

  # Create a two-column view
  col1, col2 = st.columns(2)
  with col1:
      # User input - The number of ideas to generate
      num_input = st.slider(
        "Number of ideas", 
        value = 3, 
        key = "num_input", 
        min_value=1, 
        max_value=10,
        help="Choose to generate between 1 to 10 ideas")
  with col2:
      # User input - The 'temperature' value representing the level of creativity
      creativity_input = st.slider(
        "Creativity", value = 0.5, 
        key = "creativity_input", 
        min_value=0.1, 
        max_value=0.9,
        help="Lower values generate more “predictable” output, higher values generate more “creative” output")  
  # Submit button to start generating ideas
  generate_button = form.form_submit_button("Generate Idea")

  if generate_button:
    if appetite_input == "":
      st.error("Industry field cannot be blank")
    else:
      my_bar = st.progress(0.05)
      st.subheader("Meal prep Ideas:")

      for i in range(num_input):
          st.markdown("""---""")
          startup_idea = generate_idea(appetite_input,creativity_input)
          startup_name = generate_name(startup_idea,creativity_input)
          st.markdown("##### " + startup_name)
          st.write(startup_idea)
          my_bar.progress((i+1)/num_input)