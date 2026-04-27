# Web Crawler Project (CS172 — Part A)

## Overview

```
TBD
```

## Installation

### Prerequisites

- Python 3.10 or newer (`python --version` to check)
- `pip` (bundled with Python)

### 1. Clone the repo

```bash
git clone <repo-url>
cd CS172_Project
```

### 2. Create a virtual environment

Run this once in the project root:

```bash
python -m venv .venv
```

This creates a `.venv/` folder (already in `.gitignore`, so it won't be committed).

### 3. Activate the virtual environment

You must activate it **every time you open a new terminal**.

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows — CMD:**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

You should now see `(.venv)` at the start of your prompt. To verify:

```bash
python -c "import sys; print(sys.executable)"
```

The path should contain `.venv`.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

When new packages are added to `requirements.txt` later, just rerun the same command.

### 5. Deactivate (when done)

```bash
deactivate
```
## Usage
