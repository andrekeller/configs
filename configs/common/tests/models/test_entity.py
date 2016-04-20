"""
confi.gs common app tests for models/entity.py
"""
# django
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
# confi.gs
from common.models import Entity


class EntityTestCase(TestCase):

    def setUp(self):
        Entity.objects.create(
            name="Test Entity"
        )
        Entity.objects.create(
            name="Test Entity with Notes",
            notes="Some notes about the test entity",
        )

    def test_entity(self):
        entity = Entity.objects.get(
            name='Test Entity',
        )
        entity_with_notes = Entity.objects.get(
            name='Test Entity with Notes',
        )
        entities = Entity.objects.all()

        self.assertEqual(entity.name, 'Test Entity')
        self.assertEqual(entity.notes, None)
        self.assertEqual(entity_with_notes.notes, "Some notes about the test entity")
        self.assertEqual(entities.count(), 2)

    def test_entity_duplicate(self):
        duplicate_entity = Entity(
            name="Test Entity"
        )
        with self.assertRaises(ValidationError):
            duplicate_entity.full_clean()
        with self.assertRaises(IntegrityError):
            duplicate_entity.save()

    def test_entity_blank(self):
        blank_entity = Entity(
            name=""
        )
        with self.assertRaises(ValidationError):
            blank_entity.full_clean()

    def test_entity_name_to_long(self):
        blank_entity = Entity(
            name="test"*128
        )
        with self.assertRaises(ValidationError):
            blank_entity.full_clean()


