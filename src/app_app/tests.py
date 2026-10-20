from django.conf import settings
from django.test import TestCase
from .models import ProductoRopa

# Create your tests here.
class SumaTest(TestCase):
    def test_suma_correcta(self):
        response = self.client.post('/', {'num1': '10', 'num2': '15'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultado: 25.0')

    def test_guarda_producto_en_base_seleccionada(self):
        response = self.client.post('/', {
            'guardar_ropa': '1',
            'db_activa': 'default',
            'nombre_ropa': 'Camiseta',
            'categoria_ropa': 'CAMISA',
            'talla_ropa': 'M',
            'precio_ropa': '19.99',
        })

        self.assertRedirects(response, '/?db=default')
        self.assertTrue(ProductoRopa.objects.using('default').filter(nombre='Camiseta').exists())

    def test_selector_solo_muestra_bases_configuradas(self):
        response = self.client.get('/')

        expected_options = [
            {'alias': alias, 'label': label}
            for alias, label in settings.DATABASE_LABELS.items()
        ]
        self.assertEqual(response.context['database_options'], expected_options)