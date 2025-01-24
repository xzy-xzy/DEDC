import argparse

parser = argparse.ArgumentParser( )
parser.add_argument("--demo_n", default=4, type=int)
parser.add_argument("--test_n", default=4, type=int)
parser.add_argument("--shot", default=3, type=int)
parser.add_argument("--show_primitive", action="store_true")
parser.add_argument("--no_sys_gap", action="store_true")
parser.add_argument("--complete_sys_gap", action="store_true")
parser.add_argument("--convert_symbol", choices=["none", "anom", "cross"], default="none")
parser.add_argument("--model", default="gpt-4o-2024-08-06")
parser.add_argument("--api_key", default="none")


config = parser.parse_args( )
config.name = f"{config.demo_n}_to_{config.test_n}_shot{config.shot}"
if config.no_sys_gap:
    config.name += "_no_sys_gap"
if config.complete_sys_gap:
    config.name += "_complete_sys_gap"
if config.convert_symbol != "none":
    config.name += f"_{config.convert_symbol}"
if config.show_primitive:
    config.name += "_show_primitive"
