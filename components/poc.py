# components/poc.py
import streamlit as st
import base64
import uuid

def render():
    # Backup
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
            # GENEREAZĂ ID UNIC
            poc_id = str(uuid.uuid4())[:8]
            st.session_state.pocs.append({
                "id": poc_id,
                "title": title or "Untitled PoC",
                "description": desc,
                "code": code,
                "images": images_b64
            })
            st.success(f"PoC added! (ID: {poc_id})")
            st.rerun()

    # === LISTĂ POC – CU ID UNIC (FĂRĂ PROBLEME LA DELETE) ===
    st.markdown("### Current PoCs")
    if st.session_state.pocs:
        # Parcurgem în ordine inversă pentru delete stabil
        for i in range(len(st.session_state.pocs)-1, -1, -1):
            poc = st.session_state.pocs[i]
            poc_id = poc.get("id", f"temp_{i}")
            
            with st.expander(f"**{poc.get('title','Untitled PoC')}** (ID: {poc_id})", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(poc.get("description", ""))
                    if poc.get("code"):
                        st.code(poc["code"], language="bash")
                with col2:
                    if st.button("Delete", key=f"del_poc_{poc_id}"):  # CHEIE UNICĂ!
                        st.session_state.pocs.pop(i)
                        st.success("PoC deleted!")
                        st.rerun()

                if poc.get("images"):
                    cols = st.columns(min(3, len(poc["images"])))
                    for j, img_b64 in enumerate(poc["images"]):
                        with cols[j % 3]:
                            st.image(img_b64, use_column_width=True)
    else:
        st.info("No PoC added yet. Click 'Add New PoC' above.")
