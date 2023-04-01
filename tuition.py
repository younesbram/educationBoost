from fpdf import FPDF
import streamlit as st
import openai

# free app, created using vim foot pedals
st.set_page_config(page_title="EducationBoost", page_icon="🤩", layout="centered", initial_sidebar_state="auto", menu_items={
    "Get Help": "https://www.github.com/younesbram/aicomedy",
    "Report a bug": "https://www.younes.ca/contact",
    "About": "# Generative Education!",
},)

# generate a pdf file from a string


def generate_pdf_content(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 5, content)
    return pdf.output(dest="S").encode("latin1")


openai.api_key = st.secrets["OPENAI_API_KEY"]


def generate_course_outline(topic, difficulty):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful, well organized assistant that creates course outlines.  Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it and never mention anything else other than the course outline."},
            {"role": "system", "name": "example_user",
                "content": "I need to create a course outline for my advanced differential equations class."},
            {"role": "system", "name": "example_assistant",
                "content": "Sure, here's a professionally made course outline for your advanced-level differential equations class Course Overview This course focuses on linear differential equations and their applications in science and engineering. Differential Equations are the language in which the laws of nature are expressed. Understanding properties of solutions of differential equations is fundamental to much of contemporary science and engineering."},
            {"role": "system", "name": "example_user",
                "content": "NEVER Mention this again 'Sure, here's a professionally made course outline for your X-level Y class:'. I need to create a course outline for my beginner differential equations class. "},
            {"role": "system", "name": "example_assistant",
                "content": "This course focuses on basic differential equations and their applications in science and engineering. In this course, you'll discover how to speak the language of nature using differential equations. By the end of the course, you'll be able to model simple physical systems, test the plausibility of solutions, visualize solutions using graphs and arrows, make educated guesses, classify critical points, and understand how systems behave - all with the magic of differential equations!"},
            {"role": "system", "name": "example_user",
                "content": "Perfect. Expert Numerical Analysis For Engineering"},
            {"role": "system", "name": "example_assistant",
                "content": "The formulation, methodology, and techniques for numerical solution of engineering problems. Topics covered include: fundamental principles of digital computing and the implications for algorithm accuracy and stability, error propagation and stability, the solution of systems of linear equations, including direct and iterative techniques, roots of equations and systems of equations, numerical interpolation, fundamentals of finite-difference solutions to ordinary differential equations, and error and convergence analysis."},
            {"role": "user", "content": f" {difficulty}  {topic} class. Please use different sizes of headers. Only reply with the course outline, including course goals, and prerequisite topics."},
        ],
        temperature=0.8,
    )
    generatedAdvice = response['choices'][0]['message']['content']
    return generatedAdvice


def generate_assignment(topic, difficulty, assignment_type):
    if assignment_type == "Quiz":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates quizzes. Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it."},
                {"role": "user", "content": f"Pretend you are my professor. Give me a quiz for my {difficulty}-level  {topic} class. My professor is very well trained in his field and in the field of making learning fun and engaging. Make it a professional one that would really help any student"},
            ],
            temperature=0.8,
        )
        generatedAdvice = response['choices'][0]['message']['content']

    elif assignment_type == "Homework":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates homework. Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it."},
                {"role": "user", "content": f"Pretend you are my professor. Give me a homework for my {difficulty}-level  {topic} class. My professor is very well trained in his field and in the field of making learning fun and engaging. Make it a professional one that would really help any student"},
            ],
            temperature=0.8,
        )
        generatedAdvice = response['choices'][0]['message']['content']
    elif assignment_type == "Assignment":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates assignments. Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it."},
                {"role": "user", "content": f"Pretend you are my professor. Give me an assignment for my {difficulty}-level  {topic} class. My professor is very well trained in his field and in the field of making learning fun and engaging. Make it a professional one that would really help any student"},
            ],
            temperature=0.8,
        )
        generatedAdvice = response['choices'][0]['message']['content']

    return generatedAdvice


def generate_lecture(topic, difficulty):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates lectures. Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it. You ONLY respond with the lecture starting with Prof AI:"},
            {"role": "user", "content": f"Pretend you are my professor. Give me a lecture for my {difficulty}-level  {topic} class. My professor is very well trained in his field and in the field of making learning fun and engaging. Make it a long and detailed one that would really help any student"},
        ],
        temperature=0.8,
    )
    generatedAdvice = response['choices'][0]['message']['content']
    return generatedAdvice


def generate_questions(topic, question_type, question_count, difficulty):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful question maker that creates different types of questions. Always remind people of hints to go with their topic. Adapt to the difficulty of the course : either Beginner, Advanced, or Expert but never mention it."},
            {"role": "user", "content": f"Pretend you are my professor. Give me {question_count}  {question_type}-type question for my {difficulty}-level  {topic} class. My professor is very well trained in his field and in the field of making learning fun and engaging. He  ORGANIZES them with newlines and bigger text"},
        ],
        temperature=0.8,
    )
    generatedAdvice = response['choices'][0]['message']['content']
    return generatedAdvice


def generate_content(topic, content_type, assignment_type, difficulty, question_type=None, question_count=None):
    if content_type == "Course Outline":
        return generate_course_outline(topic, difficulty)
    elif content_type == "Assignment":
        return generate_assignment(topic, difficulty, assignment_type)
    elif content_type == "Lecture":
        return generate_lecture(topic, difficulty)
    elif content_type == "Questions":
        return generate_questions(topic, question_type, question_count, difficulty)


st.title("LearnBoost: AI-Powered Education")

difficulty = st.selectbox("Select Difficulty Level",
                          ("Beginner", "Advanced", "Expert"))

topic = st.text_input("Topic", max_chars=130)
content_type = st.selectbox(
    "Content Type", ("Course Outline", "Assignment", "Questions", "Lecture"))
question_type = ["True or False", "Short Answer", "Matching", "Fill in the blank",
                 "Multiple choice", "Coding", "Essay", "Problem-solving", "Case study", "Random real life situation"]
assignment_type = ["Quiz", "Homework", "Assignment"]
question_count = 1

if content_type == "Questions":
    question_type = st.selectbox("Question Type", question_type)
    question_count = st.slider("Number of Questions", 1, 3)
    if question_count > 1 and question_type == "Essay" or question_type == "Case study":
        st.warning(
            "Essay questions & Case studies can only be generated one at a time.")
        question_count = 1

if content_type == "Assignment":
    assignment_type = st.selectbox("Assignment Type", assignment_type)

if st.button("Generate Content"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Please be patient..."):
            content = generate_content(
                topic, content_type, assignment_type, difficulty, question_type, question_count)
            st.write(content)
            st.download_button('Download', content)
            st.markdown(
                "[Donate here](https://donate.stripe.com/dR68x365dgNPaXeaEE)")
            st.markdown(
                "[Request access to GPT4 mode](https://twitter.com/didntdrinkwater)")
