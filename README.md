🧾 Donation Management System (Flask + MongoDB)

A role-based donation management system built using Flask and MongoDB, featuring secure JWT authentication, modular architecture with Blueprints, and clean RBAC (Role-Based Access Control) for managing users and donations.

⚙️ Tech Stack

Backend Framework: Flask (Python)

Database: MongoDB (via PyMongo)

Authentication: JWT (JSON Web Token)

Authorization: Role-Based Access Control (RBAC)

Tools Used: Postman (API Testing), dotenv (env config), Flask Blueprints (modular structure)

📂 Folder Structure
donation_management/
│
├── app.py                         # Main Flask app entry
│
├── controllers/                   # Business logic
│   ├── auth_controller.py
│   ├── donation_controller.py
│   └── user_controller.py
│
├── routes/                        # API endpoints
│   ├── auth_routes.py
│   ├── donation_routes.py
│   └── user_routes.py
│
├── utils/                         # Middleware & helpers
│   ├── auth_middleware.py         # token_required decorator
│
├── middlewares/
│   └── role_required.py           # role_required decorator
│
├── models/
│   └── donation_model.py
│
└── .env, requirements.txt, etc.

👥 User Roles & Permissions
Role	Permissions	Description
Admin	Full CRUD	Can add, edit, delete any donation or user
Donor	Own CRUD	Can add, update, delete only their own donations
Volunteer	Read-only	Can view all donations but can’t edit or delete
🔐 Authentication System

Secure login using JWT Tokens

Tokens stored client-side (for frontend use)

Protected routes use @token_required

Role checking handled via @role_required([...]) decorator

🧱 API Endpoints
🔑 Auth Routes
Endpoint	Method	Description
/register	POST	Register new user with role (Admin, Donor, Volunteer)
/login	POST	Authenticate user and return JWT token
💰 Donation Routes
Endpoint	Method	Access
/add_donation	POST	Admin, Donor
/donations	GET	Admin, Volunteer, Donor
/update_donation/<id>	PUT	Admin, Donor (own)
/delete_donation/<id>	DELETE	Admin, Donor (own)
👥 User Routes
Endpoint	Method	Access
/users	GET	Admin
/users/<id>	PUT	Admin
/users/<id>	DELETE	Admin
✅ Completed Features

Role-based authentication & authorization

Modular architecture using Blueprints

Centralized error handling

Fully tested via Postman

MongoDB integrated with PyMongo

🚧 Next Phase — Frontend (Upcoming)

Frontend will be built using React + Vite, featuring three dashboards:

Dashboard	Description
Admin Dashboard	Manage all users and donations
Donor Dashboard	Add, edit, and delete own donations
Volunteer Dashboard	View all donations only

🧑‍💻 Author

Ibtisam Khan
💼 Backend Developer (Flask, Node.js)
📧 ibtisamk700@gmail.com
