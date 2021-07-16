import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
from matplotlib import pyplot as plt
from google.cloud import storage
import os
from PIL import Image
from decouple import config

gen_restore_input = "abuela_input_images_dev"
scratches_restore_input = "abuela_input_images_scratches_dev"
restored_images = "abuela_input_images_dev"

# App libraries
from app.object_store import ObjectStore
# Jaruco is the hometown my grandmother is from in Cuba.
# She is the insipiration for this project.
from app.pipelines import Jaruco as Jaruco


# Start of Streamlit App
# Convert this to an actual Main function later
st.title("Hola, Abuela!")

st.sidebar.write(
    '''
    ## Step 1.
    Pick a photo you want to restore
    '''
    )


uploaded_file = st.sidebar.file_uploader("Max image size 650x650 (temp issue due to gpu limits)")


## Process the Photo
if uploaded_file is not None:
    #Display the photo that will get enhanced
    image = Image.open(uploaded_file)
    object_store = ObjectStore()

    '''
    **This is the photo that will get restored**
    '''
    st.image(image, caption="Before")

    '''
    ## Step 2.
    **Choose what type of restore you want to apply**
    '''
    with st.form("Choose Restore Option"):
        restore_type = st.radio("Does the image contain cracks or creases?", ['No - General Restore', 'Yes - Fill In Cracks'])
        submitted = st.form_submit_button("Restore") 

        if submitted:
            if restore_type == 'No - General Restore':
                # TEMP: Upload it to gcloud to bkup
                object_store.upload_blob(gen_restore_input, uploaded_file, uploaded_file.name)
                
                # Kick off restoration pipeline for no_scratch img
                Jaruco.general_restore(uploaded_file)

                # Fetch the restored image
                restored_image = object_store.download_blob(restored_images)

            elif restore_type == 'Yes - Fill In Cracks':
                # TEMP: Upload it to gcloud to bkup
                object_store.upload_blob(scratches_restore_input, uploaded_file, uploaded_file.name)
                
                # Kick off restoration pipeline for imgs with scratches
                Jaruco.general_restore_wcracks(uploaded_file)

                # Fetech the restored cracked image
                restored_image = object_store.download_blob(restored_images)
            else:
                pass
            
            st.success('Done!')

            before, after = st.beta_columns(2)
            
            with before:
                st.header("Before")
                st.image(image)

            with after:
                st.header("After")
                st.image(restored_image)