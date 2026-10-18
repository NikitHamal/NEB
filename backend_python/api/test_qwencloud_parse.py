"""Offline tests for qwencloud response parsing (no network — fabricated frames)."""
from django.test import SimpleTestCase

from api import qwencloud_proxy as qc


def _msg(text, ptype="Text", role="assistant"):
    return {
        "role": role,
        "contentList": [
            {"jsonPath": "/contentList/0/type", "content": ptype},
            {"jsonPath": "/contentList/0/content", "content": text},
        ],
    }


class QwencloudParseTests(SimpleTestCase):
    def test_single_message_cumulative_deltas(self):
        prev = {}
        e1, s1, _ = qc._extract_message_deltas([_msg("ap")], prev)
        e2, s2, _ = qc._extract_message_deltas([_msg("apple")], prev)
        self.assertTrue(s1 and s2)
        self.assertEqual([e["content"] for e in e1 + e2], ["ap", "ple"])

    def test_static_greeting_does_not_poison_answer(self):
        prev = {}
        snap1 = [_msg("Hi there! How can I help you today?"), _msg("ap")]
        snap2 = [_msg("Hi there! How can I help you today?"), _msg("apple")]
        e1, _, _ = qc._extract_message_deltas(snap1, prev)
        e2, _, _ = qc._extract_message_deltas(snap2, prev)
        texts = [e["content"] for e in e1 + e2 if e["type"] == "text"]
        self.assertEqual(texts, ["Hi there! How can I help you today?", "ap", "ple"])
        self.assertIn("apple", "".join(texts))

    def test_role_case_insensitive(self):
        prev = {}
        events, saw, _ = qc._extract_message_deltas([_msg("hi", role="Assistant")], prev)
        self.assertTrue(saw)
        self.assertEqual(events[0]["content"], "hi")

    def test_user_messages_ignored(self):
        prev = {}
        events, saw, _ = qc._extract_message_deltas([_msg("hello", role="user")], prev)
        self.assertFalse(saw)
        self.assertEqual(events, [])

    def test_unrecognized_shape_counted(self):
        prev = {}
        weird = [{"role": "assistant", "contentList": [{"jsonPath": "/weird", "content": "x"}]}]
        events, saw, unparsed = qc._extract_message_deltas(weird, prev)
        self.assertFalse(saw)
        self.assertEqual(events, [])
        self.assertEqual(unparsed, 1)

    def test_deepthink_goes_to_thought(self):
        prev = {}
        events, saw, _ = qc._extract_message_deltas([_msg("let me think", ptype="DeepThink")], prev)
        self.assertTrue(saw)
        self.assertEqual(events[0]["type"], "thought")

    def test_empty_text_guarded_without_network(self):
        chunks = list(qc._stream_predict(None, "anon", "qwen3.8-max", "s", "t", "   ",
                                         "", False, 4000, 0.7, 0.8, False))
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["type"], "error")
        self.assertIn("no user content", chunks[0]["error"])
