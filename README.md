🍱 FoodShare+

A Smart Food Donation & Distribution Platform

📌 Overview

FoodShare+ is a web-based platform designed to reduce food waste and improve food distribution by connecting donors, volunteers, and administrators in a structured and efficient system.

The platform ensures that excess food is not wasted but instead delivered to communities in need through a coordinated workflow.
🎯 Problem Statement

A significant amount of food is wasted daily, while many people still face food shortages. The lack of coordination between food donors and distribution channels leads to inefficiency and loss of valuable resources.

FoodShare+ solves this problem by providing a centralized system for food donation and distribution.

💡 Key Features
👤 User Management

    Secure registration & login system

    Role-based access control (Donor, Volunteer, Admin)

    Profile management

🍲 Donation Management (Donor)

    Create food donation posts

    Add details (type, quantity, location, expiry)

    Track donation status (Pending → Assigned → Collected → Distributed)

🚚 Volunteer System

    View available donation tasks

    Accept assigned tasks

    Update delivery status in real-time

    Track activity history

🛠️ Admin Panel

    Manage users (Donor & Volunteer)

    Assign donations to volunteers

    Monitor system activity

    Control user access (activate/deactivate accounts)

📊 Dashboard System

    Separate dashboards for each role

    Real-time statistics and status tracking

    Clean and user-friendly interface

🔐 Security

    Session-based authentication

    Role-based authorization

    Protection against unauthorized access

🔄 System Workflow

 -Donor creates a donation

 -Admin assigns a volunteer

 -Volunteer collects and delivers food

 -System updates status at each step

This ensures transparency and proper tracking of every donation.
🧱 Technology Stack

Backend	- Flask (Python)
Database - SQLite + SQLAlchemy
Frontend	- HTML, CSS, Bootstrap
Templating	- Jinja2

🗄️ Database Structure

Main entities:

  1. Users → stores roles and authentication data

  2. Donations → stores food details and status

  3. Assignments → links volunteers to donations

     🚀 Setup Instructions
1. Clone the repository
   git clone https://github.com/your-username/foodshare-plus.git
   cd foodshare-plus
     
2. Create virtual environment
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)

3. Install dependencies
pip install flask sqlalchemy

4. Run the application
   python app.py

5. Open in browser
http://127.0.0.1:5000/ or http://127.0.0.1:5000/Home

📸 Screenshots

<img width="1920" height="1080" alt="about" src="https://github.com/user-attachments/assets/65a69e91-ed8f-4237-9756-45164477e86e" />
<img width="1920" height="1080" alt="faq" src="https://github.com/user-attachments/assets/744fd379-1e5c-4636-81ed-67edf3e28db4" />
<img width="1920" height="1080" alt="Monitor Donations" src="https://github.com/user-attachments/assets/82462d29-1b9b-4002-9587-108a8cf8e593" />
<img width="1920" height="1080" alt="restriction system" src="https://github.com/user-attachments/assets/234aae41-d3d0-4f36-b2be-f5653a5eadde" />
<img width="1920" height="1080" alt="view replies" src="https://github.com/user-attachments/assets/8f2cc4df-846a-437b-a660-a0e68a53ffac" />
<img width="1920" height="1080" alt="message management" src="https://github.com/user-attachments/assets/0619a69c-13e6-47a6-973d-7b057df81cae" />
<img width="1920" height="1080" alt="Assign volunteer" src="https://github.com/user-attachments/assets/0c364a56-c60a-4617-813a-1ee480a0af2d" />
<img width="1920" height="1080" alt="Admin dashbaord" src="https://github.com/user-attachments/assets/92494658-7823-4ce4-a62f-1da1db748d2e" />
<img width="1920" height="1080" alt="status updated" src="https://github.com/user-attachments/assets/2890bada-d7d9-4e41-93af-25cd810300a9" />
<img width="1920" height="1080" alt="Volunteer Dashboard" src="https://github.com/user-attachments/assets/280d1f96-943a-4447-8206-5a25d29f6643" />
<img width="1920" height="1080" alt="Contact" src="https://github.com/user-attachments/assets/c0b551d4-87a4-40b2-8db2-4f126ce2b3d5" />
<img width="1920" height="1080" alt="Donation History" src="https://github.com/user-attachments/assets/ff382f50-a757-4fb1-b163-2b2a5ef7b8ae" />
<img width="1920" height="1080" alt="edit,delete donation" src="https://github.com/user-attachments/assets/a8c8fea5-04d9-481d-ba8b-38b1c6367b9f" />
<img width="1920" height="1080" alt="donor dashboard (2)" src="https://github.com/user-attachments/assets/e43ef489-23ed-4bf8-8fbf-b8025a94d195" />
<img width="1920" height="1080" alt="Create Donation" src="https://github.com/user-attachments/assets/6b04417d-7861-4fd6-bd06-fb5e7ddca217" />
<img width="1920" height="1080" alt="LOGIN" src="https://github.com/user-attachments/assets/6c907643-91cc-444e-97f5-88c79acc3985" />
<img width="1920" height="1080" alt="Register" src="https://github.com/user-attachments/assets/25f1a292-45f8-4b11-8a79-9bba8ab5d736" />
<img width="1920" height="1080" alt="Home" src="https://github.com/user-attachments/assets/b4646d5d-2db2-43f3-be38-306296e1857f" />


📄 License

This project is for academic purposes.
