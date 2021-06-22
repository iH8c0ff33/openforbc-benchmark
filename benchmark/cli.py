from __future__ import print_function, unicode_literals
import time 
from tasks import run
import subprocess
from pprint import pprint
from celery import uuid
from PyInquirer import prompt
import json


class UserMenu:
    def __init__(self):
        self.selectBenchmark:dict
        self.gpuUsage:float
        self.runnerDict:dict

    def runner(self):
        benchmarks = [{
            'type': 'checkbox',
            'message': 'Select Benchmark',
            'name': 'benchmark',
            'choices': [ 
                {'name': 'MLPerf'},
                {'name': '3D Mark'},
                {'name': 'Unigine Heaven'},
                {'name': 'Dummy Benchmark'}
            ],
            'validate': lambda answer: 'You must choose at least one Benchmark to run.' \
                if len(answer) == 0 else True
        }]
        self.selectBenchmark = prompt(benchmarks)
        gpuUsage = [
            {'type':'input',
             'name':'gpuUsage',
             'message':'How much GPU usage do you want to assign?',
             'validate': lambda val: float(val)>0.0 and float(val)<1.0
            }
        ]
        self.gpuUsage = prompt(gpuUsage)
        self.runnerDict = {**self.selectBenchmark,**self.gpuUsage}
        pprint(self.runnerDict)
        with open("../config/benchmarkconfig.json","w") as configFile:
            json.dump(self.runnerDict,configFile)


if __name__ == "__main__":
    inst = UserMenu()
    inst.runner()