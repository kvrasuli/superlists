from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import  FunctionalTest

class ItemValidationTest(FunctionalTest):
	'''тест валидации элемента списка'''
	def test_cannot_add_empty_list_items(self):
		'''тест: нельзя добавлять пустые элементы списка'''
		# эдит открывает домашнюю страницу и случайно пытается отправить
		# пустой элемент списка. Она нажимает Enter на пустом поле ввода
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		#браузер перехватывает запрос и не загружает страницу со списком

		#домашняя страница  обновляется, и появляется сообщение об ошибке,
		#которое говорит, что элементы списка не должны быть пустыми
		self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

		#эдит начинает набирать текст нового элемента и ошибка исчезает
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))

		#как ни странно, эдит решает отправить второй пустой элемент списка
		self.get_item_input_box().send_keys(Keys.ENTER)

		#и снова браузер не подчинился
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
		
		#и она может его исправить, заполнив поле неким текстом
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		'''тест: нельзя добавлять повторяющиеся элементы'''
		#эдит открывают домашнюю страницу и начинает новый список
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wellies')

		#она случайно пытается ввести повторяющийся элемент
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		#она видит полезное сообщение об ошибке
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text, 
			"You've already got this in your list"
			))

		