import json
from django.test import TestCase, Client
from django.urls import reverse


class NebyNeedleP5Tests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_p5_art_tool_execution(self):
        url = reverse('web:ajax_neby_assist')
        payload = {
            'tool': 'generate_p5_art',
            'args': {
                'prompt': 'glowing cosmic nebula',
                'style': 'generative',
                'color_palette': 'neon',
                'complexity': 'high',
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('result', data)
        result = data['result']
        self.assertEqual(result['style'], 'generative')
        self.assertEqual(result['color_palette'], 'neon')
        self.assertIn('setup = function()', result['code'])

    def test_generate_p5_art_cloud_routing_parse(self):
        from web.views_needle import _parse_cloud_reply, _execute_tool

        raw_reply = json.dumps({
            "tool_call": {
                "name": "generate_p5_art",
                "arguments": {
                    "prompt": "sunset wave landscape",
                    "style": "landscape",
                    "color_palette": "warm"
                }
            }
        })

        parsed = _parse_cloud_reply(raw_reply)
        self.assertIsNotNone(parsed)
        kind, name, args, text = parsed
        self.assertEqual(kind, 'tool')
        self.assertEqual(name, 'generate_p5_art')
        self.assertEqual(args['prompt'], 'sunset wave landscape')

        exec_res = _execute_tool(name, args)
        self.assertEqual(exec_res['style'], 'landscape')
        self.assertIn('beginShape', exec_res['code'])
