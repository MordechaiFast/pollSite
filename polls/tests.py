from django.test import TestCase

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from .models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_future(self):
        """Tests if was_published_recently() returns False for questions with future date"""
        future_time = timezone.now() + timedelta(seconds=1)
        future_question = Question(pub_date=future_time)
        assert not future_question.was_published_recently()

    def test_was_published_recently_old(self):
        """Tests that was_published_recently() returns False for questions older than one day"""
        day_ago = timezone.now() - timedelta(days=1)
        old_question = Question(pub_date=day_ago)
        assert not old_question.was_published_recently()

    def test_was_published_recently_recent(self):
        """Tests that was_published_recently() returns True for questions within one day"""
        within_a_day = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=within_a_day)
        assert recent_question.was_published_recently()

def create_question(question_text:str, days: int) -> Question:
    """Creates a question published DAYS offset from now"""
    return Question.objects.create(question_text=question_text,
     pub_date= timezone.now() + timedelta(days=days))

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """Tests that if no questions exist, an appropriate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        assert response.status_code == 200
        assert "No polls are available." in str(response.content)
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        """Tests that a quesiton from the recent past is displayed"""
        question = create_question("Past question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [question])

    def test_future_question(self):
        """Tests that a quesiton from the future is not displayed"""
        create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        assert "No polls are available." in str(response.content)
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_and_future_question(self):
        """Tests that if both a past and a future question are entered, only the past question is displayed"""
        question = create_question("Past question", -30)
        create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [question])

    def test_two_questions(self):
        """Tests that when two questions are entered, they both are displayed"""
        question1 = create_question("Past question 1", -30)
        question2 = create_question("Past question 2", -20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],
         [question2, question1])
