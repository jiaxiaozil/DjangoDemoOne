import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question,Choice
from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        30天后的时间实例
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        """
        1天1秒前的时间实例
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        """
        23小时59分59秒前的时间实例
        """
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)

def create_question(question_text,days):
    """
    用给的text和days，创建text和now+days的question测试数据
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return  Question.objects.create(question_text=question_text, pub_date=time)

# def creat_choices(question_text,days,choice_text,votes):
#     return Choice.objects.create(question=(create_question(question_text,days)).pk,choice_text=choice_text, votes=votes)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        question =create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        '''比较俩个查询集合时查询集对象是不同查询的结果，即使它们的结果（比较ds1.query和ds2.query）具有相同的值，
        它们也不会相同。如果先将查询集转换为列表，则应该可以进行正常比较（当然，假设它们具有相同的排序顺序）：
        self.assertEqual(list(ds1), list(ds2))，否则报错，或者在最后加上ordered=False'''
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
           [question1,question2],ordered=False
        )



class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question',days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question',days=-5)
        url = reverse('polls:results',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)




# Create your tests here.










