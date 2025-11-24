from django.db import migrations


def create_skills(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    skills = [
        ('Python', 'Fundamental', 90, 'ri-python-line'),
        ('JavaScript', 'Basic', 65, 'ri-javascript-line'),
        ('C++', 'Basic', 60, 'ri-code-line'),
        ('HTML', 'Fundamental', 95, 'ri-html5-line'),
        ('CSS', 'Fundamental', 90, 'ri-css3-line'),
        ('React', 'Basic', 60, 'ri-reactjs-line'),
        ('Django', 'Fundamental', 88, 'ri-database-2-line'),
        ('REST API', 'Fundamental', 85, 'ri-exchange-line'),
        ('Linux', 'Fundamental', 80, 'ri-terminal-box-line'),
        ('Git', 'Fundamental', 85, 'ri-git-branch-line'),
        ('Linear Algebra', 'Fundamental', 75, 'ri-function-line'),
        ('Discrete Math', 'Fundamental', 70, 'ri-shapes-line'),
        ('Calculus', 'Fundamental', 72, 'ri-superscript-2'),
        ('PostgreSQL', 'Fundamental', 78, 'ri-database-line'),
        ('Problem Solving', 'Fundamental', 92, 'ri-lightbulb-flash-line'),
    ]
    for name, level, proficiency, icon in skills:
        Skill.objects.get_or_create(name=name, defaults={'level': level, 'proficiency': proficiency, 'icon': icon})


def remove_skills(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Skill.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_skills, remove_skills),
    ]


