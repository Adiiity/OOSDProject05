import unittest
import json
from game_library import Board,Tile,Player, Share



class Test(unittest.TestCase):
    # setup
    def testcase_1(self):
        # input
        with open('admin-tester/state-tests/in0.json','r') as file:
            input = json.load(file)
        # output
        with open('admin-tester/state-tests/out0.json','r') as file:
            output = json.load(file)

        
        return self.assertEqual(input,output)
    # place
    def testcase_2(self):
        # input
        with open('admin-tester/state-tests/in1.json','r') as file:
            input = json.load(file)
        # output
        with open('admin-tester/state-tests/out1.json','r') as file:
            output = json.load(file)

        
        return self.assertEqual(input,output)

# buy
    def testcase_3(self):
        # input
        with open('admin-tester/state-tests/in2.json','r') as file:
            input = json.load(file)
        # output
        with open('admin-tester/state-tests/out2.json','r') as file:
            output = json.load(file)

        
        return self.assertEqual(input,output)
    


if __name__ == '__main__':
    unittest.main()