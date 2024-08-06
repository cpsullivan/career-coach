'''
This file combines code from career_advisor.py, cover_letter.py, and resume_polisher.py into a single user interface
'''

# Import necessary packages
from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

# Function to polish the résumé
def polish_resume(position_name, resume_content, job_description, polish_prompt=""):
    # Function to compare the résumé with the job description and polish it
    prompt = (
        f"Improve the following résumé content: '{resume_content}' to better align with the requirements and expectations of a {position_name} position, "
        f"taking into account the job description: '{job_description}'. Return the polished version, highlighting necessary adjustments. {polish_prompt}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a human-resource professional and job coach that evaluates and improves résumés."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        polished_resume = response.choices[0].message.content
        return polished_resume
    except Exception as e:
        return f"Error generating polished résumé: {e}"

# Function to generate a customized cover letter
def generate_cover_letter(company_name, position_name, job_description, resume_content):
    # Craft the prompt for the model to generate a cover letter
    prompt = (
        f"Generate a customized cover letter using the company name: {company_name}, "
        f"the position applied for: {position_name}, and the job description: {job_description}. "
        f"Ensure the cover letter highlights my qualifications and experience as detailed in the résumé content: {resume_content}. "
        "Adapt the content carefully to avoid including experiences not present in my résumé but mentioned in the job description. "
        "The goal is to emphasize the alignment between my existing skills and the requirements of the role."
    )

    try:
        generated_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional assistant who writes personalized cover letters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        # Extract the generated text
        cover_letter = generated_response.choices[0].message.content
        return cover_letter
    except Exception as e:
        return f"Error generating cover letter: {e}"

# Function to generate career advice
def generate_career_advice(position_applied, job_description, resume_content):
    # The prompt for the model
    prompt = (
        f"Considering the job description: {job_description}, and the résumé provided: {resume_content}, "
        f"identify areas for enhancement in the résumé. Offer specific suggestions on how to improve these aspects "
        f"to better match the job requirements and increase the likelihood of being selected for the position of {position_applied}."
    )

    try:
        # Generate response
        generated_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career advisor who provides insightful suggestions for improving résumés based on job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )

        # Extract and format the generated text
        advice = generated_response.choices[0].message.content
        return advice
    except Exception as e:
        return f"Error generating career advice: {e}"

# Create the Gradio interface with tabs
def create_interface():
    # Shared inputs
    inputs = [
        gr.Textbox(label="Position Applied For", placeholder="Enter the name of the position...", elem_id="position_name"),
        gr.Textbox(label="Company Name", placeholder="Enter the name of the company...", elem_id="company_name"),
        gr.Textbox(label="Job Description Information", placeholder="Paste the job description here...", lines=10, elem_id="job_description"),
        gr.Textbox(label="Your Résumé Content", placeholder="Paste your résumé content here...", lines=10, elem_id="resume_content"),
        gr.Textbox(label="Polish Instruction (Optional)", placeholder="Enter specific instructions or areas for improvement (optional)...", lines=5, elem_id="polish_instruction"),
    ]

    # Define the Gradio interface with tabs
    interface = gr.Blocks()

    with interface:
        gr.Markdown("## Career Coach Application")
        gr.Markdown(
            "This application provides three services: Résumé Polishing, Cover Letter Generation, and Career Advice. "
            "Enter your information once, and access the different services through the tabs."
        )
        with gr.Tabs():
            with gr.Tab("Résumé Polisher"):
                gr.Interface(
                    fn=polish_resume,
                    inputs=[inputs[0], inputs[3], inputs[2], inputs[4]],  # Position, Résumé, Job Description, Polish Instructions
                    outputs=gr.Textbox(label="Polished Résumé"),
                    title="Résumé Polisher",
                    description="Get a polished version of your résumé by aligning it with the job description."
                )
            with gr.Tab("Cover Letter Generator"):
                gr.Interface(
                    fn=generate_cover_letter,
                    inputs=[inputs[1], inputs[0], inputs[2], inputs[3]],  # Company, Position, Job Description, Résumé
                    outputs=gr.Textbox(label="Customized Cover Letter"),
                    title="Cover Letter Generator",
                    description="Generate a customized cover letter based on your résumé and the job description."
                )
            with gr.Tab("Career Advisor"):
                gr.Interface(
                    fn=generate_career_advice,
                    inputs=[inputs[0], inputs[2], inputs[3]],  # Position, Job Description, Résumé
                    outputs=gr.Textbox(label="Career Advice"),
                    title="Career Advisor",
                    description="Receive career advice to improve your résumé and increase your chances of getting the job."
                )

    return interface

# Launch the combined application
if __name__ == "__main__":
    app = create_interface()
    app.launch()
