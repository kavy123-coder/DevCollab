"""
seed_data.py — DevCollab demo data seeder
==========================================
Yahan ye file apne project mein copy karo:
  apps/users/management/commands/seed_data.py

Pehle folder structure banana padega:
  apps/users/management/__init__.py
  apps/users/management/commands/__init__.py
  apps/users/management/commands/seed_data.py

Run karo:
  python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import Skill, Userprofile
from apps.posts.models import Tag, Post, Comment
from apps.jobs.models import Jobs, Application
from faker import Faker
import random

fake = Faker()

# ── Config ──────────────────────────────────────────────
NUM_USERS       = 10
NUM_SKILLS      = 12
NUM_TAGS        = 8
NUM_POSTS       = 20
NUM_JOBS        = 8
NUM_APPLICATIONS = 15
# ────────────────────────────────────────────────────────

SKILL_NAMES = [
    "Python", "Django", "React", "JavaScript", "TypeScript",
    "PostgreSQL", "Docker", "AWS", "GraphQL", "FastAPI",
    "Vue.js", "Redis",
]

TAG_NAMES = [
    "backend", "frontend", "devops", "open-source",
    "tutorial", "career", "database", "api",
]

ROLES = ["Developer", "Developer", "Developer", "Recruiter"]  # weighted

CITIES = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai"]

STATUS_CHOICES = ["Pending", "Accepted", "Rejected"]


class Command(BaseCommand):
    help = "Seed demo data for all apps"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding demo data...\n")

        skills  = self._create_skills()
        tags    = self._create_tags()
        users   = self._create_users(skills)
        posts   = self._create_posts(users, tags)
        self._create_comments(posts, users)
        self._create_likes(posts, users)
        jobs    = self._create_jobs(users, skills)
        self._create_applications(jobs, users)

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Done!\n"
            f"   Users: {NUM_USERS}  Skills: {NUM_SKILLS}  Tags: {NUM_TAGS}\n"
            f"   Posts: {NUM_POSTS}  Jobs: {NUM_JOBS}  Applications: {NUM_APPLICATIONS}\n"
            f"\n   Login with any user: password is 'password123'\n"
            f"   Superuser (already exists) ka password same rahega.\n"
        ))

    # ── Skills ──────────────────────────────────────────
    def _create_skills(self):
        skills = []
        for name in SKILL_NAMES:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills.append(skill)
        self.stdout.write(f"  ✓ {len(skills)} skills created")
        return skills

    # ── Tags ────────────────────────────────────────────
    def _create_tags(self):
        tags = []
        for name in TAG_NAMES:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        self.stdout.write(f"  ✓ {len(tags)} tags created")
        return tags

    # ── Users + Profiles ────────────────────────────────
    def _create_users(self, skills):
        users = []

        # Superuser ko bhi profile de do agar nahi hai
        for su in User.objects.filter(is_superuser=True):
            profile, created = Userprofile.objects.get_or_create(
                user=su,
                defaults={
                    "role": "Admin",
                    "bio": "Platform administrator.",
                    "github_url": "https://github.com/admin",
                    "linkedin_url": "",
                }
            )
            if created:
                profile.skills.set(random.sample(skills, 3))
            users.append(su)

        for i in range(NUM_USERS):
            username = fake.user_name() + str(random.randint(10, 99))
            email    = fake.email()

            # Duplicate username se bachne ke liye
            while User.objects.filter(username=username).exists():
                username += str(random.randint(0, 9))

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            role = random.choice(ROLES)
            Userprofile.objects.create(
                user=user,
                role=role,
                bio=fake.paragraph(nb_sentences=2),
                github_url=f"https://github.com/{username}",
                linkedin_url=f"https://linkedin.com/in/{username}",
            )
            # 2–5 random skills
            profile = user.userprofile
            profile.skills.set(random.sample(skills, random.randint(2, 5)))

            users.append(user)

        self.stdout.write(f"  ✓ {NUM_USERS} users created (password: password123)")
        return users

    # ── Posts ────────────────────────────────────────────
    def _create_posts(self, users, tags):
        posts = []
        for _ in range(NUM_POSTS):
            author = random.choice(users)
            post = Post.objects.create(
                author=author,
                title=fake.sentence(nb_words=6).rstrip("."),
                content="\n\n".join(fake.paragraphs(nb=3)),
            )
            # 1–3 random tags
            post.tags.set(random.sample(tags, random.randint(1, 3)))
            posts.append(post)

        self.stdout.write(f"  ✓ {NUM_POSTS} posts created")
        return posts

    # ── Comments ─────────────────────────────────────────
    def _create_comments(self, posts, users):
        count = 0
        for post in posts:
            # Har post pe 0–4 comments
            for _ in range(random.randint(0, 4)):
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=fake.sentence(nb_words=random.randint(8, 20)),
                )
                count += 1
        self.stdout.write(f"  ✓ {count} comments created")

    # ── Likes ─────────────────────────────────────────────
    def _create_likes(self, posts, users):
        for post in posts:
            likers = random.sample(users, random.randint(0, min(5, len(users))))
            post.likes.set(likers)
        self.stdout.write(f"  ✓ Likes added to posts")

    # ── Jobs ──────────────────────────────────────────────
    def _create_jobs(self, users, skills):
        jobs = []
        # Sirf recruiters jobs post karein
        recruiters = [
            u for u in users
            if hasattr(u, "userprofile") and u.userprofile.role == "Recruiter"
        ]
        # Agar koi recruiter nahi toh kuch bhi use karo
        if not recruiters:
            recruiters = users

        for _ in range(NUM_JOBS):
            job = Jobs.objects.create(
                recruiter=random.choice(recruiters),
                title=random.choice([
                    "Backend Developer", "Frontend Engineer", "Full Stack Developer",
                    "DevOps Engineer", "Django Developer", "React Developer",
                    "Data Engineer", "API Developer",
                ]),
                description=fake.paragraph(nb_sentences=4),
                location=random.choice(CITIES),
                is_remote=random.choice([True, False]),
            )
            job.skill_required.set(random.sample(skills, random.randint(2, 4)))
            jobs.append(job)

        self.stdout.write(f"  ✓ {NUM_JOBS} jobs created")
        return jobs

    # ── Applications ──────────────────────────────────────
    def _create_applications(self, jobs, users):
        # Developers apply karein
        developers = [
            u for u in users
            if hasattr(u, "userprofile") and u.userprofile.role == "Developer"
        ]
        if not developers:
            developers = users

        count = 0
        seen = set()  # same user same job pe dobara apply na kare

        attempts = 0
        while count < NUM_APPLICATIONS and attempts < NUM_APPLICATIONS * 5:
            attempts += 1
            applicant = random.choice(developers)
            job       = random.choice(jobs)
            key       = (applicant.id, job.id)
            if key in seen:
                continue
            seen.add(key)

            Application.objects.create(
                job=job,
                applicant=applicant,
                cover_letter=fake.paragraph(nb_sentences=2),
                resume="resumes/demo_resume.pdf",   # placeholder path
                status=random.choice(STATUS_CHOICES),
            )
            count += 1

        self.stdout.write(f"  ✓ {count} applications created")
