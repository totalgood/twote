import django_filters
from twote.models import OutgoingTweet, Tweet

APPROVAL_CHOICES = (
    (0, 'needs_action'),
    (1, 'Approved'),
    (2, 'Denied'),
)

class OutgoingTweetFilter(django_filters.FilterSet):
    approved = django_filters.ChoiceFilter(choices=APPROVAL_CHOICES)

    class Meta:
        model = OutgoingTweet
        fields = ['approved',]


class StrictTweetFilter(django_filters.FilterSet):
    class Meta:
        model = Tweet
        fields = ['is_strict', 'tags']