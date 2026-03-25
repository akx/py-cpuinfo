from cpuinfo import cpuinfo
from cpuinfo.cpuinfo import Trace
from tests import helpers


class MockDataSource_enforcing:
	@staticmethod
	def has_sestatus():
		return True

	@staticmethod
	def sestatus_b():
		returncode = 0
		output = r'''
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      31
'''
		return returncode, output


class MockDataSource_not_enforcing:
	@staticmethod
	def has_sestatus():
		return True

	@staticmethod
	def sestatus_b():
		returncode = 0
		output = r'''
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   eating
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      31
'''
		return returncode, output


class MockDataSource_exec_mem_and_heap:
	@staticmethod
	def has_sestatus():
		return True

	@staticmethod
	def sestatus_b():
		returncode = 0
		output = r'''
allow_execheap                  on
allow_execmem                   on
'''
		return returncode, output


class MockDataSource_no_exec_mem_and_heap:
	@staticmethod
	def has_sestatus():
		return True

	@staticmethod
	def sestatus_b():
		returncode = 0
		output = r'''
allow_execheap                  off
allow_execmem                   off
'''
		return returncode, output


trace = Trace(False, False)


def test_enforcing(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource_enforcing, monkeypatch)
	assert cpuinfo._is_selinux_enforcing(trace) is True


def test_not_enforcing(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource_not_enforcing, monkeypatch)
	assert cpuinfo._is_selinux_enforcing(trace) is False


def test_exec_mem_and_heap(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource_exec_mem_and_heap, monkeypatch)
	assert cpuinfo._is_selinux_enforcing(trace) is False


def test_no_exec_mem_and_heap(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource_no_exec_mem_and_heap, monkeypatch)
	assert cpuinfo._is_selinux_enforcing(trace) is True
