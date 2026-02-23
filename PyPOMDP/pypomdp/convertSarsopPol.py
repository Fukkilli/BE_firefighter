#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:26:16 2021

@author: c.ponzoni
"""
import argparse
from html.parser import HTMLParser
from util.alpha_vector import AlphaVector
from util.json_encoder import toJSON
import numpy as np

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        if tag == "alphavector":
            self.alpha_vecs = []
            for attr in attrs:
                print("     attr:", attr)
                if 'vectorlength' in attr[0]:
                    self.vsize=int(attr[1])
                    print("SIZE ", self.vsize)
        if tag == "vector":
            for attr in attrs:
                if "action" in attr[0]:
                    action = int(attr[1])
                    if action == 0:
                        action = "manu"
                    elif action == 1:
                        action = "auto"
                    
                    self.alpha = AlphaVector(a=action,v=np.zeros(self.vsize))
                    print(self.alpha)
        

    def handle_endtag(self, tag):
        print("End tag  :", tag)
        if tag == "alphavector":
            print(self.alpha_vecs)
            encoder = toJSON("alphavecfileconverted.policy",self.alpha_vecs)
            encoder.write_json()

    def handle_data(self, data):
        print("Data     :", data)
        self.add_alpha(data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        #c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

        
    def starting(self):
        self.alpha_vecs = []
        self.action_list = []
        
    def add_alpha(self, data):
        #print("Adding alphavectors")
        values = data.split(" ")
        values.pop()
        print(values, len(values))
        self.v = []
        if len(values) == self.vsize:
            for v in values:
                self.v.append(float(v))
            #v = np.asarray(values, dtype=np.float64, order='C')
            print(self.v)
            self.alpha.v = self.v
            self.alpha_vecs.append(self.alpha)
        
        
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Converting Sarsop policy file')
    parser.add_argument('--policyfile', type=str, default='sarsop.policy', help='alphaVec policy file')
    
    args = vars(parser.parse_args())
    print(args['policyfile'])
    
    with open (args['policyfile'], "r") as myfile:
        data = myfile.read().replace('\n', '')
    myfile.close()
    html_parser = MyHTMLParser()
    html_parser.starting()
    html_parser.feed(data)
    