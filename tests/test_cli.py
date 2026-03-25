import json
import os
import re
import sys
from subprocess import PIPE, Popen

from cpuinfo import cpuinfo


def test_json():
	command = [sys.executable, 'cpuinfo/cpuinfo.py', '--json']
	p1 = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p1.communicate()[0]

	assert p1.returncode == 0

	output = output.decode(encoding='UTF-8')

	info = json.loads(output, object_hook=cpuinfo._utf_to_str)

	assert list(cpuinfo.CPUINFO_VERSION) == info['cpuinfo_version']
	assert info['cpuinfo_version_string'] == cpuinfo.CPUINFO_VERSION_STRING


def test_version():
	command = [sys.executable, 'cpuinfo/cpuinfo.py', '--version']
	p1 = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p1.communicate()[0]

	assert p1.returncode == 0

	output = output.decode(encoding='UTF-8')
	output = output.strip()

	assert output == cpuinfo.CPUINFO_VERSION_STRING


def test_trace():
	# Get all log files before test
	before_log_files = [
		f
		for f in os.listdir('.')
		if os.path.isfile(f) and re.match(r'^cpuinfo_trace_\d+-\d+-\d+_\d+-\d+-\d+-\d+.trace$', f)
	]
	# print('\n', before_log_files)

	# Run with trace to generate new log file
	command = [sys.executable, 'cpuinfo/cpuinfo.py', '--trace']
	p1 = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p1.communicate()[0]
	assert p1.returncode == 0

	# Get all log files after test
	after_log_files = [
		f
		for f in os.listdir('.')
		if os.path.isfile(f) and re.match(r'^cpuinfo_trace_\d+-\d+-\d+_\d+-\d+-\d+-\d+.trace$', f)
	]
	# print('\n', after_log_files)

	# Read the new log file into a string
	new_log_file = list(set(after_log_files) - set(before_log_files))[0]
	with open(new_log_file) as f:
		output = f.read().strip()

	# Remove the new log file
	os.remove(new_log_file)

	assert len(output) > 200
	assert output.startswith('!' * 80)
	assert output.endswith('!' * 80)


def test_default():
	command = [sys.executable, 'cpuinfo/cpuinfo.py']
	p1 = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p1.communicate()[0]

	assert p1.returncode == 0

	output = output.decode(encoding='UTF-8')

	version = output.split('Cpuinfo Version: ')[1].split('\n')[0].strip()

	assert version == cpuinfo.CPUINFO_VERSION_STRING
