from django.test import TestCase
import accounts.views
from unittest.mock import patch


class SendLoginEmailViewTest(TestCase):
    '''тест представления, которое отправляет сообщение для входа в систему'''
    
    def test_redirects_to_home_page(self):
        '''тест: переадресуется на домашнюю страницу'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        '''тест: отправляется сообщение на адрес из метода post'''

        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        '''тест: добавляется сообщение об успехе'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email"
        )
        self.assertEqual(message.tags, "success")

class LoginViewTest(TestCase):
    '''тест представления входа в систему'''

    def test_redirects_to_home_page(self):
        '''тест: переадерсуется на домашнюю страницу'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')