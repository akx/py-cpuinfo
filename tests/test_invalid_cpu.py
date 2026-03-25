import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 1
	is_windows = False
	arch_string_raw = 'unknown_cpu'
	uname_string_raw = 'unknown_cpu'


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_arch_parse_unknown():
	# If the arch is unknown, the result should be null
	arch, bits = cpuinfo._parse_arch(cpuinfo.DataSource.arch_string_raw)
	assert arch is None
	assert bits is None


def test_check_arch_exception():
	# If the arch is unknown, it should raise and exception
	try:
		cpuinfo._check_arch()
		pytest.fail('Failed to raise Exception')
	except Exception as err:
		assert (
			err.args[0]
			== 'py-cpuinfo currently only works on X86 and some ARM/LoongArch/MIPS/PPC/RISCV/SPARC/S390X CPUs.'
		)
