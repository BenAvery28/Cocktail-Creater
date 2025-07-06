import streamlit as st
import requests
from PIL import Image
import io


def all_cocktails(drinks):
    """Once we have the known ingredients we query the TheCocktailDB API for cocktials that
    are possible to make"""
    cocktails = set()
    for ingredients in drinks:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredients}"
        res = requests.get(url).json()
        if res["drinks"]:
            for drink in res["drinks"]:
                cocktails.add(drink["strDrink"])
    return cocktails

st.title("Cocktail Maker")

uploaded_file = st.file_uploader("Upload your bottles photo", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image")

        # hardcoded bottles for now but they should be pulled from the image uploaded by the user
        bottles = ["Vodka", "Whiskey", "Rum"]  
        st.write(f"Detected bottles: {', '.join(bottles)}")

        # call the API to figure out which drinks the user can create with the bottles detected
        drinks = all_cocktails(bottles)

        if drinks:
            st.write("You can make these drinks:")    
            for drink in sorted(drinks):
                st.write("- " + drink)
        else:
            st.write("No drinks found for your ingredients.")

    except Exception as e:
        st.error(f"Could not process the uploaded file. Error: {e}")