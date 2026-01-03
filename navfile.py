from fastapi import HTTPException, Response
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image
import mein, ollama_handler, session_logic, setup_variables, ui
import requests
import report_gen

st.set_page_config(layout="wide")


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
      with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("/Users/kishl/Downloads/My Projects/Portfolio/Style/style.css")

lottie_contact = load_lottie("https://lottie.host/56cb3b62-fd1b-46bd-b372-40b76789e182/5dVrec5D7A.json")
gym_img = Image.open("/Users/kishl/OneDrive/Pictures/animategym.webp")


def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://cdn.pixabay.com/photo/2024/03/01/12/27/ai-generated-8606462_1280.jpg");
             background-size: cover
         }}
         </style>
             
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()


with st.container():
        
    st.write("##")
    st.subheader("Hey there :wave:")
    st.title("Welcome to Fitness Arena")
    st.write("""Go through the profile to explore the daily diet routine.
                Focus on improving your health, continuously rededine the planning.
                You can access chatbots to guide you for better fitness ideas and planning.""")
    st.write("---")

with st.container():
        with st.sidebar:
            selected = option_menu(
                                    menu_title= "Main Menu",
                                    options= ['About','Fitness Report','Chatbot','Contact'],
                                    icons=['person','code-slash','','chat-left-text-fill']
                                )
if selected == "About":
        with st.container():
             col1, col2 = st.columns(2)
             with col1:
                  st.write("##")
                  st.subheader("YOUR FITNESS PARNTER")
                  st.write("##")
            
        st.write("""
                  This is your fitness partner involves building a chatbot, which is powered by Ollama package, functions and is based on the ReAct (Reasoning and Acting) framework.
                  It is designed to deliever nutritional information and advice, achieving this by interpreting user’s dietary habits and integrating an API of nutritional data.""")
        
        st.write("---")
        with st.container():
              col3, col4 = st.columns(2)
              with col3:
                    st.subheader(":violet[Why Chatbots]", divider='rainbow')
                    st.write("""
                    - **Create a personalized fitness or nutrition plan**
                        - You can provide your personal details. It can help you create a personalised report for you.
                        - Further, you can use the report to make a plan for improving your health and diet plans.
                    - **Provide educational content related to the chatbot primary purpose**
                        - Used the latest trending technologies for providing accurate responses which you can rely on.
                        - You can get various tips and hints, links to articles, embedded videos, and images.
                        - The integrated chatbot enhances the productivity by training the chatbot on personalised data.
                    - **Motivate through encouraging and congratulatory messages**
                        - Stay healthy and focused with preplaned exercises.
                        - Get a star as a token of appreciation after completeing your task.
                    """)
              with col4:
                    st.image(gym_img)


        st.write("---")
        st.write("##")

if selected == "Fitness Report":
        with st.container():
            st.subheader("Your Caring Planner")
            st.write("##")
        # Configure the API endpoint
        API_URL = "http://127.0.0.1:8000/api"  # Replace with your actual API endpoint

        # Function to call the API to generate a workout plan
        def generate_workout_plan(plan_type, duration, intensity):
            pdf_data = report_gen.create_workout_plan_pdf()
            response = Response(content=pdf_data, media_type="application/pdf")
            if response.status_code == 200:
                with open("workout_plan.pdf", "wb") as f:
                    f.write(pdf_data)
                return "workout_plan.pdf"
            else:
                return None

        # Function to call the API to generate a meal plan
        def generate_meal_plan(calories, diet_type):
            pdf_data = report_gen.create_meal_plan_pdf()
            response = Response(content=pdf_data, media_type="application/pdf")
            if response.status_code == 200:
                with open("meal_plan.pdf", "wb") as f:
                    f.write(pdf_data)
                return "meal_plan.pdf"
            else:
                return None
            # return response.json()

        # Function to call the API to generate a health report
        def generate_health_report(user_data):
            pdf_data = report_gen.create_health_plan_pdf()
            response = Response(content=pdf_data, media_type="application/pdf")
            if response.status_code == 200:
                with open("health_plan.pdf", "wb") as f:
                    f.write(pdf_data)
                return "health_plan.pdf"
            else:
                return None
        
        
        def weekday_dict(days):
            for day in days:
                {day : [].append()}

        # Streamlit sidebar for navigation
        st.sidebar.title("Fitness Planning AI")
        menu = st.sidebar.radio("Select a feature", ("Workout Plan", "Meal Plan", "Health Report"))

        if menu == "Workout Plan":
            st.title("Generate a Workout Plan")
            plan_type = st.selectbox("Plan Type", ["Cardio", "Strength", "Flexibility", "Balance"])
            duration = st.slider("Duration (minutes)", 10, 120, 30)
            intensity = st.selectbox("Intensity", ["Low", "Moderate", "High"])
            
            if st.button("Generate Workout Plan"):
                workout_pdf = generate_workout_plan(plan_type, duration, intensity)
                if workout_pdf:
                    st.success(f"PDF Workout Plan generated: {workout_pdf}")
                    st.download_button(label="Download PDF", data=open(workout_pdf, "rb"), file_name="workout_plan.pdf", mime="application/pdf")
                else:
                    st.error("Failed to generate PDF workout plan")

        elif menu == "Meal Plan":
            st.title("Generate a Meal Plan")
            calories = st.number_input("Calories", min_value=1200, max_value=4000, value=2000, step=100)
            diet_type = st.selectbox("Diet Type", ["Standard", "Vegetarian", "Vegan", "Keto", "Paleo"])
            
            if st.button("Generate Meal Plan"):
                meal_pdf = generate_meal_plan(calories, diet_type)
                if meal_pdf:
                    st.success(f"PDF Meal Plan generated: {meal_pdf}")
                    st.download_button(label="Download PDF", data=open(meal_pdf, "rb"), file_name="meal_plan.pdf", mime="application/pdf")
                else:
                    st.error("Failed to generate PDF meal plan")

                

        elif menu == "Health Report":
            st.title("Generate a Health Report")
            age = st.number_input("Age", min_value=10, max_value=100, value=30)
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            if st.button("Generate Health Report"):
                user_data = {
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "activity_level": activity_level,
                    "gender": gender
                }
                health_pdf = generate_health_report(user_data)
                if health_pdf:
                    st.success(f"PDF Health Plan generated: {health_pdf}")
                    st.download_button(label="Download PDF", data=open(health_pdf, "rb"), file_name="health_plan.pdf", mime="application/pdf")
                else:
                    st.error("Failed to generate PDF health plan")
            
if selected == "Chatbot":
        mein.chat_history()

if selected == "Contact":
        st.header("Get In Touch With Me!")
        st.write("##")
        st.write("##")

        contact_form = """
        <form action="https://formsubmit.co/kkishlay9142@gmail.com" method="POST">
        <input type = "hidden" name ="_captcha" value = "false">
        <input type="text" name="name" placeholder = "Your name" required>
        <input type="email" name="email" placeholder = "Your email" required>
        <textarea name = "message" placeholder = "Your message" required></textarea>
        <button type="submit">Send</button>
        </form>
        """
        left_col, right_col = st.columns((2,1))
        with left_col:
                st.markdown(contact_form, unsafe_allow_html= True)
        with right_col:
                st_lottie(lottie_contact,height=245,width=450)