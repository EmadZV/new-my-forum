# Generated by Django 4.1 on 2022-08-22 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_alter_usermodel_last_seen_and_more'),
        ('mycontent', '0002_alter_postmodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField()),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mycontent.answermodel')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mycontent.postmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myauth.usermodel')),
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='myauth.usermodel')),
            ],
        ),
    ]
