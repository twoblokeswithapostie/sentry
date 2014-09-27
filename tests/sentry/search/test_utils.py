from __future__ import absolute_import

from sentry.constants import STATUS_RESOLVED
from sentry.testutils import TestCase
from sentry.search.utils import parse_query


class ParseQueryTest(TestCase):
    def test_simple(self):
        result = parse_query('foo bar', self.user)
        assert result == {'tags': {}, 'query': 'foo bar'}

    def test_mix_tag_and_query(self):
        result = parse_query('foo bar key:value', self.user)
        assert result == {'tags': {'key': 'value'}, 'query': 'foo bar'}

    def test_single_tag(self):
        result = parse_query('key:value', self.user)
        assert result == {'tags': {'key': 'value'}, 'query': ''}

    def test_multiple_tags(self):
        result = parse_query('foo:bar key:value', self.user)
        assert result == {'tags': {'key': 'value', 'foo': 'bar'}, 'query': ''}

    def test_single_tag_with_quotes(self):
        result = parse_query('foo:"bar"', self.user)
        assert result == {'tags': {'foo': 'bar'}, 'query': ''}

    def test_tag_with_quotes_and_query(self):
        result = parse_query('key:"a value" hello', self.user)
        assert result == {'tags': {'key': 'a value'}, 'query': 'hello'}

    def test_is_resolved(self):
        result = parse_query('is:resolved', self.user)
        assert result == {'status': STATUS_RESOLVED, 'tags': {}, 'query': ''}

    def test_assigned_me(self):
        result = parse_query('assigned:me', self.user)
        assert result == {'assigned_to': self.user, 'tags': {}, 'query': ''}