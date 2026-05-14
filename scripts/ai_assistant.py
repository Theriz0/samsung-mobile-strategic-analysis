import streamlit as st
import google.generativeai as genai

def render_ai_assistant(filtered_df):
    st.subheader("Data Inspector AI")
    st.write("Ask questions about your data to generate insights for your reports.")
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY is missing from .streamlit/secrets.toml")
        return

    genai.configure(api_key=api_key)
    
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        default_index = 0
        for i, m in enumerate(available_models):
            if "gemini-1.5-flash" in m:
                default_index = i
                break
        selected_model_name = st.selectbox("Select Gemini Model:", available_models, index=default_index if available_models else 0)
    except Exception as e:
        st.error(f"Could not load models. Check your API key. Error: {e}")
        selected_model_name = None
        
    if selected_model_name:
        model = genai.GenerativeModel(selected_model_name)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        with st.form(key="ai_form"):
            prompt = st.text_area("Ask the AI Assistant a question:", placeholder="e.g., What was the flagship revenue?")
            submit_button = st.form_submit_button(label="Ask AI")
            
        if submit_button and prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing data..."):
                    try:
                        # Inject dataframe context
                        data_context = filtered_df.to_markdown(index=False)
                        full_prompt = f"You are a helpful data analyst. Here is the current data from the dashboard:\n\n{data_context}\n\nUser Question: {prompt}"
                        
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Error querying Gemini: {e}")
