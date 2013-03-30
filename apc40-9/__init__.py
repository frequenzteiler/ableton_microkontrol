# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.5)

from APC40 import APC40

def create_instance(c_instance):
    return APC40(c_instance)

from _Framework.Capabilities import *

def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(vendor_id = 2536, product_ids = [
            115], model_name = 'Akai APC40'),
        PORTS_KEY: [
            inport(props = [
                NOTES_CC,
                SCRIPT,
                REMOTE]),
            outport(props = [
                SCRIPT,
                REMOTE])] }

