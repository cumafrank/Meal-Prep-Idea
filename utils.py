import cohere
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
import requests
import re

# Set up Cohere client
#co = cohere.Client(st.secrets["COHERE_API_KEY"])
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def get_nutrient_info(ingredient):
    api_key = os.getenv('USDA_API_KEY')
    base_url = "https://api.nal.usda.gov/fdc/v1"
    
    # Search for the ingredient
    search_url = f"{base_url}/foods/search?api_key={api_key}&query={ingredient}"
    response = requests.get(search_url)
    data = response.json()
    
    if data['foods']:
        food_id = data['foods'][0]['fdcId']
        
        # Get detailed nutrient information
        details_url = f"{base_url}/food/{food_id}?api_key={api_key}"
        details_response = requests.get(details_url)
        details_data = details_response.json()
        
        # Extract relevant nutrient information
        nutrients = {}
        for nutrient in details_data['foodNutrients']:
            if nutrient['nutrient']['name'] in ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference']:
                nutrients[nutrient['nutrient']['name']] = nutrient['amount']
        
        return nutrients
    
    return None

def generate_idea_v1(cuisine, temperature):
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

def generate_idea_v2(cuisine, tdee, goal, num_meals, temperature=0.7):
    # Calculate target macros based on TDEE and goal
    if goal == "Cutting":
        calorie_target = tdee * 0.8
    elif goal == "Bulking":
        calorie_target = tdee * 1.2
    else:  # Maintenance
        calorie_target = tdee
    
    protein_target = calorie_target * 0.3 / 4  # 30% of calories from protein
    fat_target = calorie_target * 0.25 / 9  # 25% of calories from fat
    carb_target = calorie_target * 0.45 / 4  # 45% of calories from carbs
    
    prompt = f"""
Generate a detailed meal prep idea with the following requirements:
- Cuisine: {cuisine}
- Total calories per day: {calorie_target:.0f}
- Protein per day: {protein_target:.0f}g
- Fat per day: {fat_target:.0f}g
- Carbs per day: {carb_target:.0f}g
- Physique goal: {goal}
- Number of meals: {num_meals}

Provide the following information:
1. Detailed cuisine name
2. List of ingredients with precise quantities
3. Step-by-step recipe instructions
4. Macro breakdown per meal and for the entire day

Format your response as follows:

Cuisine Name:
[Detailed cuisine name]

Requirements:
- Cuisine: {cuisine}
- Total calories per day: {calorie_target:.0f}
- Protein per day: {protein_target:.0f}g
- Fat per day: {fat_target:.0f}g
- Carbs per day: {carb_target:.0f}g
- Physique goal: {goal}

Ingredients:
- [Ingredient 1]: [Quantity]
- [Ingredient 2]: [Quantity]
...

Recipe:
1. [Step 1]
2. [Step 2]
...

Macro Breakdown:
Per meal:
- Calories: [X]
- Protein: [X]g
- Fat: [X]g
- Carbs: [X]g

Total per day:
- Calories: [X]
- Protein: [X]g
- Fat: [X]g
- Carbs: [X]g

Only fill your answer in those middle bracket, e.g. [], and triple dot, e.g. ...
"""

    response = co.chat(
        message=prompt,
        model='command-r',
        temperature=temperature,
        preamble=""
    )
    
    return response.text


import re

import re

def validate_nutrition(idea, tdee, goal):
    # Extract the macro breakdown from the generated idea
    total_pattern = r"Total per day:.*?Calories:\s*(\d+).*?Protein:\s*(\d+)g.*?Fat:\s*(\d+)g.*?Carbs:\s*(\d+)g"
    match = re.search(total_pattern, idea, re.DOTALL | re.IGNORECASE)
    
    if match:
        calories, protein, fat, carbs = map(int, match.groups())
        
        # Calculate target macros
        if goal == "Cutting":
            calorie_target = tdee * 0.8
        elif goal == "Bulking":
            calorie_target = tdee * 1.2
        else:  # Maintenance
            calorie_target = tdee
        
        protein_target = calorie_target * 0.3 / 4
        fat_target = calorie_target * 0.25 / 9
        carb_target = calorie_target * 0.45 / 4
        
        # Check if the generated plan meets the requirements
        calorie_diff = abs(calories - calorie_target)
        protein_diff = abs(protein - protein_target)
        fat_diff = abs(fat - fat_target)
        carb_diff = abs(carbs - carb_target)
        
        # You can adjust these thresholds as needed
        if (calorie_diff <= 100 and protein_diff <= 10 and 
            fat_diff <= 5 and carb_diff <= 20):
            return True, "The meal plan meets the nutritional requirements."
        else:
            return False, f"The meal plan does not meet the requirements. Differences: Calories: {calorie_diff:.0f}, Protein: {protein_diff:.0f}g, Fat: {fat_diff:.0f}g, Carbs: {carb_diff:.0f}g"
    else:
        return False, "Unable to extract macro information from the generated idea."

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

# Test
# get_nutrient_info("Chicken thigh")