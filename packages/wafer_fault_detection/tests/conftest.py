import pytest
import os
import shutil


def pytest_sessionstart(session: "Session") -> None:
  os.makedirs('test_data')
  os.makedirs('test_logs')
  os.makedirs('validatedFile/good_data')
  os.makedirs('validatedFile/bad_data')
  

def pytest_sessionfinish(session, exitstatus):
  shutil.rmtree('test_data')
  shutil.rmtree('test_logs')
  shutil.rmtree('validatedFile')