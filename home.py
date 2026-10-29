
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

SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1gBxO-Y-57yL-gC26cckx9EJZ7gACMV6BV_37KEWgSqo/edit"
)

# ---------------- GOOGLE SHEETS CONNECTION ----------------
@st.cache_resource
def get_connection():
    return st.connection(
        "gsheets",
        type=GSheetsConnection,
        spreadsheet=SPREADSHEET_URL,
    )


def save_lead(name, phone, website_type, requirements):
    """Append one lead without replacing existing spreadsheet records."""
    conn = get_connection()

    existing = conn.read(worksheet="Sheet1", ttl=0)

    if existing is None:
        existing = pd.DataFrame(columns=COLUMNS)

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
            clean_phone = re.sub(
                r"[\s\-()]",
                "",
                client_phone.strip(),
            )

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
                        "Our team will contact you using the number "
                        "you provided. The response time may vary."
                    )

                except Exception:
                    logger.exception("Unable to save website enquiry.")
                    st.error(
                        "We could not save your enquiry right now. "
                        "Please try again later or contact us by phone."
                    )

    st.divider()
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
            "and desktop screens. The final result depends on testing "
            "and the agreed project scope."
        )

    st.markdown(
        f"""
        <div class="cta-box">
            <h3>📞 Contact Us Directly</h3>
            <p>Call us to discuss your website requirements.</p>
            <a href="tel:{PHONE_NUMBER}" class="phone-link">
                📱 +91 9532991633
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- SALES CHAT ASSISTANT ----------------
with right_col:
    st.subheader("💬 Chat with Our Sales Assistant")
    st.caption(
        "Ask about pricing, features, timelines, or how to book."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 Welcome to our website-making service. "
                    "We offer website packages under ₹2,000. "
                    "What kind of website do you need?"
                ),
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Ask about price, features, or booking..."
    )

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        query = user_input.lower()

        if any(word in query for word in [
            "price", "cost", "how much", "rate", "rupee", "₹", "budget"
        ]):
            reply = (
                "💰 Our advertised website packages are under **₹2,000**. "
                "The final price depends on the features you need. "
                "Domain, hosting, and paid third-party services may "
                "cost extra."
            )

        elif any(word in query for word in [
            "time", "days", "day", "when", "long", "duration", "delivery"
        ]):
            reply = (
                "⏱️ A basic website usually takes an estimated "
                "**3–5 business days** after we receive the required "
                "content. More complex projects can take longer."
            )

        elif any(word in query for word in [
            "book", "order", "buy", "start", "contact", "hire"
        ]):
            reply = (
                "🚀 To get started, fill out the consultation form "
                "on the left, or call **+91 9532991633** to discuss "
                "your requirements."
            )

        elif any(word in query for word in [
            "e-commerce", "ecommerce", "shop", "store",
            "sell", "payment", "product"
        ]):
            reply = (
                "🏪 Yes, we can discuss an e-commerce website with "
                "product listings and ordering features. Payment "
                "gateway setup may require additional configuration "
                "and fees."
            )

        elif any(word in query for word in [
            "mobile", "phone", "screen", "responsive", "tablet"
        ]):
            reply = (
                "📱 Our websites are designed to work on mobile phones, "
                "tablets, and desktops."
            )

        elif any(word in query for word in [
            "support", "maintenance", "help", "after launch"
        ]):
            reply = (
                "🛠️ Basic technical support can be discussed when "
                "booking. Please confirm the included services and "
                "support duration before placing your order."
            )

        elif any(word in query for word in [
            "hello", "hi", "hey", "namaste"
        ]):
            reply = (
                "Hello! 👋 What kind of website would you like us to build?"
            )

        elif any(word in query for word in [
            "portfolio", "personal website", "blog", "business website"
        ]):
            reply = (
                "💼 We can discuss business websites, personal portfolios, "
                "blogs, and landing pages. Tell us what you want your "
                "website to do."
            )

        else:
            reply = (
                "I'd be happy to help! 😊 You can ask about pricing, "
                "delivery time, mobile compatibility, e-commerce, or "
                "booking. For other questions, call **+91 9532991633**."
            )

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        st.rerun()
