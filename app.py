import streamlit as st
from google import genai
import os

# Configure the landing page
st.set_page_config(
    page_title="Affordable Website Maker", 
    page_icon="🌐", 
    layout="wide"
)

# Initialize the Gemini client securely
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

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
    .form-container {
        background-color: #F9FAFB;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)

# Main layout split into Left (Content & Forms) and Right (AI Sales Chatbot)
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

    # Lead Capture Form linked directly to your email notification
    st.subheader("📩 Get a Free Consultation Call")
    st.caption("Fill out this form to send your details directly to our team.")
    
    # CHANGE 'YOUR_EMAIL@gmail.com' BELOW TO YOUR ACTUAL EMAIL ADDRESS
    form_html = """
    <form action="https://formsubmit.co" method="POST" class="form-container">
        <input type="hidden" name="_next" value="https://streamlit.io">
        <div style="margin-bottom: 12px;">
            <label style="font-weight:bold; display:block; margin-bottom:5px;">Your Name*</label>
            <input type="text" name="name" required placeholder="Enter your full name" style="width:100%; padding:8px; border-radius:4px; border:1px solid #ccc;">
        </div>
        <div style="margin-bottom: 12px;">
            <label style="font-weight:bold; display:block; margin-bottom:5px;">Your Phone Number*</label>
            <input type="tel" name="phone" required placeholder="Enter your 10-digit mobile number" style="width:100%; padding:8px; border-radius:4px; border:1px solid #ccc;">
        </div>
        <div style="margin-bottom: 12px;">
            <label style="font-weight:bold; display:block; margin-bottom:5px;">Website Type</label>
            <select name="website_type" style="width:100%; padding:8px; border-radius:4px; border:1px solid #ccc;">
                <option>Business Landing Page</option>
                <option>E-commerce Store</option>
                <option>Personal Portfolio</option>
                <option>Blog</option>
                <option>Other</option>
            </select>
        </div>
        <div style="margin-bottom: 16px;">
            <label style="font-weight:bold; display:block; margin-bottom:5px;">Project Requirements</label>
            <textarea name="requirements" rows="3" placeholder="Briefly describe your business..." style="width:100%; padding:8px; border-radius:4px; border:1px solid #ccc;"></textarea>
        </div>
        <button type="submit" style="background-color:#2563EB; color:white; border:none; padding:10px 20px; font-size:16px; font-weight:bold; border-radius:6px; cursor:pointer; width:100%;">
            Submit Requirements 🚀
        </button>
    </form>
    """
    st.markdown(form_html, unsafe_allow_html=True)

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
    st.subheader("💬 Ask Our AI Assistant")
    st.caption("Get immediate answers about pricing, timelines, features, and technical details.")
    
    # Setup AI Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI assistant. Want to get a stunning website for your business at just ₹2,000? Ask me anything about our services!"}
        ]

    # Show existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle New Chat Input
    if user_input := st.chat_input("Ask about our website services..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            if client:
                try:
                    system_prompt = (
                        "You are an expert sales representative for an affordable web design agency. "
                        "The agency builds high-quality, professional, mobile-friendly landing pages and business websites for under 2,000 Indian Rupees (₹2,000). "
                        "Always be extremely professional, polite, helpful, and focused on convincing the client to order a website. "
                        "If the customer wants to book a project, tell them to call the direct official phone number: 9532991633 or fill out the form on the left. "
                        "Keep your responses concise, sharp, and easy to read."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"{system_prompt}\n\nCustomer: {user_input}"
                    )
                    ai_reply = response.text
                    placeholder.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    placeholder.error(f"Error: {e}")
            else:
                reply = "I'm ready to answer! Please make sure your GEMINI_API_KEY environment variable is configured to activate live cloud responses."
                placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
