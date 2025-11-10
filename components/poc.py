# components/poc.py
import streamlit as st
import base64

def render():
    st.subheader("Proof of Concept")

    # === BACKUP – în caz că nu e inițializat în main.py ===
    if "poc_list" not in st.session_state:
        st.session_state.poc_list = []

    # === ADD NEW POC ===
    with st.expander("Add New PoC", expanded=True):
        title = st.text_input("Title", "SMB Relay Attack", key="poc_title")
        description = st.text_area("Description", height=100, key="poc_desc")
        code = st.text_area("Terminal Code", height=150, key="poc_code", placeholder="┌──(root㉿kali)-[~]\n└─# responder -I eth0")
        
        uploaded_imgs = st.file_uploader("Screenshots", type=["png","jpg","jpeg"], accept_multiple_files=True, key="poc_imgs")
        images_b64 = []
        for img in uploaded_imgs:
            b64 = base64.b64encode(img.read()).decode()
            images_b64.append(f"data:{img.type};base64,{b64}")

        if st.button("Add PoC", type="primary"):
            poc = {
                "title": title,
                "description": description,
                "code": code,
                "images": images_b64
            }
            st.session_state.poc_list.append(poc)
            st.success("PoC added!")
            st.rerun()

    # === LISTĂ POC ===
    st.markdown("### Current PoCs")
    if st.session_state.poc_list:
        for idx, poc in enumerate(st.session_state.poc_list):
            with st.expander(f"{poc.get('title','PoC')} (ID: {idx})", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(poc.get("description", ""))
                    if poc.get("code"):
                        st.code(poc["code"])
                with col2:
                    if st.button("Delete", key=f"del_poc_{idx}"):
                        st.session_state.poc_list.pop(idx)
                        st.success("PoC deleted!")
                        st.rerun()

                if poc.get("images"):
                    cols = st.columns(min(len(poc["images"]), 3))
                    for i, img_b64 in enumerate(poc["images"]):
                        with cols[i % 3]:
                            st.image(img_b64, use_column_width=True)
    else:
        st.info("No PoC added yet.")
