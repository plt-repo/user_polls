# Generated by Django 2.2.10 on 2021-01-13 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True, null=True, verbose_name='Текстовый ответ')),
                ('user_id', models.IntegerField(verbose_name='Идентификатор пользователя')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('start_date', models.DateTimeField(verbose_name='Дата старта')),
                ('end_date', models.DateTimeField(verbose_name='Дата окончания')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Ответ текстом'), (2, 'Ответ с выбором одного варианта'), (3, 'Ответ с выбором нескольких вариантов')], verbose_name='Тип вопроса')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Описание варианта ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='polls.Question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='SelectedQuestionAnswerOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='Идентификатор пользователя')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_question_answer_options', to='polls.Answer', verbose_name='Выбранные пользователем варианты ответа')),
                ('answer_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='polls.QuestionAnswerOption', verbose_name='Вариант ответа')),
            ],
            options={
                'verbose_name': 'Выбранный пользователем вариант ответа',
                'verbose_name_plural': 'Выбранные пользователем варианты ответа',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='polls.Question', verbose_name='Вопрос'),
        ),
    ]
