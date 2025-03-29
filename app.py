import streamlit as st
import requests

# Fungsi untuk memanggil API Groq
def call_groq_api(system_message, user_prompt, model):

    groq_api_key=st.secrets["OPENROUTER_APIKEY"]
    #groq_api_key =  OPENROUTER_API_KEY # Ganti dengan API key Groq Anda
    groq_url = "https://openrouter.ai/api/v1/chat/completions"  # Contoh endpoint Groq

    # Siapkan array messages
    messages = []

    # Tambahkan role system jika ada
    if system_message:
        messages.append({"role": "system", "content": system_message})

    # Tambahkan role user
    messages.append({"role": "user", "content": user_prompt})

    groq_data = {
        "model": model,
        "messages": messages
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_api_key}"
    }

    response = requests.post(groq_url, json=groq_data, headers=headers)
    groq_response = response.json()

    # Ambil hanya konten dari respons
    content = groq_response['choices'][0]['message']['content']
    return content

# Judul aplikasi Streamlit
st.title("API Interface")

# Input untuk System Message (opsional)
system_message = st.text_area("System Message (Optional)", value="", height=100)

# Input untuk User Prompt
user_prompt = st.text_area("Prompt", value="", height=100)

# Pilihan model
#model_options = ["google/gemma-3-27b-it", "other-model-1", "other-model-2"]
#selected_model = st.selectbox("Select Model", model_options)
selected_model = st.text_input("Model:", "google/gemma-3-27b-it")

# Tombol Submit
if st.button("Submit"):
    if user_prompt.strip() == "":
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Waiting for response..."):
            try:
                # Panggil API Groq
                response_content = call_groq_api(system_message, user_prompt, selected_model)
                # Tampilkan hasil
                st.success("Response received!")
                st.write("### Response:")
                st.write(response_content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
