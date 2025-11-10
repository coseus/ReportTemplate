# components/poc.py
import streamlit as st
import base64
import uuid

def render():
    # PROTECȚIE ABSOLUTĂ – chiar dacă main.py uită
    if "pocs" not in st.session_state:
        st.session_state.pocs = []

    st.subheader("Proof of Concept")

    with st.expander("Add New PoC", expanded=True):
        title = st.text_input("Title", value="Untitled PoC", key="poc_title")
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
            poc_id = str(uuid.uuid4())[:8]
            st.session_state.pocs.append({
                "id": poc_id,
                "title": title.strip() or "Untitled PoC",
                "description": desc,
                "code": code,
                "images": images_b64
            })
            st.success(f"PoC added! (ID: {poc_id})")
            st.rerun()

    st.markdown("### Current PoCs")
    
    if not st.session_state.pocs:
        st.info("No PoC added yet.")
        return

    for i in range(len(st.session_state.pocs) - 1, -1, -1):
        poc = st.session_state.pocs[i]
        poc_id = poc.get("id", f"temp_{i}")
        
        with st.expander(f"**{poc.get('title', 'Untitled PoC')}** (ID: {poc_id})"):
            col1, col2 = st.columns([3, 1])
            with col1:
                if poc.get("description"):
                    st.write(poc["description"])
                if poc.get("code"):
                    st.code(poc["code"], language="bash")
            with col2:
                if st.button("Delete", key=f"del_{poc_id}"):
                    st.session_state.pocs.pop(i)
                    st.success("Deleted!")
                    st.rerun()

            if poc.get("images"):
                cols = st.columns(3)
                for j, img in enumerate(poc["images"][:3]):
                    with cols[j]:
                        st.image(img, use_column_width=True)
                if len(poc["images"]) > 3:
                    st.caption(f"+ {len(poc['images'])-3} more images")
