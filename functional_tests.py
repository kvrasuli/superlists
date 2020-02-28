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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_element_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Купить павлиньи перья' for row in rows)
		)
		#текстовое поле приглашает ее ввести элемент 2
		#она вводит "сделать мушку из павлиньих перьев"
		#эдит очень методична
		self.fail('Закончить тест!')
		
		#страница обновляется и теперь в спике 2 элемента

		#эдит интересно запомнился ли ее список. сайт сгенерировал для нее уникальный URL и об этом выводится небольшой текст с пояснениями

		#она посещает этот URL и ее список еще там

		#ей нравки и она идет спать


if __name__ == '__main__':
	unittest.main(warnings='ignore')
