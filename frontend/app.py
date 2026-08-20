import streamlit as st
import requests

st.title("☁️ Project 19: Terraform Infrastructure Blueprint")
if st.button("Verify Terraform State"):
    res = requests.get("http://127.0.0.1:8000/api/state")
    if res.status_code == 200:
        data = res.json()
        st.success(data["state_status"])
        st.metric("Managed Cloud Resources", data["resources_provisioned"])
        st.write(f"**Target Workspace:** {data['workspace']} ({data['cloud_provider']})")