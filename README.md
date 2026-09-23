## How to setup locally


**1. Clone the repository**

```bash
git clone https://github.com/wdotgonzales/eastvantage-technical-exam.git
```

**2. Go to its directory**
```bash
cd eastvantage-technical-exam
```

**3. Create the Virtual Environment**



```bash
python -m venv venv 
```

or

```bash
python3 -m venv venv 
```




**4. Activate the Virtual Environment**

Use the command for your terminal.

#### macOS / Linux Terminal

```bash
source venv/bin/activate
```

#### Git Bash (Windows)

```bash
source venv/Scripts/activate
```

#### Command Prompt (Windows)

```cmd
venv\Scripts\activate.bat
```

#### PowerShell (Windows)

```powershell
venv\Scripts\Activate.ps1
```

**5. Install Dependencies**

```bash
pip install -r requirements.txt
```

**6. Run server**
```bash
fastapi dev main.py
```

Server started at http://127.0.0.1:8000

Documentation at http://127.0.0.1:8000/docs
