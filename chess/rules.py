"""Load Piece Rules for Chess Game
Ethan Lew
elew@pdx.edu
"""

import os, glob, json


class RulesLoader:
    """load valid piece rules from a variety of representations"""
    @staticmethod
    def valid_rules(rules):
        """ensure that piece rules are valid"""
        required_keys = ["piece_name", "extensible", "blockable",
                         "capturable", "capture_group", "advance_group",
                         "x_symmetry", "y_symmetry"]
        for k in required_keys:
            if k not in rules:
                return False
        return True

    @classmethod
    def from_jsons(cls, directory):
        """load all rules from a directory containing JSON files"""
        assert os.path.exists(directory), f"directory {directory} does not exist"
        json_files = glob.glob(os.path.join(directory, "*.json"))
        loader = cls()
        for jfname in json_files:
            with open(jfname, 'r') as jfp:
                rules = json.load(jfp)
                if cls.valid_rules(rules):
                    loader.add_piece(rules)
                else:
                    print(f"WARNING: rule <{rules}> from {jfname} failed and won't be added")
        return loader

    def __init__(self):
        self._rules = {}

    def add_piece(self, rule):
        """given a dict describing piece rules, add to loaded rules"""
        self.valid_rules(rule)
        self._rules[rule["piece_name"].lower()] = rule

    def get_rules(self, name):
        if name.lower() in self._rules:
            return self._rules[name.lower()]
        else:
            return {}

    @property
    def piece_names(self):
        return [k for k, v in self._rules.items()]