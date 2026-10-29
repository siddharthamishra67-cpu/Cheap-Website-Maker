import re
import logging
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Affordable Website Maker",
    page_icon="🌐",
    layout="wide",
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .price-tag {
        background-color: #DCFCE7;
        color: #15803D;
        font-size: 25px;
        font-weight: 700;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #22C55E;
        margin-bottom: 30px;
    }
    .cta-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    .phone-link {
        font-size: 28px;
        font-weight: 800;
        color: #2563EB;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- CONSTANTS ----------------
PHONE_NUMBER = "+919532991633"
COLUMNS = ["Name", "Phone", "Type", "Requirements"]


# ---------------- GOOGLE SHEETS CONNECTION ----------------
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)


def save_lead(name, phone, website_type, requirements):
    """Append one lead without replacing existing spreadsheet records."""
    
    # Load secrets cleanly as a raw dictionary
    sec = dict(st.secrets["connections"]["gsheets"])
    
    # Fix broken newlines in the private key text string automatically
    if "private_key" in sec and isinstance(sec["private_key"], str):
        sec["private_key"] = sec["private_key"].replace("\\n", "\n")
        
    # Force clean Line-break formatting parameters explicitly
    conn = st.connection(
        "gsheets",
        type=GSheetsConnection,
        spreadsheet=sec.get("spreadsheet"),
        project_id=sec.get("project_id"),
        private_key_id=sec.get("private_key_id"),
        private_key=sec.get("private_key"),
        client_email=sec.get("client_email"),
        client_id=sec.get("client_id")
    )

    # Do not overwrite the sheet if reading existing data fails.
    try:
        existing = conn.read(worksheet="Sheet1", ttl=0)
    except Exception:
        existing = None

    if existing is None or existing.empty:
        existing = pd.DataFrame(columns=COLUMNS)

    # Ensure the expected columns exist.
    for column in COLUMNS:
        if column not in existing.columns:
            existing[column] = ""

    existing = existing[COLUMNS].fillna("")

    new_lead = pd.DataFrame(
        [{
            "Name": name,
            "Phone": phone,
            "Type": website_type,
            "Requirements": requirements,
        }],
        columns=COLUMNS,
    )

    updated = pd.concat([existing, new_lead], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated)


# ---------------- LAYOUT ----------------
left_col, right_col = st.columns([1.2, 1])

with left_col:

    # Hero section
    st.markdown(
        '<div class="main-title">🚀 Need a Professional Website?</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-title">'
        "Get your business online with a stunning, "
        "high-speed landing page."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="price-tag">'
        "💰 Special Offer: Website Packages Under ₹2,000!"
        "</div>",
        unsafe_allow_html=True,
    )

    # Features
    st.subheader("🛠️ What We Offer:")

    f1, f2 = st.columns(2)

    with f1:
        st.markdown("✅ **Modern, clean UI designs**")
        st.markdown("✅ **Mobile and tablet responsive**")
        st.markdown("✅ **Fast-loading pages**")

    with f2:
        st.markdown("✅ **Maps and contact forms**")
        st.markdown("✅ **Social media links**")
        st.markdown("✅ **Basic technical support**")

    st.divider()

    # Portfolio
    st.subheader("📁 Our Design Samples")

    p1, p2 = st.columns(2)

    with p1:
        st.info(
            "**🏪 Business / E-commerce Site**\n\n"
            "Product displays, simple navigation, and "
            "options for customers to contact or order."
        )

    with p2:
        st.info(
            "**💼 Portfolio / Landing Page**\n\n"
            "Professional layouts, clear typography, and "
            "contact forms to generate enquiries."
        )

    st.caption(
        "Final features, domain, hosting, payment integration, "
        "and support terms depend on the agreed package."
    )

    st.divider()

    # Lead capture form
    st.subheader("📩 Get a Free Consultation")
    st.caption("Fill in the form to send your project requirements.")

    with st.form("consultation_form", clear_on_submit=True):

        client_name = st.text_input(
            "Your Name *",
            placeholder="Enter your full name",
            max_chars=100,
        )

        client_phone = st.text_input(
            "Your Phone Number *",
            placeholder="Enter your 10-digit mobile number",
            max_chars=16,
        )

        web_type = st.selectbox(
            "Website Type",
            [
                "Business Landing Page",
                "E-commerce Store",
                "Personal Portfolio",
                "Blog",
                "Other",
            ],
        )

        requirements = st.text_area(
            "Project Requirements",
            placeholder="Describe your business and website needs...",
            max_chars=3000,
        )

        consent = st.checkbox(
            "I agree to be contacted about my website enquiry."
        )

        submitted = st.form_submit_button(
            "Submit Requirements 🚀",
            use_container_width=True,
        )

        if submitted:

            clean_name = client_name.strip()
            clean_phone = re.sub(r"[\s\-()]", "", client_phone.strip())

            # Validate an Indian mobile number.
            if clean_phone.startswith("+91"):
                clean_phone = clean_phone[3:]
            elif clean_phone.startswith("91") and len(clean_phone) == 12:
                clean_phone = clean_phone[2:]

            if not clean_name:
                st.error("Please enter your name.")

            elif not re.fullmatch(r"[6-9]\d{9}", clean_phone):
                st.error(
                    "Please enter a valid 10-digit Indian mobile number."
                )

            elif not consent:
                st.warning(
                    "Please agree to be contacted about your enquiry."
                )

            else:
                try:
                    with st.spinner("Submitting your enquiry..."):
                        save_lead(
                            clean_name,
                            clean_phone,
                            web_type,
                            requirements.strip(),
                        )

                    st.success(
                        "Thank you! Your enquiry has been submitted."
                    )
                    st.info(
                        "Our team will call you at your provided number within 2 hours."
                    )

                except Exception:
                    # Log technical details privately on the server.
                    logger.exception("Unable to save website enquiry.")

                    st.error(
                        "We could not save your enquiry right now. "
                        "Please try again later or contact us by phone."
                    )

    st.divider()

    # FAQ
    st.subheader("🤔 Frequently Asked Questions")

    with st.expander("⏱️ How long does a website take?"):
        st.write(
            "The estimated delivery time for a basic website is "
            "3–5 business days after receiving the required content. "
            "Complex projects may take longer."
        )

    with st.expander("💸 Are there any extra charges?"):
        st.write(
            "Packages are advertised under ₹2,000. Confirm the final "
            "price before booking. Domain registration, hosting, "
            "premium features, and third-party services may cost extra."
        )

    with st.expander("📱 Will the website work on mobile?"):
        st.write(
            "Websites are designed to adapt to mobile phones, tablets, "
            "and desktop screens. The final result depends on testing metrics."
        )

    # Call to Action Box
    st.markdown(
        f"""
        <div class="cta-box">
            <h3>📞 Call Us Directly for Fast Booking</h3>
            <p style="font-size: 16px; color: #4B5563;">Tap the number below to talk to an expert right now!</p>
            <a href="tel:{PHONE_NUMBER}" class="phone-link">📱 {PHONE_NUMBER}</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

with right_col:
    st.subheader("💬 Chat with Our Sales Assistant")
    st.caption("Get immediate answers about pricing, timelines, features, and project booking instructions.")
    
    # Initialize stable local chat records
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your automated agency representative. Want to get a professional business website launched at just ₹2,000? Tell me what kind of site you need!"}
        ]

    # Render layout dialogue logs
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
