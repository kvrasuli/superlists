from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	'''тест нового посетителя'''
	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()

	def tearDown(self):
		'''демонтаж'''
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		'''подтверждение строки в таблице списка'''
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,  [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		'''тест: можно начать список и получить его позже'''
		#эдит слышала про приложение с онлайн списком по адресу
		self.browser.get('http://localhost:8000')
		#заголовок и шапка говорит что это список неотложных дел
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)


		#ей предлагается ввести элемент списка
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#она набирает "купить павлиньи перья"
		#ее хобби - вязание рыболовных мушек
		inputbox.send_keys('Купить павлиньи перья')

		#она нажимает ентер, страница обновляется, и теперь страница содержит "1: купить павлиньи перья" как элемент списка
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		self.check_for_row_in_list_table('1: Купить павлиньи перья')

		#текстовое поле приглашает ее ввести элемент 2
		#она вводит "сделать мушку из павлиньих перьев"
		#эдит очень методична
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Сделать мушку из павлиньих перьев')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		
		#страница обновляется и теперь в спике 2 элемента
		self.check_for_row_in_list_table('1: Купить павлиньи перья')
		self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

		#эдит интересно запомнился ли ее список. сайт сгенерировал для нее уникальный URL и об этом выводится небольшой текст с пояснениями

		#она посещает этот URL и ее список еще там

		#ей нравки и она идет спать
		self.fail('Закончить тест!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
