import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define a list of random crop facts(Did You Know?)
crop_facts = [
    "Maize is one of the oldest cultivated crops, dating back thousands of years.",
    "Beans are an excellent source of fiber, vitamins, and minerals.",
    "Rice is the primary food source for over half of the world's population.",
    "Tanzania is one of the top maize-producing countries in Africa.",
    "Beans are often called the 'poor man's meat' due to their high protein content.",
    "Beans, rice, and maize are vital staples in Tanzanian cuisine.",
    "Beans are a good source of protein, a dietary essential in Tanzania.",
    "Rice is commonly enjoyed as one of the main dish in Tanzanian meals.",
    "Beans are often used in Tanzanian stews and soups.",
    "Maize is used to make ugali, a popular Tanzanian dish.",
    "Beans are commonly used in Tanzanian street food.",
    "Rice is a key ingredient in Tanzanian biryani dishes.",
    "Rice is a primary crop in the Morogoro region of Tanzania.",
    "Rice paddies provide habitat for diverse bird species in Tanzania.",
]

# Function to send feedback via email
def send_feedback_email(user_name, user_email, user_feedback):
    # Email configuration
    sender_email = "jamesloma80@gmail.com"
    sender_password = "Monnie19#"
    recipient_email = "lisakatani1008@gmail.com"

    # Create the email message
    subject = "User Feedback from Crop Price Prediction App"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the feedback content
    message.attach(MIMEText(f"User: {user_name}\nEmail: {user_email}\n\nFeedback:\n{user_feedback}", "plain"))

    # Send the email
    #try:
    #  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    #       server.login(sender_email, sender_password)
    #       server.sendmail(sender_email, recipient_email, message.as_string())
    #except Exception as e:
    #   st.error("Error sending email. Please try again later.")  # Display an error message to the user

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        pass  # Do nothing if an error occurs, no error message will be displayed


# Function to create sharing links
def create_share_links(text):
    # Twitter sharing link
    twitter_url = f"https://twitter.com/intent/tweet?text={text}"
    twitter_icon = ""
    twitter_button = f'<a href="{twitter_url}" title="Share on Twitter" target="_blank" rel="noopener noreferrer"><button>{twitter_icon} Twitter</button></a>'
    
    # WhatsApp sharing link
    whatsapp_url = f"https://wa.me/?text={text}"
    whatsapp_icon = ""
    whatsapp_button = f'<a href="{whatsapp_url}" title="Share on WhatsApp" target="_blank" rel="noopener noreferrer"><button>{whatsapp_icon} WhatsApp</button></a>'
    
    # Instagram sharing link
    instagram_url = f"https://www.instagram.com/?text={text}"
    instagram_icon = ""
    instagram_button = f'<a href="{instagram_url}" title="Share on Instagram" target="_blank" rel="noopener noreferrer"><button>{instagram_icon} Instagram</button></a>'
    
    return f"{twitter_button} | {whatsapp_button} | {instagram_button}"



