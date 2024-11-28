from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    if prompt != "":
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(image)
    return response.text


st.set_page_config(page_title="Gemini Image Demo")

st.header("Stamp Vision")
# input=st.text_input("Input Prompt: ",key="input")
prompt = """
Analyze the uploaded image and identify if it is a valid stamp. If valid, perform the following tasks:

Use global knowledge and external references to gather additional details about the stamp, including historical, cultural, or philatelic significance.

- Name of the Stamp
- Date of Issue
- Price
- Brief Description or Special Details (50 words at max)

If the image is blurry or cannot be recognized as a stamp, respond with an error message indicating: 

{"error": "Invalid image. Please try again."}

Output Example (Valid Image):   
{   "name": "Mahatma Gandhi Commemorative Stamp",   
    "date_of_issue": "1948-08-15",   
    "price": "10 Rupees",   
    "description": "Issued to commemorate Mahatma Gandhi's contributions; features a portrait of Gandhi." 
}     

Output Example (Invalid Image):
{   
    "error": "Invalid image. Please try again." 
}     

Process the image carefully and ensure accurate information is extracted."""

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)


submit = st.button("Tell me about the image")

## If ask button is clicked

if submit:
    response = get_gemini_response(prompt, image)
    st.subheader("The Response is")
    st.write(response)
