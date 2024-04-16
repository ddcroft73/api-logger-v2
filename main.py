#!/usr/bin/python3

from logger.api_logger_v2 import logzz

def demo():
    
    for i in ['bug', 'crap', 'car', 'helicopter']:
        print(i)
    logzz.info("This is a test")


if __name__ == "__main__":
    demo()