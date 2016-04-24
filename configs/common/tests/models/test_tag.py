"""
confi.gs common app tests for models/entity.py
"""
# django
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
# confi.gs
from common.models import Tag


class TagTestCase(TestCase):

    def setUp(self):
        Tag.objects.create(
            name="Test Tag 1"
        )
        Tag.objects.create(
            name="Test Tag 2",
        )

    def test_tag(self):
        tag = Tag.objects.get(
            name='Test Tag 1',
        )
        tags = Tag.objects.all()

        self.assertEqual(tag.name, 'Test Tag 1')
        self.assertEqual(tags.count(), 2)

    def test_tag_duplicate(self):
        duplicate_tag = Tag(
            name="Test Tag 1"
        )
        with self.assertRaises(ValidationError):
            duplicate_tag.full_clean()
        with self.assertRaises(IntegrityError):
            duplicate_tag.save()

    def test_tag_blank(self):
        blank_tag = Tag(
            name=""
        )
        with self.assertRaises(ValidationError):
            blank_tag.full_clean()

    def test_tag_name_to_long(self):
        long_tag = Tag(
            name="test"*128
        )
        with self.assertRaises(ValidationError):
            long_tag.full_clean()


