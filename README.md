# CooKSmarT
An intelligent web application designed to recommend recipes based purely on the ingredients available. This tool helps users discover new dishes, minimize food waste, and explore their favorite regional cuisines efficiently.
## Setup
1. Create virtualenv:
   - mac/linux:
     python -m venv venv
     source venv/bin/activate
   - windows:
     python -m venv venv
     venv\Scripts\activate

2. Install:
   pip install -r requirements.txt

3. Structure
   <img width="314" height="478" alt="Screenshot 2025-09-30 at 1 44 26 PM" src="https://github.com/user-attachments/assets/2348ca9e-9858-487f-973e-6f326b2627d5" />

4. Features:
* Instantly recommends recipes based on pantry ingredients
* Identifies what’s missing and suggests clever substitutions
* Supports regional cuisines from India, Italian, China
* Responsive interface for seamless browsing

5. Seed DB (creates SQLite DB `cooksmart.db`):
   python db_init.py

6. Run:
   python app.py
Open: http://127.0.0.1:5000

7. Results:
   <img width="1428" height="731" alt="Screenshot 2025-09-30 at 1 40 29 PM" src="https://github.com/user-attachments/assets/c06d7d78-0941-43fd-9608-8106e019b66c" />
   <img width="1428" height="731" alt="Screenshot 2025-09-30 at 1 40 52 PM" src="https://github.com/user-attachments/assets/23e7cd6f-1a2b-4e4b-b224-8194e721d67f" />



