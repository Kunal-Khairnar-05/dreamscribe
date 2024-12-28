import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key= st.secrets["gemini_api_key"])
model = genai.GenerativeModel("gemini-1.5-flash")

img = Image.open("DREAMSCRIBE.png")


def generate_story(concept, target_audience):
    """Generate a learning story based on the provided concept and audience."""
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    {"text": f"You are a Story Generator, your job is to simplify the given concept using story which students can remember during their exams and from that story they can identify key components and describe them briefly in exam paper. Generate a story about '{concept}' for {target_audience}."}
                ],
            },
        ]
    )
    result = chat_session.send_message(f"Concept: {concept}, Target Audience: {target_audience}")
    return result.text

# Streamlit UI
st.title("DREAMSCRIBE 💭📝")

st.image(
    img,
    caption="Generate Learning from Stories for Students",
    width=300
)

concept = st.text_input("Enter the Concept", placeholder="e.g., Photosynthesis, Quick Sort")
target_audience = st.text_input("Enter the Target Audience", placeholder="e.g., High School, Engineering Students")

if st.button("Generate Story"):
    if concept and target_audience:
        with st.spinner("Generating story..."):
            try:
                story = generate_story(concept, target_audience)
                st.success("Story generated successfully!")
                st.subheader("Generated Story:")
                st.write(story)
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide both the concept and target audience.")

# Adding Follow up Questions
st.subheader("Follow-up Questions")
question1 = st.text_input("Question 1", placeholder="e.g., Can you explain xyz part briefly?")

if st.button("Generate Answer"):
    if question1:
        with st.spinner("Generating answer..."):
            try:
                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                {"text": f"You are a Student, you have read the story about '{concept}' for {target_audience}. Now, you have to answer the following question: {question1}."}
                            ],
                        },
                    ]
                )
                result = chat_session.send_message(f"Question: {question1}")
                answer = result.text
                st.success("Answer generated successfully!")
                st.subheader("Generated Answer:")
                st.write(answer)
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide the question.")

st.caption("Kunal Khairnar | SINIXCODE © 2024")
