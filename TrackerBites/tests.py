from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import BiteTrackerModel
from django.utils import timezone
import json
import uuid

class TrackerBitesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        today = timezone.now().date()
        self.bite = BiteTrackerModel.objects.create(
            user=self.user,
            bite_name="Test Bite",
            bite_calories=500,
            bite_date=today,
            bite_time='breakfast'  # Lowercase to match choices
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('TrackerBites:show_tracker_bites'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_show_tracker_bites(self):
        response = self.client.get(reverse('TrackerBites:show_tracker_bites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker_bites.html')

    def test_add_bite_calorie_entry(self):
        data = {
            'bite_name': 'New Bite',
            'bite_calories': 300,
            'bite_date': timezone.now().date(),
            'bite_time': 'lunch'
        }
        response = self.client.post(reverse('TrackerBites:add_bite_calorie_entry'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(BiteTrackerModel.objects.filter(bite_name='New Bite').exists())

    def test_add_bite_calorie_entry_ajax(self):
        data = {
            'bite_name': 'Ajax Bite',
            'bite_calories': 400,
            'bite_date': timezone.now().date().strftime('%Y-%m-%d'),
            'bite_time': 'dinner'
        }
        response = self.client.post(reverse('TrackerBites:add_bite_calorie_entry_ajax'), data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(BiteTrackerModel.objects.filter(bite_name='Ajax Bite').exists())

    def test_add_bite_calorie_entry_ajax_invalid(self):
        data = {
            'bite_name': 'Invalid Bite'
            # Missing required fields
        }
        response = self.client.post(reverse('TrackerBites:add_bite_calorie_entry_ajax'), data)
        self.assertEqual(response.status_code, 400)

    def test_get_bite_tracker_json(self):
        response = self.client.get(reverse('TrackerBites:get_bite_tracker_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)  # Should have our test bite

    def test_get_bite_tracker_json_by_date(self):
        today = timezone.now().date().strftime('%Y-%m-%d')
        response = self.client.get(
            reverse('TrackerBites:get_bite_tracker_json_by_date', kwargs={'date': today})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    # def test_get_bite_tracker_json_by_date_and_time(self):
    #     today = timezone.now().date().strftime('%Y-%m-%d')
    #     response = self.client.get(
    #         reverse('TrackerBites:get_bite_tracker_json_by_date_and_time', 
    #                kwargs={'date': today, 'time': 'Breakfast'})  # Capitalize to match view logic
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response['Content-Type'], 'application/json')
    #     data = json.loads(response.content)
    #     self.assertEqual(len(data), 1)

    def test_calculate_total_calories_by_date(self):
        today = timezone.now().date().strftime('%Y-%m-%d')
        # Add another bite to test sum
        BiteTrackerModel.objects.create(
            user=self.user,
            bite_name="Second Bite",
            bite_calories=1000,
            bite_date=timezone.now().date(),
            bite_time='lunch'
        )
        
        response = self.client.get(
            reverse('TrackerBites:calculate_total_calories_by_date', kwargs={'date': today})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data['total_calories'], 1500)  # 500 + 1000
        self.assertEqual(data['total_bites'], 2)
        self.assertEqual(data['total_calories_percentage'], 60.0)  # (1500/2500)*100

    def test_valid_time_choices(self):
        for time_choice, _ in BiteTrackerModel.time_choices:
            bite = BiteTrackerModel.objects.create(
                user=self.user,
                bite_name=f"Test {time_choice}",
                bite_calories=500,
                bite_date=timezone.now().date(),
                bite_time=time_choice
            )
            self.assertEqual(bite.bite_time, time_choice)

    def test_model_validation(self):
        with self.assertRaises(ValidationError):
            bite = BiteTrackerModel(
                user=self.user,
                bite_name="Invalid Time",
                bite_calories=500,
                bite_date=timezone.now().date(),
                bite_time='invalid_time'  # Invalid choice
            )
            bite.full_clean()

    def test_model_user_cascade(self):
        bite_id = self.bite.id
        self.user.delete()
        self.assertFalse(BiteTrackerModel.objects.filter(id=bite_id).exists())

    def test_model_date_nullable(self):
        bite = BiteTrackerModel.objects.create(
            user=self.user,
            bite_name="No Date",
            bite_calories=500,
            bite_time='breakfast',
            bite_date=None
        )
        self.assertIsNone(bite.bite_date)

    # def test_delete_bite_entry_ajax(self):
    #     response = self.client.post(
    #         reverse('TrackerBites:delete_bite_entry_ajax', kwargs={'id': self.bite.id})
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(BiteTrackerModel.objects.filter(id=self.bite.id).exists())

    # def test_edit_bite_entry_ajax(self):
    #     data = {
    #         'name': 'Updated Bite',
    #         'calories': '600',
    #         'date': timezone.now().date().strftime('%Y-%m-%d'),
    #         'time': 'lunch'
    #     }
    #     response = self.client.post(
    #         reverse('TrackerBites:edit_bite_entry_ajax', kwargs={'id': self.bite.id}),
    #         data
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     updated_bite = BiteTrackerModel.objects.get(id=self.bite.id)
    #     self.assertEqual(updated_bite.bite_name, 'Updated Bite')
    #     self.assertEqual(updated_bite.bite_calories, '600')