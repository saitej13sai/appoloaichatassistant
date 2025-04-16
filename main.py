import streamlit as st
import google.generativeai as genai

# ==== CONFIG ====
genai.configure(api_key="AIzaSyDUvbyMHm5M5fkQXR5itUALhMH5XqQ4FRs")  # Replace with your actual key
model = genai.GenerativeModel("gemini-1.5-pro")
# ================

appointments = []

hospital_context = """
Apollo Hospitals is one of Asia's leading healthcare providers, offering a wide range of medical services, specialties, and world-class facilities.

🩺 Departments and Specialties:
- Cardiology (Heart Care)
- Neurology (Brain & Nervous System)
- Orthopedics (Bone & Joint Care)
- Oncology (Cancer Care)
- Pediatrics (Child Health)
- Gynecology and Obstetrics (Women’s Health)
- Nephrology (Kidney Care)
- Gastroenterology (Digestive Health)
- Urology (Urinary System)
- Dermatology (Skin Care)
- Psychiatry and Mental Wellness
- ENT (Ear, Nose & Throat)
- General Medicine and Surgery

🧑‍⚕️ Prominent Doctors:
- Dr. Ramesh Babu – Cardiologist
- Dr. Anjali Mehra – Gynecologist
- Dr. Ravi Kumar – Neurologist
- Dr. Sandeep Verma – Orthopedic Surgeon
- Dr. Meenakshi Rao – Pediatrician

📅 Appointment Timings:
- Outpatient services: 8:00 AM to 8:00 PM, Monday to Saturday.
- Emergency services: 24/7

🏥 Facilities:
- Advanced diagnostic labs, MRI/CT scans
- In-patient wards & private rooms
- Online consultation & telemedicine
- Pharmacy & ambulance services
- Preventive care & health check-up packages

📍 Locations:
Branches in Chennai, Delhi, Hyderabad, Bengaluru, Mumbai, and more.

📞 Helpline:
24/7 helpline: 1860-500-1066
Website: www.apollohospitals.com

Note: This assistant is for support only, not emergency advice.
"""

def book_appointment(name, date, time, specialty):
    appointments.append({
        "name": name,
        "date": date,
        "time": time,
        "specialty": specialty
    })
    return f"✅ Appointment booked for {name} on **{date}** at **{time}** with a **{specialty}** specialist."

# === Streamlit UI ===
st.title("🩺 Apollo Hospital AI Assistant")

if "name" not in st.session_state:
    st.session_state.name = ""

if not st.session_state.name:
    st.session_state.name = st.text_input("👋 Hello! What is your name?", placeholder="Enter your name")

if st.session_state.name:
    st.markdown(f"Hi **{st.session_state.name}**, welcome to Apollo Hospital Assistant.")
    issue = st.text_input("🤒 What health issue or symptom are you facing?", placeholder="e.g., chest pain, fever, headache")

    if issue:
        st.write("📋 Here's a brief about your issue and guidance:")
        prompt = (
            f"You are a helpful medical assistant at Apollo Hospital. "
            f"User's symptom/problem: {issue}. In around 120 words, explain what this issue could be, "
            f"which department might help, and if necessary, suggest booking an appointment. Keep it simple and calm.\n"
            f"{hospital_context}"
        )
        response = model.generate_content(prompt).text
        st.success(response)

        if st.checkbox("✅ Would you like to book an appointment?"):
            date = st.text_input("📅 When would you like the appointment?", placeholder="e.g., Tomorrow, 20th April, next Monday")
            time = st.text_input("⏰ At what time?", placeholder="e.g., 10 AM, afternoon, evening, 5")

            specialty = st.selectbox("🩺 Select Department", [
                "Cardiology", "Neurology", "Orthopedics", "Oncology", "Pediatrics", "Gynecology",
                "Nephrology", "Gastroenterology", "Urology", "Dermatology",
                "Psychiatry", "ENT", "General Medicine"
            ])

            if st.button("📌 Book Appointment"):
                confirmation = book_appointment(st.session_state.name, date, time, specialty)
                st.success(confirmation)

    st.markdown("---")
    st.markdown("🔁 Refresh the page to restart or change details.")
