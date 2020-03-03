from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
	'''тест нового посетителя'''
	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		'''демонтаж'''
		self.browser.refresh()
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		'''ожидать строку в таблице списка'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text,  [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_layout_and_styling(self):
		'''тест макета и стилевого оформления'''
		# эдит открывает домашнюю страницу
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		#она замечает, что поле ввода аккуратно центрировано
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

		#она начинает новый список и видит что поле ввода там тоже аккуратно центрировано
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
		

	def test_can_start_a_list_for_one_user(self):
		'''тест: можно начать список для одного пользователя'''
		#эдит слышала про приложение с онлайн списком по адресу
		self.browser.get(self.live_server_url)
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


		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		#текстовое поле приглашает ее ввести элемент 2
		#она вводит "сделать мушку из павлиньих перьев"
		#эдит очень методична
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Сделать мушку из павлиньих перьев')
		inputbox.send_keys(Keys.ENTER)
		
		
		#страница обновляется и теперь в спике 2 элемента
		self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		#эдит интересно запомнился ли ее список. сайт сгенерировал для нее уникальный URL и об этом выводится небольшой текст с пояснениями

		#она посещает этот URL и ее список еще там

		#ей нравки и она идет спать
		# self.fail('Закончить тест!')

	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''тест: многочисленные пользователи могут начать списки по разным url'''
		# эдит начинает новый спписок
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Купить павлиньи перья')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		#она замечает, что ее список имеет уникальный URL-адрес
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#теперь новый пользователь, френсис, приходит на сайт
		## мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая инфа от эдит не прошла через куки и пр.
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		#френсис посещает дом. страницу, нет признаков списка эдит
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиньи перья', page_text)

		#френсис начинает свой список, вводя новый элемент
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Купить молоко')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить молоко')

		#френсис получает уникальный  URL-адрес
		fransis_list_url = self.browser.current_url
		self.assertRegex(fransis_list_url,'/lists/.+')
		self.assertNotEqual(fransis_list_url, edith_list_url)

		#опять таки нет ни следа от списка эдит
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиньи перья', page_text)
		self.assertIn('Купить молоко', page_text)

		#удовлетворенные они ложаться спать (you know what i mean)

	