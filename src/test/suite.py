from test_reset import TestReset
from test_post import TestPost
from test_get import TestGet
from test_put import TestPut
from test_patch import TestPatch
from test_delete import TestDelete
import argparse
import os
import unittest


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReset))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPost))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGet))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPut))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPatch))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDelete))
    return test_suite


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action='store', type=str, default='127.0.0.1', required=False)
    parser.add_argument('--port', action='store', type=int, default=8080, required=False)
    parser.add_argument('-v', '--verbose', action='store', type=int, default=2, required=False)
    parser.add_argument('--docker', action='store_true', default=False, required=False)
    args = parser.parse_args()

    if args.docker:
        args.host = '0.0.0.0'
        args.port = 8080

    # env variable
    base_url = f'http://{args.host}:{args.port}'
    # print(f'base_url [{base_url}]')
    os.environ['BASE_URL'] = base_url

    mySuit = suite()
    runner = unittest.TextTestRunner(verbosity=args.verbose)
    runner.run(mySuit)
