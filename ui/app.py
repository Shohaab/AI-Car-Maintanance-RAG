import streamlit as st
import requests

st.title("🚗 AI Car Maintenance Guide")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    st.markdown(f"### 🧑 You:\n{chat['question']}")
    answer = chat["answer"]

    sections = ["Simple Explanation", "Probable Causes", "Checks", "Safety Warning"]

    st.markdown("### 🤖 AI Answer:")
    for section in sections:
        start = answer.find(section + ":")
        if start != -1:
            # Find section end
            end_positions = [
                answer.find(s + ":", start + 1)
                for s in sections
                if answer.find(s + ":", start + 1) != -1
            ]
            end = min(end_positions) if end_positions else len(answer)
            content = answer[start + len(section) + 1:end].strip()

            st.subheader(section)
            st.write(content)

st.write("---")

# 🔥 ALWAYS VISIBLE Input Box (continuous chat)
question = st.text_input("Ask another question:")

# When user presses Enter or clicks the button
if st.button("Ask") or (question and st.session_state.get("submitted") != question):
    if question.strip():
        try:
            res = requests.post("http://127.0.0.1:8000/ask", json={"question": question})

            if res.status_code == 200:
                answer = res.json().get("answer", "No answer returned")
                st.session_state.chat_history.append({"question": question, "answer": answer})
                st.session_state.submitted = question  # Prevent double sending
                st.rerun()  # 🔥 Re-run UI but keep chat history
            else:
                st.error(f"Error: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Failed to connect: {e}")
