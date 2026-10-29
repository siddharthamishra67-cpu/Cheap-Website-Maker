import streamlit as st

# Configure the landing page layout cleanly
st.set_page_config(
    page_title="Affordable Website Maker", 
    page_icon="🌐", 
    layout="wide"
)

# Custom styling for a professional tech agency look
st.markdown("""
    <style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 22px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .price-tag {
        background-color: #DCFCE7;
        color: #15803D;
        font-size: 28px;
        font-weight: 700;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #22C55E;
        margin-bottom: 40px;
    }
    .cta-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .phone-link {
        font-size: 32px;
        font-weight: 800;
        color: #2563EB;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# Main layout split into Left (Content & Forms) and Right (AI Sales Assistant)
left_col, right_col = st.columns([1.2, 1])

with left_col:
    # Header & Hero Area
    st.markdown('<div class="main-title">🚀 Need a Professional Website?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Get your business online with a stunning, high-speed landing page.</div>', unsafe_allow_html=True)
    st.markdown('<div class="price-tag">💰 Special Offer: Full Website Under ₹2,000 Only!</div>', unsafe_allow_html=True)
    
    # Features List
    st.subheader("🛠️ What We Offer:")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown("✅ **Modern & Clean UI Designs**")
        st.markdown("✅ **100% Mobile & Tablet Responsive**")
        st.markdown("✅ **Lightning Fast Page Speeds**")
    with f_col2:
        st.markdown("✅ **Google Maps & Contact Forms**")
        st.markdown("✅ **Social Media Link Setup**")
        st.markdown("✅ **Free Lifetime Technical Support**")
        
    st.markdown("---")
    
    # Portfolio Section
    st.subheader("📁 Our Design Samples")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.info("🏪 **E-Commerce / Business Site**\n\nClean product cards, easy navigation, and instant checkout setups.")
    with p_col2:
        st.info("💼 **Portfolio / Landing Page**\n\nBold typography, smooth animations, and high lead-conversion forms.")

    st.markdown("---")

    # Lead Capture Form processed natively without connection blocks
    st.subheader("📩 Get a Free Consultation Call")
    st.caption("Fill out this form to send your details directly to our team.")

    with st.form("consultation_form", clear_on_submit=True):
        client_name = st.text_input("Your Name*", placeholder="Enter your full name")
        client_phone = st.text_input("Your Phone Number*", placeholder="Enter your 10-digit mobile number")
        web_type = st.selectbox("Website Type", ["Business Landing Page", "E-commerce Store", "Personal Portfolio", "Blog", "Other"])
        requirements = st.text_area("Project Requirements", placeholder="Briefly describe your business details...")
        
        submit_btn = st.form_submit_button("Submit Requirements 🚀")
        
        if submit_btn:
            if not client_name or not client_phone:
                st.error("Please fill out your Name and Phone Number so we can reach you!")
            else:
                try:
                    import gspread
                    import requests
                    
                    # Cleanly authorize the session for a public web request link
                    gc = gspread.Client(auth=None, session=requests.Session())
                    sheet = gc.open_by_url(st.secrets["spreadsheet_url"]).sheet1
                    
                    # Append the form entries into the spreadsheet columns
                    sheet.append_row([client_name, client_phone, web_type, requirements])
                    st.success(f"Thank you {client_name}! Your requirements have been logged safely. Our team will call you at {client_phone} within 2 hours.")
                except Exception as e:
                    st.error(f"Failed to log message: {e}. Please ensure the sheet sharing is set to 'Anyone with the link can Edit'.")

    st.markdown("---")

    # Frequently Asked Questions (FAQ) Section
    st.subheader("🤔 Frequently Asked Questions")
    with st.expander("⏱️ How long does it take to make the website?"):
        st.write("We deliver your fully completed, mobile-friendly landing page website within 3 to 5 business days after receiving your initial contents.")
        
    with st.expander("💸 Are there any hidden fees or extra costs?"):
        st.write("No hidden layout charges. The base design is strictly under ₹2,000. If you require premium custom domains (.com/.in) or hosting setups, we can add them at actual base cost.")
        
    with st.expander("📱 Will my website work properly on mobile screens?"):
        st.write("Absolutely. Every site we build is 100% mobile responsive and engineered to look gorgeous on iPhones, Android devices, tablets, and laptops.")

    # Call to Action Box
    st.markdown(
        """
        <div class="cta-box">
            <h3>📞 Call Us Directly for Fast Booking</h3>
            <p style="font-size: 16px; color: #4B5563;">Tap the number below to talk to a human expert right now!</p>
            <a href="tel:+919532991633" class="phone-link">📱 +91 9532991633</a>
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
            st.markdown(msg["content"])

    # Process localized dialog query replies securely
    if user_input := st.chat_input("Ask about pricing, timeline, booking..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        query = user_input.lower()
        with st.chat_message("assistant"):
            if "price" in query or "cost" in query or "how much" in query or "rate" in query or "rupee" in query or "₹" in query:
                reply = "Our premium business website package is strictly under **₹2,000** completely! This includes a modern user interface design, mobile responsiveness, and lifetime free basic support. No hidden maintenance charges."
            elif "time" in query or "day" in query or "when" in query or "long" in query or "duration" in query:
                reply = "We complete and publish your business website within **3 to 5 business days** once you send us your layout text details and pictures!"
            elif "book" in query or "order" in query or "buy" in query or "start" in query or "contact" in query:
                reply = "Fantastic! To book your website right away, please **fill out the lead consultation form on the left** with your name and phone number, or call our team directly at **+91 9532991633**. We will contact you instantly!"
            elif "e-commerce" in query or "shop" in query or "store" in query or "sell" in query:
                reply = "Yes, we specialize in building clean, high-speed **E-commerce Stores**! We can set up clear product showcase cards, smooth payment button redirections, and easy navigation pathways to help you sell items easily."
            elif "mobile" in query or "phone" in query or "screen" in query or "responsive" in query:
                reply = "Every single website we build is engineered to look beautiful and function perfectly on all smart devices, including Android phones, iPhones, tablets, iPads, and computer screens."
            else:
                reply = "I would love to help you get your business online for just **₹2,000**! We provide custom landing pages, portfolios, and e-commerce setups with free tech support. To discuss your precise requirements or book a project, please fill out the intake form on the left or call us directly at **+91 9532991633**!"
                
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
