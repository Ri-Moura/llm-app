import streamlit as st
import requests

st.title("Multimodal RAG Implementation")

st.write("Upload a PDF file or provide a URL to extract and analyze the brand voice.")

# Form to upload file or provide URL
form = st.form(key='input_form')
index_name = form.text_input("Index Name:", value="default_index")
url = form.text_input("URL of the PDF file:")
submit_button = form.form_submit_button(label='Submit')

if submit_button:
    if url:
        payload = {'index_name': index_name, 'url': url}
        response = requests.post("http://54.172.243.231:8000/generate-content/", data=payload)
    else:
        st.error("Please provide a URL")
        response = None

    if response:
        if response.status_code == 200:
            result = response.json()
            st.success("Brand Voice Extracted Successfully!")
            st.write(result)
        else:
            st.error(f"Error {response.status_code}: {response.text}")

st.write("---")

st.write("Delete an existing Pinecone index.")
delete_index_form = st.form(key='delete_index_form')
delete_index_name = delete_index_form.text_input("Index Name to delete:")
delete_button = delete_index_form.form_submit_button(label='Delete')

if delete_button:
    response = requests.post(f"http://54.172.243.231:8000/delete-index/?index_name={delete_index_name}")
    if response.status_code == 200:
        st.success(f"Index {delete_index_name} deleted successfully!")
    else:
        st.error(f"Error {response.status_code}: {response.text}")