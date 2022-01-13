
from django.test import TestCase, Client
from correlation.models import User, Data_type, Correlation_data
from datetime import timedelta, datetime
from django.urls import reverse
import json


# Create your tests here.


class ViewsTestCase(TestCase):

    def setUp(self):
        self.type1 = Data_type.objects.create(type_name='pulse')
        self.type2 = Data_type.objects.create(type_name='steps')
        self.user1 = User.objects.create(username='TestUser1', password='123taz@111', email='test@mail.ru')
        self.user2 = User.objects.create(username='TestUser2', password='223taz@222', email='test2@mail.ru')
        self.client = Client()
        self.testObj = {
            "user_id": 1,
            "data": {
                "x_data_type": "steps",
                "y_data_type": "pulse",
                "x":[
                    {
                        "date": "2022-01-01",
                        "value": 0.5
                    },
                    {
                        "date": "2022-01-01",
                        "value": 1.5
                    },
                    {
                        "date": "2022-01-01",
                        "value": 2.5
                    },
                ],
                "y":[
                    {
                        "date": "2022-01-01",
                        "value": 3.5
                    },
                    {
                        "date": "2022-01-01",
                        "value": 4.5
                    },
                    {
                        "date": "2022-01-01",
                        "value": 5.5
                    },
                    ]
                }
            }



    def test_create_correlation_success(self):
        y = json.dumps(self.testObj)
        self.add_calc = self.client.post( reverse('calculate'), data=y, content_type='application/json')
        self.assertEqual(self.add_calc.status_code, 200)

    def test_create_correlation_wrong_userid(self):
        obj = self.testObj.copy()
        obj['user_id'] = '55'
        y = json.dumps(obj)
        add_calc = self.client.post( reverse('calculate'), data=y, content_type='application/json')
        self.assertEqual(add_calc.status_code, 404)


    def test_create_correlation_wrong_type(self):
        obj = self.testObj.copy()
        obj['data']['x_data_type'] = 'WrongType'
        y = json.dumps(obj)
        add_calc = self.client.post( reverse('calculate'), data=y, content_type='application/json')
        self.assertEqual(add_calc.status_code, 404)

    def test_create_correlation_wrong_date(self):
        obj = self.testObj.copy()
        obj['data']['x'][0]['date'] = '15-14-2028'
        y = json.dumps(obj)
        add_calc = self.client.post( reverse('calculate'), data=y, content_type='application/json')
        self.assertEqual(add_calc.status_code, 404)

    def test_create_correlation_wrong_format_value(self):
        obj = self.testObj.copy()
        obj['data']['x'][0]['value'] = 'str'
        y = json.dumps(obj)
        add_calc = self.client.post( reverse('calculate'), data=y, content_type='application/json')
        self.assertEqual(add_calc.status_code, 404)

