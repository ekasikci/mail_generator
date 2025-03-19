# Mail Generator

Mail Generator is a Python-based application that extracts job postings from career pages and generates tailored job application emails using language models.

## Features

- **Job Extraction:** Extracts job postings from website text.
- **Email Generation:** Crafts personalized job application emails based on the job description and optionally provided CV data.
- **CV Processing:** Supports processing of PDF and DOCX CV documents using [PyPDF2](https://pypi.org/project/PyPDF2/) and [python_docx](https://pypi.org/project/python-docx/).
- **Web Interface:** Uses [Streamlit](https://streamlit.io/) to provide an interactive UI for entering URLs and uploading CVs.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Create and activate a virtual environment:
   ```sh
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit application:
```sh
streamlit run main.py
```
