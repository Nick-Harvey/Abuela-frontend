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
			# This is what Yusuf added
			while True:
				time.sleep(5)
				try:
					if all(job.state == 3 for job in client.list("general_restore_input")):
						break
				except Exception as e:
					logging.error("job fetch failed: %s".format(e))
			pass
		pass



	def general_restore_wcracks(uploaded_file):
		"""Do a general restore on a photo that does have cracks"""
		filename = '/{}'.format(uploaded_file.name)
		img_bytes = uploaded_file.getvalue()
		
		with client.commit("general_restore_w_cracks_input", "master") as commit:
			client.put_file_bytes(commit, filename, img_bytes)

		with st.spinner(text='Restoring... (~40 Seconds)'):
			time.sleep(40)
			pass
		pass