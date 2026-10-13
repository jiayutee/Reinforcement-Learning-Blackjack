import http.client
import json
import re
import threading
import unittest
from public_game.local_game import make_server


class PublicHTTPTests(unittest.TestCase):
    def test_round_auth_and_stale_requests(self):
        server=make_server(0,7)
        thread=threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        connection=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
        try:
            connection.request('GET','/')
            response=connection.getresponse(); page=response.read().decode()
            self.assertEqual(response.status,200)
            token=re.search("const token='([^']+)'",page).group(1)
            headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{server.server_port}','X-Game-Token':token}
            def post(payload, supplied=headers):
                connection.request('POST','/command',json.dumps(payload),supplied)
                response=connection.getresponse()
                return response.status,json.loads(response.read())
            code,_=post({'command':'deal','revision':0,'stake':20},{'Content-Type':'application/json'})
            self.assertEqual(code,403)
            code,view=post({'command':'deal','revision':0,'stake':20})
            self.assertEqual(code,200); self.assertIsNone(view['dealer'][1])
            code,stale=post({'command':'hit','revision':0})
            self.assertEqual(code,409); self.assertEqual(stale['state'],view)
            code,done=post({'command':'stand','revision':1})
            self.assertEqual(code,200); self.assertEqual(done['profit'],-20)
        finally:
            connection.close(); server.shutdown(); server.server_close(); thread.join()
