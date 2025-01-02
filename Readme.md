# EasyLogs
A Django-based business management system by Om Pandey.

## Core Features

| Module | Features | Security |
|--------|-----------|-----------|
| **Authentication** | • Multi-level access (Admin/Employee)<br>• Secure login/logout<br>• Custom decorators | • Password hashing<br>• Session management<br>• CSRF protection |
| **Dashboard** | • Real-time analytics<br>• Performance metrics<br>• Activity monitoring | • Role-based access<br>• Data filtering<br>• Audit logging |
| **Finance** | • Cheque lifecycle tracking<br>• Status management<br>• Email reminders | • Transaction logging<br>• Validation checks<br>• Access control |

## Technical Details

| Component | Technologies | Description |
|-----------|--------------|-------------|
| **Backend** | Django 4.x | Core application framework |
| **Database** | PostgreSQL/SQLite | Data persistence |
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **Styling** | Tailwind CSS | Modern UI framework |

## User Roles & Capabilities

| Feature | Admin | Employee |
|---------|--------|-----------|
| Dashboard | Full system overview | Personal metrics |
| Employee Management | ✓ | ✗ |
| Inquiry Management | Full access | Assigned only |
| Cheque Processing | Full access | Assigned only |
| System Backup | ✓ | ✗ |
| Activity Logs | ✓ | ✗ |

## Installation

```bash
git clone https://github.com/ompandey07/EASYLOGS
cd EASYLOGS
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin@admin.com | admin@1200 |

## Tech Stack

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![HTML](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![Tailwind](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## License
MIT License

---
Created by Om Pandey © 2024