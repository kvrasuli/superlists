from .base import  FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
	'''тест нового посетителя'''
	def test_can_start_a_list_for_one_user(self):
		'''тест: можно начать список для одного пользователя'''
		#эдит слышала про приложение с онлайн списком по адресу
		self.browser.get(self.live_server_url)
		#заголовок и шапка говорит что это список неотложных дел
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#ей предлагается ввести элемент списка
		inputbox = self.get_item_input_box()
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
		self.add_list_item('Сделать мушку из павлиньих перьев')
		
		#страница обновляется и теперь в спике 2 элемента
		self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
		self.wait_for_row_in_list_table('1: Купить павлиньи перья')

		#эдит интересно запомнился ли ее список. сайт сгенерировал для нее уникальный URL и об этом выводится небольшой текст с пояснениями
		#она посещает этот URL и ее список еще там
		#ей нравки и она идет спать

	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''тест: многочисленные пользователи могут начать списки по разным url'''
		# эдит начинает новый спписок
		self.browser.get(self.live_server_url)
		self.add_list_item('Сделать мушку из павлиньих перьев')

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
		self.add_list_item('Купить молоко')

		#френсис получает уникальный  URL-адрес
		fransis_list_url = self.browser.current_url
		self.assertRegex(fransis_list_url,'/lists/.+')
		self.assertNotEqual(fransis_list_url, edith_list_url)

		#опять таки нет ни следа от списка эдит
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиньи перья', page_text)
		self.assertIn('Купить молоко', page_text)

		#удовлетворенные они ложаться спать (you know what i mean)

