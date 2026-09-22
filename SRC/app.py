import streamlit as st
import pickle
from pathlib import Path
from tensorflow.keras.models import load_model

from auth import register_user, login_user


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Developer Sales Intelligence AI",
    page_icon="🏢",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f8fc;
}

/* Main header */
.hero {
    background: linear-gradient(135deg, #071a3d, #1456c7);
    border-radius: 20px;
    padding: 35px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero h3 {
    font-size: 21px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 16px;
    margin-bottom: 5px;
}

/* Section headings */
.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #123b7a;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 3px 12px rgba(15,23,42,0.06);
}

/* Prediction area */
.prediction-box {
    background: linear-gradient(135deg, #eef6ff, #ffffff);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #bfdbfe;
}

/* Footer */
.footer {
    text-align: center;
    padding: 25px;
    color: #64748b;
    font-size: 14px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    background-color: #1877F2;
    color: white;
    border: none;
}

.stButton > button:hover {
    background-color: #0d5ecb;
    color: white;
}
/* Hide unnecessary top padding */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================================================
# LOGIN / REGISTER
# =========================================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="hero">
        <h1>🏢 Developer Sales Intelligence AI</h1>
        <h3>AI-Powered Property Sales Prediction</h3>
        <p>Vasai One • Swastik Lifestyle Pvt. Ltd.</p>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    with login_tab:

        st.subheader("Welcome Back")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            key="login_button",
            use_container_width=True
        ):

            if login_user(
                login_username,
                login_password
            ):

                st.session_state.logged_in = True
                st.session_state.username = login_username

                st.success("Login successful!")
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    with register_tab:

        st.subheader("Create Your AI Account")

        register_username = st.text_input(
            "Choose Username",
            key="register_username"
        )

        register_password = st.text_input(
            "Choose Password",
            type="password",
            key="register_password"
        )

        register_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button(
            "📝 Create Account",
            key="register_button",
            use_container_width=True
        ):

            if register_password != register_confirm:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    register_username,
                    register_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Account created successfully. "
                        "Go to the Login tab."
                    )

                else:

                    st.error(message)

    st.stop()


# =========================================================
# LOAD MODEL
# =========================================================

model = load_model(
    "MODEL/property_sales_model.keras"
)

with open(
    "MODEL/property_scaler.pkl",
    "rb"
) as file:

    scaler = pickle.load(file)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🏢 Developer AI")

    st.markdown("---")

    st.markdown("### 👤 User")

    st.write(
        st.session_state.username
    )

    st.markdown("---")

    st.markdown("### 🏗️ Developer")

    st.write("**Swastik Lifestyle Pvt. Ltd.**")

    st.markdown("### 🏢 Project")

    st.write("**Vasai One**")
    st.write("📍 Vasai West, Suncity")

    st.markdown("---")

    st.markdown("### 🏠 Property Types")

    st.write("• 2 BHK")
    st.write("• 3 BHK")
    st.write("• 4 BHK")
    st.write("• Duplex")

    st.markdown("---")

    st.markdown("### 🏗️ Project Structure")

    st.write("102 Residential Units")
    st.write("22-Storey Tower")
    st.write("G+5 Amenities + Parking")
    st.write("Starting ₹1.04 Cr+")

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()


# =========================================================
# HERO SECTION
# =========================================================

# =========================================================
# HERO SECTION
# =========================================================

hero_path = Path(__file__).resolve().parent / "vasai_one_hero.png"

if hero_path.exists():
    st.image(str(hero_path), use_container_width=True)
else:
    st.error("Hero image not found.")

# =========================================================
# PROJECT IMAGE
# =========================================================



# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">🏗️ Project Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Residential Units",
        "102"
    )

with c2:
    st.metric(
        "Tower",
        "22 Storey"
    )

with c3:
    st.metric(
        "Configurations",
        "2 / 3 / 4 BHK + Duplex"
    )

with c4:
    st.metric(
        "Starting Price",
        "₹1.04 Cr+"
    )


# =========================================================
# PROJECT HIGHLIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">✨ Project Highlights</div>',
    unsafe_allow_html=True
)

h1, h2, h3, h4, h5, h6 = st.columns(6)

with h1:
    st.info("🏊\n\nSwimming Pool")

with h2:
    st.info("🏋️\n\nFitness Center")

with h3:
    st.info("🌳\n\nLandscaped Garden")

with h4:
    st.info("🧒\n\nChildren's Play Area")

with h5:
    st.info("🏠\n\nClubhouse")

with h6:
    st.info("🚗\n\nParking Space")


# =========================================================
# SALES INTELLIGENCE
# =========================================================

st.markdown(
    '<div class="section-title">📊 Sales & Marketing Intelligence</div>',
    unsafe_allow_html=True
)

st.info(
    "Demo/Simulated Data — created for the academic project prototype."
)


col1, col2, col3 = st.columns(3)


# =========================================================
# COLUMN 1
# =========================================================

with col1:

    total_units = st.number_input(
        "Total Residential Units",
        min_value=1,
        value=102,
        step=1
    )

    average_price = st.number_input(
        "Average Property Price (₹ Crore)",
        min_value=0.10,
        value=1.35,
        step=0.05
    )

    current_leads = st.number_input(
        "Current Leads",
        min_value=0,
        value=320,
        step=10
    )


# =========================================================
# COLUMN 2
# =========================================================