def create_home_page():
    st.markdown('<div style="background-color: #4CAF50; color: white; padding: 10px 0; box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1); display: flex; align-items: center; justify-content: center;">', unsafe_allow_html=True)
    st.image('logo.jpg', width=100)
    st.title("Welcome to the Crop Price Prediction App")
    st.write("This is the home page of the dashboard. You can use the sidebar navigation to access other pages.")

    # Informational section
    st.markdown('<div align="center">', unsafe_allow_html=True)
    st.markdown("### Crop Price Prediction")
    st.write("Our dashboard provides valuable insights into crop prices.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Crop images in three columns
    col1, col2, col3 = st.columns(3)

    # Define crop images
    crop_images = {
        "Maize": "maize.jpg",
        "Beans": "beans.jpg",
        "Rice": "rice.jpg"
    }

    # Display crop images in columns
    with col1:
        st.image(crop_images["Maize"], width=400,  caption="Maize")
    with col2:
        st.image(crop_images["Beans"], width=400, caption="Beans")
    with col3:
        st.image(crop_images["Rice"], width=400, caption="Rice")

    crop_data = {
        "Maize": {
            "icon": "🌽",
            "help": "Click to Learn More About Maize",
            "info": "Maize is a staple crop in Tanzania with a current price of 1,014 TZS per kg.",
            "conditions": "Maize thrives in well-drained soil and requires moderate rainfall and sunlight.",
            "common_growing_regions": "Common regions for maize cultivation in Tanzania include Arusha and Kilimanjaro.",
            "uses": "Maize is used for various purposes, including human consumption, animal feed, and industrial processing."
        },
        "Beans": {
            "icon": "🌱",
            "help": "Click to Learn More About Beans",
            "info": "Beans are a nutritious crop with a current price of 2,567 TZS per kg.",
            "conditions": "Beans grow well in regions with consistent rainfall and moderate temperatures.",
            "common_growing_regions": "Common regions for beans cultivation in Tanzania include Mbeya and Iringa.",
            "uses": "Beans are a good source of protein and are consumed in various dishes in Tanzanian cuisine."
        },
        "Rice": {
            "icon": "🍚",
            "help": "Click to Learn More About Rice",
            "info": "Rice is a widely consumed crop with a current price of 2,415 TZS per kg.",
            "conditions": "Rice requires flooded fields for cultivation and is grown in regions like Morogoro and Shinyanga.",
            "common_growing_regions": "Common regions for rice cultivation in Tanzania include Morogoro and Shinyanga.",
            "uses": "Rice is a staple food in Tanzania and is consumed in various forms, including steamed rice and rice-based dishes."
        }
    }

    for crop_name, crop_info in crop_data.items():
        with col1 if crop_name == "Maize" else col2 if crop_name == "Beans" else col3:
            if st.button(f"{crop_info['icon']} {crop_name}", help=crop_info["help"]):
                st.write(crop_info["info"])
                st.markdown(f"**Favorable Conditions in Tanzania:** {crop_info['conditions']}")
                st.markdown(f"**Common Growing Regions:** {crop_info['common_growing_regions']}")
                st.markdown(f"**Uses:** {crop_info['uses']}")

    # Random Crop Fact section
    st.markdown('<div align="center">', unsafe_allow_html=True)
    st.markdown("### Did You Know?")
    if st.button("Generate"):
        random_fact = random.choice(crop_facts)
        st.info(f"Crop Fact: {random_fact}")
        st.markdown("### Share this Fact")
        share_links = create_share_links(random_fact)
        st.markdown(share_links, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback and contact
    st.markdown('<div align="center">', unsafe_allow_html=True)
    st.markdown("### Feedback & Contact")
    st.write("We value your feedback. If you have any questions or suggestions, please contact us at connect@dlab.or.tz or send us your feedback through feedback form below 👇")
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback Form
    st.markdown('<div align="center">', unsafe_allow_html=True)
    st.markdown("### Feedback Form")
    st.write("Your feedback is important to us! Please fill out the form below to share your thoughts.")

    # Add input fields for user's name, email, feedback, and suggestions
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    user_feedback = st.text_area("Feedback and Suggestions", height=150)

    # Create a button to submit feedback
    if st.button("Submit Feedback"):
        # Check if required fields are not empty
        if not user_name or not user_email or not user_feedback:
            st.warning("Please fill out all fields before submitting feedback.")
        else:
            # Process and store the user's feedback
            send_feedback_email(user_name, user_email, user_feedback)
            st.success("Thank you for your feedback! We've received your input and will make improvements accordingly.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Create two columns for dLab information and development team credits
    col1, col2 = st.columns(2)

    # dLab Tanzania information
    with col1:
        st.markdown('---')
        st.image('dlab_logo.png', width=100)
        st.write("dLab Tanzania")
        st.write("Address Line: P. O. Box 33335, DSM")
        st.write("Email Address: connect@dlab.or.tz")
        st.write("Phone Number: 0225 222 410 645 / 0222 410 690")

    # Development team credits
    with col2:
        st.markdown('---')
        st.markdown("### Development Team")
        st.write("Meet the talented individuals who made this app possible:")
        st.write("- Basilisa Katani, Email: lisakatani1008@gmail.com")
        st.write("- James Loma, Email: jamesloma80@gmail.com")
        st.write("- Geoffrey Muchunguzi, Email: geoffreymuchunguzi@gmail.com")
        st.write("- Juma Omar, Email: jumaomar97@gmail.com")
        st.write("We appreciate their dedication and creativity in making this app extraordinary!")

create_home_page()
