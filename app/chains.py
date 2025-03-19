import os

import PyPDF2
import docx
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

from utils import clean_text

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.2-90b-vision-preview")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, cv_data=None):
        additional_info = f"### CV DETAILS:\n{cv_data}\n\n" if cv_data else ""
        prompt_email = PromptTemplate.from_template(
            f"""
            ### CONTEXT:
            - **Job Description:** 
              {{job_description}}
            - **CV Details:** 
              {additional_info if additional_info else "No CV details provided."}

            ### INSTRUCTION:
            Using the provided job description and (if available) CV details, craft a concise and compelling job application email. 
            The email should:
            - Be professional and engaging.
            - Highlight relevant skills and experiences tailored to the role.
            - Maintain clarity and readability.
            - Include the following sections:
              1. **Greeting:** Address the hiring manager or recruitment team.
              2. **Opening Statement:** Introduce yourself, specify the position, and express enthusiasm for the opportunity.
              3. **Relevant Background and Skills:** 
                 - Emphasize key qualifications and past experiences that align with the job.
                 - Incorporate details from the CV if provided.
              4. **Closing Statement:** Reaffirm interest, express eagerness for discussion, and include contact details.
              5. **Signature:** Close respectfully with your name and contact information.

            ### OUTPUT:
            Return the email without any preamble or additional commentary.

            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job)})
        return res.content

    def process_cv(self, cv_file):
        if cv_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(cv_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif cv_file.name.endswith('.docx'):
            doc = docx.Document(cv_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")

        # Simple text cleaning (customize this as needed)
        return text

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))