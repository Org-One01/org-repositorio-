from django.test import TestCase

# Create your tests here.
class SumaTest(TestCase):
    def test_suma_correcta(self):
        response = self.client.post('/', {'num1': '10', 'num2': '15'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultado: 25.0')