DevCollab — Developer Collaboration Platform



A production-ready REST API built with Django REST Framework, featuring JWT authentication, role-based permissions, and modular app architecture.



Tech Stack

Python | Django | Django REST Framework | PostgreSQL | JWT | Git



Key Features

\- JWT Authentication — register, login, token refresh

\- Role-based access control — Developer and Recruiter roles

\- Job listings with skill-based filtering

\- Application tracking — recruiters manage, developers apply

\- Custom permission classes for data security

\- Search, filter, ordering and pagination on all endpoints



Setup

git clone https://github.com/kavy123-coder/DevCollab.git

cd DevCollab

pip install -r requirements.txt

python manage.py migrate

python manage.py seed\_data

python manage.py runserver



&#x20;API Endpoints

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | /api/register/ | Register new user |

| POST | /api/token/ | Login |

| GET | /api/jobs/ | Browse job listings |

| POST | /api/jobs/ | Post a job (Recruiter) |

| POST | /api/applications/ | Apply for job (Developer) |

| GET | /api/posts/ | Browse posts |

