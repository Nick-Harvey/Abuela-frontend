import logging
import time
import python_pachyderm
import streamlit as st


class Jaruco:
    def __init__(self):
        self.client = python_pachyderm.Client()

    def job_progress(self, pipeline_name, uploaded_file, commit_id):
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Check Pachyderm Jobs
        for i in range(100):
            # try:
            #     if all(job.state == 3 for job in self.client.list_job("{}/{}".format(pipeline_name + "@master", commit_id))):
            #         status_text.text('Finished Restoring {}'.format(uploaded_file.name))
            #         progress_bar.progress(100)
            #         return True

            try:
                if all(job.state == 3 for job in self.client.list_job(pipeline_name, commit_id)):
                    status_text.text('Finished Restoring {}'.format(uploaded_file.name))
                    progress_bar.progress(100)
                    return True

            except Exception as e:
                logging.error("Restore failed: {}".format(e), exc_info=True)

            progress_bar.progress(i + 1)
            status_text.text('Restoring {}'.format(uploaded_file.name))
            time.sleep(1)

        return False

    def general_restore(self, uploaded_file):

        """Do a general restore on a photo that doesn't have cracks"""
        filename = '/{}'.format(uploaded_file.name)
        img_bytes = uploaded_file.getvalue()
        pcommit_id = None

        with self.client.commit("general_restore_input", "master") as commit:
            self.client.put_file_bytes(commit, filename, img_bytes)
            pcommit_id = commit.id

        with st.spinner(text='Restoring...'):
            if not self.job_progress("general_restore", uploaded_file, pcommit_id):
                logging.error("Restore failed: ", exc_info=True)
                pass

    def general_restore_wcracks(self, uploaded_file):
        """Do a general restore on a photo that does have cracks"""
        filename = '/{}'.format(uploaded_file.name)
        img_bytes = uploaded_file.getvalue()
        pcommit_id = None

        with self.client.commit("general_restore_w_cracks_input", "master") as commit:
            self.client.put_file_bytes(commit, filename, img_bytes)
            pcommit_id = commit.id

        with st.spinner(text='Restoring...'):
            if not self.job_progress("general_restore", uploaded_file, pcommit_id):
                logging.error("Restore failed: ", exc_info=True)
                pass
