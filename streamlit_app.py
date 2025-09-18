import streamlit as st
import requests
import base64

st.title("Azure Vision Scene/Defect Detection Portal")

st.write("""
Upload an image (PNG/JPG) to analyze it for manufacturing scenes or tags using the Azure Vision API.
For detecting default, use Azure Custom Vision with your labeled defect images to train models 
that recognize your unique defect type
""")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    # Convert image to base64 string
    bytes_data = uploaded_file.read()
    image_base64 = base64.b64encode(bytes_data).decode("utf-8")

    if st.button("Analyze for Scenes/Defects"):
        with st.spinner("Analyzing..."):
            url = "http://localhost:8000/api/v1/inspect"
            payload = {"image_base64": image_base64}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("Analysis Complete!")
                st.write(f"**Image ID:** {data.get('image_id')}")
                st.write(f"**Defective:** {'Yes' if data.get('is_defective') else 'No'}")
                st.write("**Probabilities:**")
                st.json(data.get("probabilities"))
                if data.get("notes"):
                    st.write(f"**Notes:** {data.get('notes')}")
                st.write("**Scenes:**")
                st.json({data.get("scenes")})    
            else:
                st.error(f"API Error: {response.status_code}")
                st.json(response.json())
