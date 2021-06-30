import os
import logging
import time
import python_pachyderm
from PIL import Image
import streamlit as st

# Connects to a pachyderm cluster on localhost:30650.
# For other options, see the API docs.
client = python_pachyderm.Client()


class Jaruco:

	def general_restore(uploaded_file):
		"""Do a general restore on a photo that doesn't have cracks"""
		filename = '/{}'.format(uploaded_file.name)
		img_bytes = uploaded_file.getvalue()

		with client.commit("general_restore_input", "master") as commit:
			client.put_file_bytes(commit, filename, img_bytes)
			pass

		#TODO Build an actual progress function
		with st.spinner(text='Restoring... (~20 Seconds)'):
			time.sleep(20)
			pass
		pass

	def general_restore_wcracks(uploaded_file):
		"""Do a general restore on a photo that does have cracks"""
		filename = '/{}'.format(uploaded_file.name)
		img_bytes = uploaded_file.getvalue()
		
		with client.commit("general_restore_w_cracks_input", "master") as commit:
			client.put_file_bytes(commit, filename, img_bytes)

		with st.spinner(text='Restoring... (~30 Seconds)'):
			time.sleep(30)
			pass
		pass