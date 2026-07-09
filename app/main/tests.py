from django.test import TestCase


class RobotsTxtTests(TestCase):
    def test_robots_txt_blocks_all_crawlers(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn(b'User-agent: *', response.content)
        self.assertIn(b'Disallow: /', response.content)
