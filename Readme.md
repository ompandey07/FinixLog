# EasyLogs
A comprehensive business management system built with Django that streamlines employee, inquiry, and financial tracking.

![Banner](https://img.shields.io/badge/EasyLogs-Business%20Management-blue)

## Key Features

### Authentication & Access Control
- Multi-level user authentication (Admin/Employee)
- Custom access decorators for route protection
- Secure login/logout functionality
- Default admin account creation

### Dashboard Analytics
- **Admin Dashboard**
  - Real-time counts: Inquiries, Pending Cheques, Employees, Contacts
  - Activity monitoring across all departments
  
- **Employee Dashboard**
  - Personal performance metrics
  - Assigned inquiries and cheques tracking
  - Contact management

### Financial Management
📊 **Cheque Tracking System**
- Complete cheque lifecycle management
- Status tracking: New → Deposited → Pending → Completed
- Email reminder system
- Detailed reporting with filtering options

### Customer Relations
📞 **Inquiry Management**
- Automated inquiry numbering
- Detailed customer information tracking
- Assignment and status monitoring
- Comprehensive search and filter capabilities

### Employee Management
👥 **Complete Employee Portal**
- Profile management with image upload
- Role-based access control
- Performance tracking
- Contact information management

### Data Security
🔒 **Backup & Restore**
- Automated database backups
- Point-in-time restoration
- Secure file handling
- Activity logging for all operations

## Technical Architecture

### Backend Framework
- Django 4.x
- Custom User Model
- Decorators for access control
- SQLite/PostgreSQL database

### Security Features
- Password hashing
- Session management
- CSRF protection
- File upload security

### Models
```python
Key Models:
- CustomUser: Extended Django user
- Employee: Profile and permissions
- Inquiry: Customer communication
- Cheque: Financial tracking
- ActivityLog: System monitoring
```

## Tech Stack
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![HTML](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![Tailwind](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

## Installation & Setup

1. **Clone & Environment Setup**
```bash
git clone https://github.com/ompandey07/EASYLOGS
cd EASYLOGS
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. **Dependencies & Configuration**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. **Default Admin Credentials**
```
Username: admin@admin.com
Password: admin@1200
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
MIT License - See LICENSE file for details

---

Created with ❤️ by Om Pandey | Copyright © 2024