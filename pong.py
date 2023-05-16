import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum

if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download"
          "it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s
                  for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    
