----RecruitHub – Smart Job Portal with ATS Resume Scoring-----
🚀 RecruitHub is a full‑stack recruitment platform built using Django that connects candidates with companies and simplifies the hiring process.
The system allows companies to post jobs, candidates to apply with resumes, and automatically evaluates resumes using an ATS (Applicant Tracking System) score.

🌟 Features:
👤 Candidate Features-
Register and login as a candidate
Browse available job opportunities
Upload resume while applying
View application status
Check ATS Resume Score
Track interview schedules

🏢 Company Features-
Register and login as company
Create and manage job postings
View all candidate applications
View candidate resumes
ATS score evaluation for candidates
Accept / Reject applications
Schedule interviews

📊 Dashboard Features-
Company dashboard analytics
Total jobs posted
Total applications received
Job management system

🧠 ATS Resume Scoring System:
The system analyzes candidate resumes and calculates an ATS compatibility score based on job description keywords.

Example:
Resume Match Score
High Match → 80%+
Medium Match → 50% - 79%
Low Match → Below 50%
This helps recruiters quickly identify the most suitable candidates.
Accepted / Rejected / Pending counts

🛠️ Tech Stack:
Frontend-
HTML
CSS
Bootstrap

Backend-
Python
Django Framework

Database-
SQLite

Libraries-
pdfminer.six (for resume parsing)

Tools-
Git
GitHub
VS Code

📂 Project Structure:
recruithub-job-portal
│
├── accounts
│   ├── views.py
│   ├── models.py
│
├── jobs
│   ├── models.py
│   ├── views.py
│
├── templates
│   ├── accounts
│   ├── jobs
│
├── recruithub
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── requirements.txt
└── build.sh

⚙️ Installation Guide:
1️⃣ Clone the repository
git clone https://github.com/SanyuktaSasane/recruithub-job-portal.git
2️⃣ Go to project directory
cd recruithub-job-portal
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run migrations
python manage.py migrate
5️⃣ Start server
python manage.py runserver
Then open:
http://127.0.0.1:8000

🚀 Future Improvements:
AI‑based resume ranking
Email interview notifications
Resume keyword suggestions
Advanced analytics dashboard
Job recommendation system

👩‍💻 Author:
Sanyukta Sasane

GitHub:
https://github.com/SanyuktaSasane

⭐ If you like this project
Give the repository a star ⭐ on GitHub.
