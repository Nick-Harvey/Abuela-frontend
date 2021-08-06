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
            
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Check Pachyderm Jobs
            for i in range(100):
                try:
                    if all(job.state == 3 for job in self.client.list_job("general_restore")):
                        status_text.text('Finished Restoring {}'.format(uploaded_file.name))
                        progress_bar.progress(100)
                        break
                except Exception as e:
                    logging.error("Restore failed: {}".format(e))

                progress_bar.progress(i + 1)
                status_text.text('Restoring {}'.format(uploaded_file.name))
                time.sleep(2)
        pass

        #         try:
        #             if all(job.state == 3 for job in self.client.list_job(
        #                 "general_restore")
        #             ):
        #                 progress_bar.progress(99)
        #                 break

        #             status_text.text('Restoring {}'.format(uploaded_file.name))

        #             for i in range(100):
        #                 progress_bar.progress(i + 1)
        #                 time.sleep(1)

        #         except Exception as e:
        #             logging.error("job fetch failed: {}".format(e))
        #     pass
        # pass

    def general_restore_wcracks(self, uploaded_file):
        """Do a general restore on a photo that does have cracks"""
        filename = '/{}'.format(uploaded_file.name)
        img_bytes = uploaded_file.getvalue()
        
        with self.client.commit("general_restore_w_cracks_input", "master") as commit:
            self.client.put_file_bytes(commit, filename, img_bytes)

        with st.spinner(text='Restoring... (~80 Seconds)'):
            time.sleep(80)
            pass
        pass