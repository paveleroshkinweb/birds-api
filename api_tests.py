import unittest
import json
import random
from api import app


def parse_bytes_to_json(data):
    return json.loads(data.decode('utf-8').replace("'", '"'))

class ApiTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    def tearDown(self):
        pass

    def test_get_version(self):
        response = self.app.get('/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Birds Service. Version 0.1')

    def test_get_birds(self):
        response = self.app.get('/birds')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertGreaterEqual(len(data), 27)
    
    def test_get_birds_with_params(self):

        response = self.app.get('/birds?attribute=asdf')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, b'Invalid attribute value asdf. Please use value from: species name color body_length wingspan')

        response = self.app.get('/birds?attribute=color&order=asf')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, b'Invalid order value asf. Please use value from: asc desc')

        response = self.app.get('/birds?attribute=color&order=asc&offset=-5')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, b'Invalid offset value -5. Offset value should be positive integer')

        response = self.app.get('/birds?attribute=color&order=asc&offset=5&limit=0')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, b'Invalid limit value 0. Limit value should be positive integer')

        response = self.app.get('/birds?attribute=color&order=asc&limit=1000')
        self.assertEqual(response.status_code, 200)
        all_data = parse_bytes_to_json(response.data)
        self.assertGreaterEqual(len(all_data), 27)

        response = self.app.get('/birds?attribute=color&order=asc&offset=5&limit=5')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertEqual(len(data), 5)

        response = self.app.get('/birds?offset=100000')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertEqual(len(data), 0)

        response = self.app.get('/birds?offset=1&limit=1000')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertEqual(len(data), len(all_data) - 1)

        response = self.app.get('/birds?attribute=name&order=asc')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertLessEqual(data[0]['name'], data[1]['name'])

        response = self.app.get('/birds?attribute=color&order=asc&offset=5&limit=5')
        self.assertEqual(response.status_code, 200)
        data = parse_bytes_to_json(response.data)
        self.assertEqual(len(data), 5)
        self.assertLessEqual(data[0]['color'], data[1]['color'])
    
    def test_post_birds(self):
        
        error_msg = b'Invalid json. Please fill all fields: species, name, color, body_length, wingspan. body_length and wingspan should be positive integers'

        response = self.app.post('/birds', json={
            'species':'sdf',
            'name':'pasha',
            'color':'red'
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, error_msg)

        response = self.app.post('/birds', json={
            'species':'asd',
            'name':'pasha',
            'color':'red',
            'body_length':5,
            'wingspan':5
        })
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.data.startswith(b'invalid input value for enum bird_species'))

        response = self.app.post('/birds', json={
            'species':'pigeon',
            'name':'pasha',
            'color':'asdf',
            'body_length':5,
            'wingspan':5
        })
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.data.startswith(b'invalid input value for enum bird_color'))

        response = self.app.post('/birds', json={
            'species':'pigeon',
            'name':'pasha',
            'color':'red',
            'body_length':-5,
            'wingspan':5
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, error_msg)

        response = self.app.post('/birds', json={
            'species':'pigeon',
            'name':'pasha',
            'color':'red',
            'body_length':5,
            'wingspan':-5
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, error_msg)
        
        response = self.app.post('/birds', json={
            'species':'pigeon',
            'name':'Tima',
            'color':'red',
            'body_length':5,
            'wingspan':5
        })
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.data.startswith(b'duplicate key value violates unique constraint'))

        bird_json = {
            'species':'pigeon',
            'name':f'Kiriora {random.randint(0, 10**6)}',
            'color':'red',
            'body_length':5,
            'wingspan':5
        }
        response = self.app.post('/birds', json=bird_json)
        self.assertEqual(response.status_code, 200)
        returned_bird = parse_bytes_to_json(response.data)
        self.assertEqual(returned_bird, bird_json)

if __name__ == '__main__':
    unittest.main()