with col2:

    site_visits = st.number_input(
        "Current Site Visits",
        min_value=0,
        value=135,
        step=5
    )

    marketing_spend = st.number_input(
        "Monthly Marketing Spend (₹ Lakh)",
        min_value=0.0,
        value=3.5,
        step=0.5
    )

    broker_leads = st.number_input(
        "Broker / Channel Partner Leads",
        min_value=0,
        value=85,
        step=5
    )


# =========================================================
# COLUMN 3
# =========================================================

with col3:

    previous_bookings = st.number_input(
        "Previous Month Bookings",
        min_value=0,
        value=17,
        step=1
    )

    avg_3_month = st.number_input(
        "3-Month Average Bookings",
        min_value=0.0,
        value=15.0,
        step=1.0
    )

    avg_6_month = st.number_input(
        "6-Month Average Bookings",
        min_value=0.0,
        value=13.0,
        step=1.0
    )


previous_revenue = st.number_input(
    "Previous Month Booking Revenue (₹ Crore)",
    min_value=0.0,
    value=23.0,
    step=0.5
)


# =========================================================
# PROPERTY CONFIGURATION
# =========================================================

st.markdown(
    '<div class="section-title">🏠 Property Configuration</div>',
    unsafe_allow_html=True
)

property_type = st.selectbox(
    "Select Property Configuration",
    [
        "2 BHK",
        "3 BHK",
        "4 BHK",
        "Duplex"
    ]
)


# =========================================================
# NEURAL NETWORK PREDICTION
# =========================================================

st.markdown(
    '<div class="section-title">🧠 Neural Network Prediction</div>',
    unsafe_allow_html=True
)

predict_button = st.button(
    "🚀 Predict Expected Bookings",
    type="primary",
    use_container_width=True
)

if predict_button:

    input_data = [[
        total_units,
        average_price,
        current_leads,
        site_visits,
        marketing_spend,
        broker_leads,
        previous_bookings,
        avg_3_month,
        avg_6_month,
        previous_revenue
    ]]

    input_scaled = scaler.transform(
        input_data
    )

    prediction = model.predict(
        input_scaled,
        verbose=0
    )

    predicted_bookings = max(
        0,
        float(prediction[0][0])
    )

    predicted_bookings = round(
        predicted_bookings
    )

    estimated_booking_value = (
        predicted_bookings * average_price
    )

    st.success(
        "AI prediction completed successfully!"
    )

    r1, r2 = st.columns(2)

    with r1:

        st.metric(
            "🎯 Expected Bookings",
            predicted_bookings
        )

    with r2:

        st.metric(
            "💰 Estimated Booking Value",
            f"₹ {estimated_booking_value:.2f} Cr"
        )

    st.caption(
        "Estimated Booking Value = "
        "Expected Bookings × Average Property Price"
    )

    st.markdown("### 📋 Prediction Summary")

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "Property Type",
        property_type
    )

    s2.metric(
        "Current Leads",
        current_leads
    )

    s3.metric(
        "Site Visits",
        site_visits
    )

    s4.metric(
        "Previous Bookings",
        previous_bookings
    )


# =========================================================
# AI WORKFLOW
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">⚙️ How the AI Works</div>',
    unsafe_allow_html=True
)

w1, w2, w3, w4 = st.columns(4)

with w1:
    st.info(
        "📊\n\n**Business Data**\n\n"
        "Leads, visits, marketing and historical sales."
    )

with w2:
    st.info(
        "⚖️\n\n**Data Scaling**\n\n"
        "Inputs are standardized before prediction."
    )

with w3:
    st.info(
        "🧠\n\n**Neural Network**\n\n"
        "The trained ANN learns patterns from sales data."
    )

with w4:
    st.info(
        "🎯\n\n**Prediction**\n\n"
        "Expected bookings and booking value."
    )


# =========================================================
# ABOUT PROJECT
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📚 About the Project</div>',
    unsafe_allow_html=True
)

a1, a2, a3 = st.columns(3)

about_left, about_right = st.columns([1.2, 1])

with about_left:

    st.markdown("### 🏢 Developer Intelligence")
    st.write(
        "An AI-powered dashboard designed to analyze "
        "property sales and marketing data and support "
        "data-driven decisions."
    )

    st.markdown("### 🧠 Artificial Neural Network")
    st.write(
        "A feed-forward neural network learns relationships "
        "between business inputs and expected bookings."
    )

    st.markdown("### 📊 Dataset")
    st.write(
        "Simulated real-estate sales data created for "
        "academic demonstration."
    )

with about_right:

    about_image = Path(__file__).resolve().parent / "about_project_visual.png"

    if about_image.exists():
        st.image(
            str(about_image),
            use_container_width=True,
            caption="Vasai One — Project Visualization"
        )
    else:
        st.warning("About project image not found.")

# =========================================================
# FOOTER / DEVELOPER CREDIT
# =========================================================

st.markdown(
    """
    <div class="footer">
        <strong>Developer Sales Intelligence AI</strong>
        <br>
        Property Sales Prediction Using Neural Network
        <br><br>
        <strong>Developed by Yash Mukesh Rathod</strong>
        <br>
        Roll No: TDCA049B
        <br>
        TYBCA Project • 2026–2027
        <br>
        KES Shroff College, Kandivali
        <br>
        Department of Information Technology
        <br><br>
        <small>Academic Prototype • Demo/Simulated Data</small>
    </div>
    """,
    unsafe_allow_html=True
)