import re

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def update_thread_title_on_first_message(sender, instance, created, **kwargs):
    """
    Update thread title with a summary of the first message content.
    """
    if not created:
        return

    # Check if this is the first message in the thread
    if instance.thread.message_count == 1:
        title = generate_message_summary(instance.content)
        instance.thread.title = title
        instance.thread.save(update_fields=["title", "updated_at"])


def generate_message_summary(content, max_length=30):
    """
    Generate a concise summary from message content.
    """
    if not content or not content.strip():
        return "New Chat"

    # Clean the content
    content = content.strip()

    # Try to get the first sentence
    sentences = re.split(r"[.!?]+", content)
    first_sentence = sentences[0].strip() if sentences else content

    # If first sentence is too long, truncate at word boundary
    if len(first_sentence) > max_length:
        words = first_sentence.split()
        truncated = ""
        for word in words:
            if len(truncated + word + " ") <= max_length - 3:  # Leave space for "..."
                truncated += word + " "
            else:
                break
        first_sentence = (
            truncated.strip() + "..."
            if truncated.strip()
            else content[: max_length - 3] + "..."
        )

    return first_sentence or "New Chat"
