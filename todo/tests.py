from django.test import TestCase, Client
from django.urls import reverse

from .models import Todo

# Create your tests here.

todo_title = "Book Dentist Appointment"

class TestTodoModel(TestCase):

    def setUp(self):
        self.todo = Todo.objects.create(
            title=todo_title
        )

    def test_todo_created(self):
        self.assertEqual(self.todo.title, todo_title)

    def test_date_automatically_assigned(self):
        self.assertTrue(self.todo.created_on)

    def test_status_assigned(self):
        self.assertEqual(self.todo.completed, False)

    def test_str(self):
        self.assertEqual(str(self.todo), todo_title)

class TestListTodoView(TestCase):
    """
    Things to test:
    1. Does a GET request work?
    2. Are there todos in the response context?
    3. Are completed todos excluded?
    4. Are the todos ordered by date created, with most recently created first?
    """

    url = reverse('index')

    def setUp(self):
        self.todo_1 = Todo.objects.create(
            title='My first todo'
        )
        self.todo_2 = Todo.objects.create(
            title='My second todo'
        )
        self.todo_3 = Todo.objects.create(
            title='My third todo'
        )
        self.todo_4 = Todo.objects.create(
            title='My fourth todo'
        )

    def test_get_request_works(self):
        response = Client().get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_todos_included_in_context(self):
        """ Test that the response generated by the view includes a key called 'todos'. """
        response = Client().get(self.url)

        self.assertIn('todos', response.context)

    def test_completed_todos_excluded(self):

        # Mark a todo as complete
        self.todo_4.completed=True
        self.todo_4.save()

        response = Client().get(self.url)

        empty_queryset = Todo.objects.none()
        todos = response.context.get('todos', empty_queryset)

        self.assertEqual(todos.count(), 3)

    def test_todos_ordered_by_date(self):
        """ Test that most recently created todos are listed first."""

        todos = Todo.objects.filter(completed=False).order_by('-created_on')

        response = Client().get(self.url)

        empty_queryset = Todo.objects.none()
        response_todos = response.context.get('todos', empty_queryset)

        self.assertEqual(response_todos.first(), todos.first())
        self.assertEqual(response_todos.last(), todos.last())
