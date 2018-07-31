#!/usr/bin/env python

import boto3
import json

def eval_compliance(rule_params):
    if "ConfigRules" in rule_params:
        rulesToCheck = list()
        