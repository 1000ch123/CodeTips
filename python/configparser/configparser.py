# -*- coding: utf-8 -*-

import configparser as cp

if __name__ == '__main__':
    config = cp.ConfigParser()
    config["host"] = "localhost"
    config["port"] = 12345
