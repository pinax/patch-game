import random

SAMPLE_SIZE = 5
BASE_URL = "http://pinaxproject.com/pinax-design/patches/"

apps = [
    {"app": "django-mailer", "topics": ["Communications"]},
    {"app": "django-user-accounts", "topics": ["Accounts"]},
    {"app": "pinax-announcements", "topics": ["Communications"]},
    {"app": "pinax-badges", "topics": ["Gamification"]},
    {"app": "pinax-blog", "topics": ["CMS"]},
    {"app": "pinax-calendars", "topics": ["Utilities"]},
    {"app": "pinax-cohorts", "topics": ["SaaS"]},
    {"app": "pinax-comments", "topics": ["Communications"]},
    {"app": "pinax-documents", "topics": ["Document Management"]},
    {"app": "pinax-eventlog", "topics": ["Infrastructure"]},
    {"app": "pinax-events", "topics": ["CMS"]},
    {"app": "pinax-forums", "topics": ["Communications"]},
    {"app": "pinax-images", "topics": ["Utilities"]},
    {"app": "pinax-invitations", "topics": ["SaaS"]},
    {"app": "pinax-likes", "topics": ["Engagement"]},
    {"app": "pinax-lms-activities", "topics": ["Learning"]},
    {"app": "pinax-messages", "topics": ["Communications"]},
    {"app": "pinax-news", "topics": ["CMS"]},
    {"app": "pinax-notifications", "topics": ["Communications"]},
    {"app": "pinax-phone-confirmation", "topics": ["Accounts"]},
    {"app": "pinax-points", "topics": ["Gamification"]},
    {"app": "pinax-ratings", "topics": ["Engagement"]},
    {"app": "pinax-referrals", "topics": ["Engagement"]},
    {"app": "pinax-stripe", "topics": ["SaaS"]},
    {"app": "pinax-submissions", "topics": ["Document Management"]},
    {"app": "pinax-teams", "topics": ["Accounts"]},
    {"app": "pinax-templates", "topics": ["Themes"]},
    {"app": "pinax-testimonials", "topics": ["CMS"]},
    {"app": "pinax-types", "topics": ["Utilities"]},
    {"app": "pinax-waitinglist", "topics": ["SaaS"]},
    {"app": "pinax-webanalytics", "topics": ["Infrastructure"]},
]


def create_item(app, topics):
    patch = "{}{}.svg".format(BASE_URL, app)
    distractors = [d["app"] for d in random.sample(list(filter(lambda x: x["app"] != app, apps)), SAMPLE_SIZE)]
    choices = distractors + [app]
    random.shuffle(choices)
    return dict(
        question=patch,
        answer=app,
        distractors=distractors,
        choices=choices,
        topics=topics + [app]
    )


def generate_items(user_state):
    dataset = {}
    filtered_apps = [app for app in apps if app["app"] != user_state.get("last_asked")]
    filtered_apps = [app for app in filtered_apps if app["app"] not in user_state.get("last_correct", {})]
    for app in filtered_apps:
        dataset[app["app"]] = create_item(app["app"], app["topics"])
    return dataset
