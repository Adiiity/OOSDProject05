import unittest
import json
from game_library import Board,Tile,Player, Share
from Client import handle_request


class Test(unittest.TestCase):
    # setup
    def testcase_1(self):
        # input
        with open('admin-tester/state-tests/in0.json','r') as file:
            request = json.load(file)
            response = handle_request(request)
        # output
        with open('admin-tester/state-tests/out0.json','r') as file:
            output = json.load(file)

        return self.assertEqual(response,output)
    # place
    def testcase_2(self):
        # input
        with open('admin-tester/state-tests/in1.json','r') as file:
            request = json.load(file)
            response = handle_request(request)
        # output
        with open('admin-tester/state-tests/out1.json','r') as file:
            output = json.load(file)


        return self.assertEqual(response,output)

# buy
    def testcase_3(self):
        # input
        with open('admin-tester/state-tests/in2.json','r') as file:
            request = json.load(file)
            response = handle_request(request)
        # output
        with open('admin-tester/state-tests/out2.json','r') as file:
            output = json.load(file)


        return self.assertEqual(response,output)



if __name__ == '__main__':
    unittest.main()