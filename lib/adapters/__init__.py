from sys import argv
from importlib import import_module

from conf.configs import adapter


# Import the module of the configured adapter and make it accessible with the variable adapterModule
adapterModule = import_module("lib.adapters."+adapter)

# Make all attributes of adapterModule directly accessible (Simulation for from <module> import *)
globals().update(
            {n: getattr(adapterModule, n) for n in adapterModule.__all__} if hasattr(adapterModule, '__all__') 
            else 
            {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')}
          )