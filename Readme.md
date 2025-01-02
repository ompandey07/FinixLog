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
# For Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser account (optional but recommended)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
