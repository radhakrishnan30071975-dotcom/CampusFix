# Generated for CampusFix Member 3 feedback feature

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[
                    (1, '1 - Very Poor'),
                    (2, '2 - Poor'),
                    (3, '3 - Average'),
                    (4, '4 - Good'),
                    (5, '5 - Excellent'),
                ])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='feedback',
                    to='complaints.complaint'
                )),
            ],
        ),
    ]
