import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='Quien es el mejor CTO de platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_question(self):
        time = timezone.now()
        future_question = Question(question_text='Quien es el mejor CTO de platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_past_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text='Quien es el mejor CTO de platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    """Create a question with the given 'question_test, and published the givben number of days offset to now
    (negative for questions published in the past, positive for questions that have yet to be published)
    '"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question("Cuál es tu curso favorito?", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        future_question = create_question("Future Question", days=30)
        past_question = create_question("Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_question(self):
        past_question1 = create_question("Past Question 1", days=-30)
        past_question2 = create_question("Past Question 2", days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [], [])


class ResultViewTest(TestCase):

    def test_past_question(self):
        """
        The result view with a pub date in the past display the
        question's text
        """
        past_question = create_question("past question", days=-15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        Questions with a future date aren't displayed and this return a 404 error(not found)
        until the date is the specified date
        """
        future_question = create_question("this is a future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
