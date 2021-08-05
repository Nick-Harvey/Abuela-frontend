import logging
import time
import python_pachyderm
import streamlit as st


class Jaruco:
    def __init__(self):
        self.client = python_pachyderm.Client()


    def get_job_state(self, pipeline_name=None):
        for job in self.client(pipeline_name):
            return job.state

    def general_restore(self, uploaded_file):

        """Do a general restore on a photo that doesn't have cracks"""
        filename = '/{}'.format(uploaded_file.name)
        img_bytes = uploaded_file.getvalue()

        with self.client.commit("general_restore_input", "master") as commit:
            self.client.put_file_bytes(commit, filename, img_bytes)
            pass

        with st.spinner(text='Restoring...'):
            
            progress_bar = st.progress(5)
            status_text = st.empty()

            # Check Pachyderm Jobs
            while True:
                try:
                    if all(job.state == 3 for job in self.client.list_job(
                        "general_restore")
                    ):
                        progress_bar.progress(100)
                        break

                    status_text.text('Restoring {}'.format(uploaded_file.name))

                    for i in range(100):
                        progress_bar(i + 1)
                        time.sleep(1)

                except Exception as e:
                    logging.error("job fetch failed: {}".format(e))
            pass
        pass

    def general_restore_wcracks(self, uploaded_file):
        """Do a general restore on a photo that does have cracks"""
        filename = '/{}'.format(uploaded_file.name)
        img_bytes = uploaded_file.getvalue()
        
        with self.client.commit("general_restore_w_cracks_input", "master") as commit:
            self.client.put_file_bytes(commit, filename, img_bytes)

        with st.spinner(text='Restoring... (~40 Seconds)'):
            time.sleep(40)
            pass
        pass