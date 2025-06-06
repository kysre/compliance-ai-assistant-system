from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import ChatUser, Message, MessageRole, Thread

User = get_user_model()


class ThreadTitleAutoUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.chat_user = ChatUser.objects.create(user=self.user)
        self.thread = Thread.objects.create(chat_user=self.chat_user)

    def test_thread_title_updates_on_first_message(self):
        """Test that thread title is updated when the first message is added."""
        # Initially, thread should have default title
        self.assertEqual(self.thread.title, "New Chat")

        # Add first message
        message_content = (
            "Hello, I need help with compliance regulations for my business."
        )
        Message.objects.create(
            thread=self.thread, role=MessageRole.USER, content=message_content
        )

        # Refresh thread from database
        self.thread.refresh_from_db()

        # Title should now be updated to a summary of the first message
        self.assertNotEqual(self.thread.title, "New Chat")
        self.assertTrue(len(self.thread.title) <= 50)  # Should be truncated
        self.assertIn("Hello", self.thread.title)

    def test_thread_title_not_updated_on_subsequent_messages(self):
        """Test that thread title is not updated after the first message."""
        # Add first message
        Message.objects.create(
            thread=self.thread, role=MessageRole.USER, content="First message content"
        )

        # Refresh and get the title after first message
        self.thread.refresh_from_db()
        first_message_title = self.thread.title

        # Add second message
        Message.objects.create(
            thread=self.thread,
            role=MessageRole.ASSISTANT,
            content="This is a response message",
        )

        # Refresh thread from database
        self.thread.refresh_from_db()

        # Title should remain the same
        self.assertEqual(self.thread.title, first_message_title)

    def test_empty_message_content_fallback(self):
        """Test that empty message content falls back to default title."""
        Message.objects.create(thread=self.thread, role=MessageRole.USER, content="")

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, "New Chat")

    def test_long_message_truncation(self):
        """Test that long messages are properly truncated."""
        long_content = "This is a very long message that should be truncated because it exceeds the maximum length limit for thread titles and should be cut off appropriately."

        Message.objects.create(
            thread=self.thread, role=MessageRole.USER, content=long_content
        )

        self.thread.refresh_from_db()
        self.assertTrue(len(self.thread.title) <= 50)
        self.assertTrue(self.thread.title.endswith("..."))
