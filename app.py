import streamlit as st
import json
import re
import base64
from io import BytesIO
from PIL import Image
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas

from playwright_agent import fill_web_form

# ---------- PAGE ----------
st.set_page_config(layout="wide")

# ---------- LOAD ----------
def load_data():
    try:
        with open("form_data.json", "r") as f:
            return json.load(f)
    except:
        return {"name": "", "age": "", "email": "", "city": ""}

def save_data(data):
    with open("form_data.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- NLP ----------
def extract_info(text, data):
    text_lower = text.lower()

    name = re.search(r"my name is ([a-zA-Z\s]+)", text_lower)
    if name:
        data["name"] = name.group(1).title()

    age = re.search(r"\b(\d{1,3})\b", text)
    if age:
        data["age"] = age.group(1)

    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", text)
    if email:
        data["email"] = email.group(0)

    city = re.search(r"from ([a-zA-Z\s]+)", text_lower)
    if city:
        data["city"] = city.group(1).title()

    return data

# ---------- IMAGE HELPERS ----------
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

def signature_to_base64(image_array):
    image = Image.fromarray((image_array).astype("uint8"))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ---------- INIT ----------
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "chat" not in st.session_state:
    st.session_state.chat = []

if "photo" not in st.session_state:
    st.session_state.photo = None

if "signature" not in st.session_state:
    st.session_state.signature = None

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 2])

# ---------- CHAT ----------
with col1:
    st.title("💬 Chat")

    user_input = st.text_input("Type: My name is John, I am 25 from Kochi")

    # PHOTO UPLOAD
    photo = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
    if photo:
        st.session_state.photo = photo

    # SIGNATURE PAD
    st.subheader("✍️ Draw Signature")

    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,1)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        height=150,
        width=300,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas_result.image_data is not None:
        st.session_state.signature = canvas_result.image_data

    # CHAT SEND
    if st.button("Send"):
        if user_input:
            st.session_state.chat.append(("You", user_input))

            st.session_state.data = extract_info(
                user_input, st.session_state.data
            )

            save_data(st.session_state.data)

            st.session_state.chat.append(("Agent", "Form updated ✅"))

    # CHAT HISTORY
    for sender, msg in st.session_state.chat:
        st.write(f"**{sender}:** {msg}")

# ---------- FORM ----------
with col2:
    data = st.session_state.data

    # PHOTO
    photo_html = ""
    if st.session_state.photo:
        img_base64 = image_to_base64(st.session_state.photo)
        photo_html = f"""
        <img src="data:image/png;base64,{img_base64}"
        style="width:120px;height:140px;
        object-fit:cover;border:1px solid black;" />
        """

    # SIGNATURE
    signature_html = ""
    if st.session_state.signature is not None:
        sig_base64 = signature_to_base64(st.session_state.signature)
        signature_html = f"""
        <img src="data:image/png;base64,{sig_base64}"
        style="width:200px;height:80px;object-fit:contain;" />
        """

    # ---------- A4 HTML ----------
    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: #d9d9d9;
            display: flex;
            justify-content: center;
        }}

        .page {{
            width: 210mm;
            height: 297mm;
            background: white;
            padding: 25mm;
            border: 2px solid black;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            font-family: "Times New Roman", serif;
            position: relative;
            box-sizing: border-box;
        }}

        .title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 40px;
        }}

        .section {{
            font-size: 18px;
            font-weight: bold;
            margin-top: 30px;
            border-bottom: 1px solid black;
            padding-bottom: 5px;
        }}

        .row {{
            margin-top: 25px;
            font-size: 17px;
        }}

        .label {{
            display: inline-block;
            width: 180px;
            font-weight: bold;
        }}

        .value {{
            display: inline-block;
            width: 300px;
            border-bottom: 1px solid black;
            padding-left: 5px;
        }}

        .photo {{
            position: absolute;
            top: 30px;
            right: 40px;
        }}

        .signature {{
            margin-top: 80px;
        }}
    </style>
    </head>

    <body>
        <div class="page">

            <div class="photo">
                {photo_html}
            </div>

            <div class="title">USER REGISTRATION FORM</div>

            <div class="section">Personal Details</div>

            <div class="row">
                <span class="label">Full Name</span>
                <span class="value">{data['name']}</span>
            </div>

            <div class="row">
                <span class="label">Age</span>
                <span class="value">{data['age']}</span>
            </div>

            <div class="section">Contact Details</div>

            <div class="row">
                <span class="label">Email</span>
                <span class="value">{data['email']}</span>
            </div>

            <div class="row">
                <span class="label">City</span>
                <span class="value">{data['city']}</span>
            </div>

            <div class="signature">
                Signature: {signature_html}
            </div>

        </div>
    </body>
    </html>
    """

    components.html(html, height=1200, scrolling=False)

    st.markdown("---")

    # EDIT FORM
    name = st.text_input("Name", data["name"])
    age = st.text_input("Age", data["age"])
    email = st.text_input("Email", data["email"])
    city = st.text_input("City", data["city"])

    if st.button("💾 Save"):
        st.session_state.data = {
            "name": name,
            "age": age,
            "email": email,
            "city": city
        }
        save_data(st.session_state.data)
        st.success("Saved!")

    if st.button("🚀 Fill Browser"):
        fill_web_form(st.session_state.data)
        st.success("Browser opened!")