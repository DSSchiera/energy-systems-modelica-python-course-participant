"""Run OpenModelica from Python (native `omc` or Docker) and load its results (Session 3 onward).

Modules:
    runner.py    simulate(), flatten(): write a .mos script, run omc, return the CSV / flat model
    results.py   read_result(): CSV result file -> pandas DataFrame indexed by time
"""
