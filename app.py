import streamlit as st
from rag_engine import search_medicines, answer_with_llm

st.set_page_config(page_title="💊 Medicine Assistant", layout="wide")

st.title("💊 Medicine Query Bot")
st.write("Ask me about common medicines and their uses!")

user_query = st.text_input("Enter your health-related query:")

if user_query:
    with st.spinner("🔍 Searching..."):
        results = search_medicines(user_query)
        answer = answer_with_llm(user_query, results)

    st.subheader("📌 Answer:")
    st.markdown(answer)

    st.subheader("🔎 Retrieved Info:")
    for r in results:
        st.markdown(f"""
        **Medicine:** {r['medicine_name']}  
        **Uses:** {r['uses']}  
        **Manufacturer:** {r['manufacturer']}  
        ![Image]({r['image_url']})  
        ---
        """)
