# Cognition: Your Local AI Second Brain

**Cognition** is a privacy-first, local tool that turns your scattered documents (PDFs, Notes, Text files) into a searchable Knowledge Graph. It uses AI to understand the *meaning* behind your files, not just keyword matching, allowing you to discover hidden connections in your data.

**Key Features:**
* **100% Local Processing:** No data leaves your machine. No API keys required.
* **Semantic Search:** Search by concept (e.g., "cooking tips") to find files that don't even contain those exact words.
* **Knowledge Graph:** Visualize how your documents relate to one another.
* **Accessible UI:** Simple web interface designed for everyone.

---

## 🚀 Quick Start

### Prerequisites
* **Python 3.9+** installed.
* **VS Code** (recommended).
* **8GB RAM** minimum recommended.

### Installation

1.  **Clone the repository** (or download and unzip):
    ```bash
    git clone [https://github.com/YOUR_USERNAME/cognition.git](https://github.com/YOUR_USERNAME/cognition.git)
    cd cognition
    ```

2.  **Run the setup command** (creates a virtual environment and installs dependencies):
    * **Windows (PowerShell):**
        ```powershell
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        pip install -r requirements.txt
        ```
    * **Linux/Mac:**
        ```bash
        make setup
        source venv/bin/activate
        ```

3.  **Run the App:**
    ```bash
    streamlit run app/main.py
    ```

4.  **Open your browser:** The app will typically launch at `http://localhost:8501`.

---

## 📖 Guided Workflow (Try this first!)

1.  **Upload:** Go to the sidebar. Under "Add Data", click "Browse files". Select the `data/sample/sample_notes.csv` file included in this repo.
2.  **Process:** Click the **"Ingest & Process"** button.
    * *What happens:* The AI reads the text, creates mathematical "embeddings" (vectors) representing the meaning, and stores them locally.
3.  **Search:** Go to the "Semantic Search" tab. Type `environment` or `cooking`.
    * *Result:* You will see results related to nature or food, even if the exact word isn't there.
4.  **Visualize:** Switch to the "Knowledge Graph" tab to see bubbles representing your documents connected by similarity.

---

## 🛠️ Deployment (Free Hosting)

Since this app uses local file storage, the easiest way to share a *demo* version is via **Streamlit Community Cloud**.

1.  **Push to GitHub:**
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    # Create a repo on GitHub.com, then:
    git remote add origin [https://github.com/YOUR_USERNAME/cognition.git](https://github.com/YOUR_USERNAME/cognition.git)
    git push -u origin main
    ```

2.  **Deploy:**
    * Go to [share.streamlit.io](https://share.streamlit.io/).
    * Sign up/Login with GitHub.
    * Click "New App".
    * Select your `cognition` repository.
    * Set Main file path to `app/main.py`.
    * Click **Deploy**.

*Note: For a persistent personal version, running locally on your laptop is recommended to keep your data private.*

---

## 🧪 Running Tests

To ensure everything is working correctly:

```bash
# Activate your venv first
pytest tests/