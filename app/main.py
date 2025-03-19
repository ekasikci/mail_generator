import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from utils import clean_text


def create_streamlit_app(llm, clean_text):
    st.title("📧 Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")
    cv_upload = st.file_uploader("Upload a CV", type=["pdf", "docx"])

    cv_data = None
    if cv_upload:
        try:
            cv_data = llm.process_cv(cv_upload)
            st.success("CV uploaded and processed successfully!")
            st.success(cv_data)
        except Exception as e:
            st.error(f"An Error Occurred while processing CV: {e}")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            for job in jobs:
                email = llm.write_mail(job, cv_data)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Email Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)