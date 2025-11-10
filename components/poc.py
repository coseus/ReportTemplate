# components/poc.py
import streamlit as st
import base64

def render():
    # Backup (în caz că uiți în main.py)
    if "pocs" not in st.session_state:
        st.session_state.pocs = []

    st.subheader("Proof of Concept")

    # === ADD NEW POC ===
    with st.expander("Add New PoC", expanded=True):
        title = st.text_input("Title", "SMB Relay Attack", key="poc_title")
        desc = st.text_area("Description", height=100, key="poc_desc")
        code = st.text_area("Terminal Code", height=150, key="poc_code",
                            placeholder="┌──(root㉿kali)-[~]\n└─# responder -I eth0")
        imgs = st.file_uploader("Screenshots", type=["png","jpg","jpeg"], 
                                accept_multiple_files=True, key="poc_imgs")
        
        images_b64 = []
        for img in imgs:
            b64 = base64.b64encode(img.read()).decode()
            images_b64.append(f"data:{img.type};base64,{b64}")

        if st.button("Add PoC", type="primary"):
            st.session_state.pocs.append({
                "title": title,
                "description": desc,
                "code": code,
                "images": images_b64
            })
            st.success("PoC added!")
            st.rerun()

    # === LISTĂ POC ===
    st.markdown("### Current PoCs")
    if st.session_state.pocs:
        for idx in range(len(st.session_state.pocs)-1, -1, -1):
            poc = st.session_state.pocs[idx]
            with st.expander(f"{poc.get('title','PoC')} (ID: {idx})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(poc.get("description", ""))
                    if poc.get("code"):
                        st.code(poc["code"], language="bash")
                with col2:
                    if st.button("Delete", key=f"del_poc_{idx}"):
                        st.session_state.pocs.pop(idx)
                        st.success("Deleted!")
                        st.rerun()

                if poc.get("images"):
                    cols = st.columns(min(3, len(poc["images"])))
                    for i, img_b64 in enumerate(poc["images"]):
                        with cols[i % 3]:
                            st.image(img_b64, use_column_width=True)
    else:
        st.info("No PoC added yet.")
