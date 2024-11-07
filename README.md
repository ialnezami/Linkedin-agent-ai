# Linkedin-agent-ai

Here’s a sample README file for your project:

---

# LinkedIn Post Generator

This project automates LinkedIn post generation and posting by using **Selenium** for web scraping and posting, and **Ollama** for generating text using the LLaMA 3 model. It simulates a software engineer persona for text generation to create professional and engaging LinkedIn posts.

## Features

- **Automated LinkedIn Posting**: Post content to LinkedIn automatically using saved cookies (after initial manual login).
- **Text Generation via LLaMA 3 Model**: Generate text for LinkedIn posts based on a software engineer persona using Ollama's LLaMA 3 model.

## Requirements

Before running the project, make sure you have the following installed:

- **Ollama**: [Download and Install Ollama](https://ollama.com/download)
- **Python** (version 3.x recommended)
- **ChromeDriver** (for Selenium, corresponding to your installed Chrome version)

### Python Dependencies

Install the required Python libraries with the following command:

```bash
pip install -r requirements.txt
```

The required libraries are:

- `selenium`: For web scraping and automation with LinkedIn.
- `Pillow`: For image manipulation (if used in your project).
- `reportlab`: For generating PDF files (if used in your project).
- `ollama`: For generating text using the LLaMA 3 model.

## Setup Instructions

### 1. Install Dependencies

Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/ialnezami/Linkedin-agent-ai.git
cd Linkedin-agent-ai
```

Then, install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Make sure you have Ollama installed on your system to use the LLaMA 3 model for text generation. You can download Ollama from the official site:

- [Ollama Installation](https://ollama.com/download)

### 3. Manual Login (First Run)

On the first run, you need to log in manually to LinkedIn. This step will save your login session cookies, allowing the script to log in automatically on future runs.

Run the project, and follow the prompts to log into your LinkedIn account. Once logged in, the session cookies will be saved for automatic login in subsequent runs.

### 4. Running the Project

After the initial manual login and saving the cookies, you can run the project automatically by executing the script:

```bash
python main.py
```

### 5. Automating the Process

Once the cookies are saved, the project will automatically log in to LinkedIn for future runs, generate content using the LLaMA 3 model via Ollama, and post the generated content to LinkedIn.

## Troubleshooting

- **LinkedIn Login Issues**: If you face issues with logging in, try clearing your cookies and logging in manually again.
- **Ollama Installation**: Ensure that Ollama is correctly installed and accessible from your system’s PATH.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
