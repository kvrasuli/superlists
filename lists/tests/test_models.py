from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List
from  django.contrib.auth import get_user_model

User = get_user_model()

class ItemModelsTest(TestCase):
	'''тест модели элемента'''
	
	def test_default_text(self):
		'''тест заданного по умолчанию текста'''
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		'''тест: элемент связан со списком'''
		list_ =  List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())

	def test_cannot_save_empty_list_items(self):
		'''тест: нельзя добавлять пустые элементы списка'''
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()

class ListModelsTest(TestCase):
	'''тест модели списка'''

	def test_get_absolute_url(self):
		'''тест: получен абсолютный url'''
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

	def test_lists_can_have_owners(self):
		'''тест: списки могут иметь владельцев'''
		user = User.objects.create(email='a@b.com')
		list_ = List.objects.create(owner=user)
		self.assertIn(list_, user.list_set.all())

	def test_list_owner_is_optional(self):
		'''тест: владелец списка является необязательным'''
		List.objects.create() # не должно поднимать исключения

	def test_duplicate_items_are_invalid(self):
		'''тест: повторы элементов не допустимы'''
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='bla')
		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='bla')
			item.full_clean()
			# item.save()

	def test_CAN_save_same_item_to_different_lists(self):
		'''тест: МОЖЕТ сохранить тот же элемент в разные списки'''
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean() # не должен поднять исключение

	def test_list_ordering(self):
		'''тест упорядочения списка'''
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='i1')
		item2 = Item.objects.create(list=list1, text='item2')
		item3 = Item.objects.create(list=list1, text='3')
		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3]
		)
	
	def test_string_representation(self):
		'''тест строкового представления'''
		item = Item(text='some text')
		self.assertEqual(str(item), 'some text')

	def test_list_name_is_first_item_text(self):
		'''тест: имя списка является текстом первого элемента'''
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='first item')
		Item.objects.create(list=list_, text='second item')
		self.assertEqual(list_.name, 'first item')

