# Generated by Django 5.2 on 2025-05-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todo_created_at_alter_todo_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='작성일'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(verbose_name='내용'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='is_complete',
            field=models.CharField(choices=[('completed', '완료'), ('incomplete', '미완료')], default='incomplete', max_length=10, verbose_name='완료 여부'),
        ),
    ]
