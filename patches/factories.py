import random

SAMPLE_SIZE = 5
BASE_URL = "http://pinaxproject.com/pinax-design/patches/"

apps = [
    "django-mailer",
    "django-user-accounts",
    "pinax-announcements",
    "pinax-badges",
    "pinax-blog",
    "pinax-calendars",
    "pinax-cohorts",
    "pinax-comments",
    "pinax-documents",
    "pinax-eventlog",
    "pinax-events",
    "pinax-forums",
    "pinax-images",
    "pinax-invitations",
    "pinax-likes",
    "pinax-lms-activities",
    "pinax-messages",
    "pinax-news",
    "pinax-notifications",
    "pinax-phone-confirmation",
    "pinax-points",
    "pinax-ratings",
    "pinax-referrals",
    "pinax-stripe",
    "pinax-submissions",
    "pinax-teams",
    "pinax-templates",
    "pinax-testimonials",
    "pinax-types",
    "pinax-waitinglist",
    "pinax-webanalytics"
]


def create_item(app):
    patch = "{}{}.svg".format(BASE_URL, app)
    distractors = random.sample(list(filter(lambda x: x != app, apps)), SAMPLE_SIZE)
    choices = distractors + [app]
    random.shuffle(choices)
    return dict(
        question=patch,
        answer=app,
        distractors=distractors,
        choices=choices
    )


def generate_items(user):
    dataset = {}
    for app in apps:
        dataset[app] = create_item(app)
    return dataset
