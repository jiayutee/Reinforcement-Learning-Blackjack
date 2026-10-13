import unittest
from public_game.commands import apply_command
from public_game.session import PublicSession


class PublicCommandTests(unittest.TestCase):
    def test_round_and_stale_command(self):
        session = PublicSession(seed=7)
        view = apply_command(session,{'command':'deal','revision':0,'stake':20})
        self.assertEqual(view['balance'],180)
        self.assertIsNone(view['dealer'][1])
        view = apply_command(session,{'command':'stand','revision':1})
        self.assertEqual(view['profit'],-20)
        with self.assertRaises(ValueError):
            apply_command(session,{'command':'stand','revision':1})
        self.assertEqual(session.view(),view)

    def test_untrusted_shapes_and_claims_do_not_mutate(self):
        session = PublicSession(seed=7)
        before = session._state
        for payload in (None,[],{}, {'command':[]},
                        {'command':'deal','revision':True,'stake':20},
                        {'command':'deal','revision':-1,'stake':20},
                        {'command':'deal','revision':0,'stake':True},
                        {'command':'deal','revision':0,'stake':20,'balance':999},
                        {'command':'stand','revision':0,'profit':100},
                        {'command':'hit','revision':0,'stake':20},
                        {'command':'deal','revision':0}):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError): apply_command(session,payload)
                self.assertIs(session._state,before)
        control = PublicSession(seed=7)
        self.assertEqual(apply_command(session,{'command':'deal','revision':0,'stake':20}),
                         control.deal(20,0))
