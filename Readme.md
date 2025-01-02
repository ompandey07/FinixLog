
# **EasyLogs**  
A Django-based business management system for streamlined inquiry and cheque management.  

Created by **Om Pandey**

---

## **Core Features**

### **Authentication Module**
- Multi-level access for Admin and Employee
- Secure login/logout functionality
- Custom decorators for access control

**Security Features:**  
- Password hashing for secure storage  
- Session management with timeout and token-based validation  
- CSRF protection for form submissions  

### **Dashboard Module**
- Real-time analytics and performance metrics  
- Activity and system monitoring  
- Interactive charts and graphs for performance tracking  

**Security Features:**  
- Role-based access control for personalized dashboard views  
- Data filtering and sorting to prevent unauthorized access to sensitive information  
- Comprehensive audit logging for system activities  

### **Finance Module**
- Full cheque lifecycle tracking from initiation to completion  
- Status management with reminders for pending cheques  
- Email notifications for users on cheque status updates  

**Security Features:**  
- Transaction logging for every financial action  
- Validation checks for transaction integrity  
- Restricted access control for sensitive financial data  

---

## **Technical Stack**

### **Backend**  
- **Framework:** Django 4.x  
- **Authentication:** JWT and Session-based  
- **API Support:** RESTful APIs using Django Rest Framework (DRF)

### **Database**  
- **Primary Database:** PostgreSQL (Highly recommended for production)  
- **Fallback Option:** SQLite (For development/testing)

### **Frontend**  
- **Languages:** HTML5, CSS3, JavaScript  
- **Framework:** Tailwind CSS (for fast UI development)

### **Version Control**  
- **Git:** For version tracking and collaboration

### **Deployment**  
- **Containerization:** Docker for development and production environments  
- **Cloud Integration:** AWS / Heroku (for cloud deployment)

### **Other Technologies**  
- **Task Queue:** Celery for background task management  
- **Testing Framework:** PyTest for unit and integration testing  
- **CI/CD:** GitHub Actions for continuous integration and deployment

---

## **Installation Guide**

To set up EasyLogs on your local machine:

### Prerequisites
- Python 3.8 or above
- PostgreSQL (Optional: use SQLite for testing)

### Steps:
```bash
# Clone the repository
git clone https://github.com/ompandey07/EASYLOGS
cd EASYLOGS

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # Linux/macOS
# For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser account (optional but recommended)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

After running the above commands, you can access the application at `http://127.0.0.1:8000/`.

---

## **Default Credentials**

| Role   | Username         | Password    |
|--------|------------------|-------------|
| Admin  | admin@admin.com  | admin@1200  |

---

## **User Roles & Capabilities**

<<<<<<< HEAD
| Feature                 | Admin               | Employee         |
|-------------------------|---------------------|------------------|
| **Dashboard**            | Full system overview| Personal metrics |
| **Employee Management**  | Full control        | View only        |
| **Inquiry Management**   | Full access         | Assigned access  |
| **Cheque Processing**    | Full access         | Assigned access  |
| **System Backup**        | Full access         | ✗                |
| **Activity Logs**        | Full access         | ✗                |
=======
<table width="90%">
  <thead>
    <tr>
      <th>Feature</th>
      <th>Admin</th>
      <th>Employee</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Dashboard</strong></td>
      <td>Full system overview</td>
      <td>Personal metrics</td>
    </tr>
    <tr>
      <td><strong>Employee Management</strong></td>
      <td>Full control</td>
      <td>View only</td>
    </tr>
    <tr>
      <td><strong>Inquiry Management</strong></td>
      <td>Full access</td>
      <td>Assigned access</td>
    </tr>
    <tr>
      <td><strong>Cheque Processing</strong></td>
      <td>Full access</td>
      <td>Assigned access</td>
    </tr>
    <tr>
      <td><strong>System Backup</strong></td>
      <td>Full access</td>
      <td>✗</td>
    </tr>
    <tr>
      <td><strong>Activity Logs</strong></td>
      <td>Full access</td>
      <td>✗</td>
    </tr>
  </tbody>
</table>
>>>>>>> 965fe6552d385dae5f5314a51abd7318a4670439

---

## **Security**

### **Authentication**  
- Password hashing using Django's PBKDF2 by default, ensuring passwords are never stored in plaintext.  
- Session-based authentication and custom JWT tokens are available for API access.

### **Role-Based Access Control**  
- Separate access control levels for Admin and Employee roles with detailed permissions.

### **Data Integrity**  
- Validation and sanitization for all user input to prevent SQL injection, XSS, and CSRF attacks.

---

## **Tech Badges**

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)  
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)  
![HTML](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)  
![CSS](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)  
![Tailwind](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)  
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)  

---

## **Contributing**

We welcome contributions to EasyLogs! To get started, please follow these steps:

1. Fork the repository by clicking the "Fork" button on the GitHub page.
2. Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/your-username/EASYLOGS
   ```
3. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and commit them:
   ```bash
   git commit -m 'Add your feature description'
   ```
5. Push the changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a pull request from your fork to the main repository.  

---

## **License**

MIT License - see the [LICENSE](LICENSE) file for details.

---

**Created by Om Pandey © 2024**
