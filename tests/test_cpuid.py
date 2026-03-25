import pytest

from cpuinfo import cpuinfo
from cpuinfo.cpuinfo import ASM, CPUID, platform
from tests import helpers


class MockASM(ASM):
	is_first = False

	def __init__(self, restype=None, argtypes=(), machine_code=[]):
		super().__init__(restype, argtypes, machine_code)

	def compile(self):
		self.func = self.run

	def run(self):
		machine_code = tuple(self.machine_code)

		# get_max_extension_support
		if machine_code == (
			b"\xb8\x00\x00\x00\x80"  # mov ax,0x80000000
			b"\x0f\xa2"  # cpuid
			b"\xc3",
		):  # ret
			return 0x8000001F

		# get_cache
		if machine_code == (
			b"\xb8\x06\x00\x00\x80"  # mov ax,0x80000006
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret))
			return 0x2006140

		# get_info
		if machine_code == (
			b"\xb8\x01\x00\x00\x00",  # mov eax,0x1"
			b"\x0f\xa2"  # cpuid
			b"\xc3",
		):  # ret
			return 0x800F82

		# get_processor_brand
		if machine_code == (
			b"\xb8\x02\x00\x00\x80",  # mov ax,0x80000002
			b"\x0f\xa2"  # cpuid
			b"\x89\xc0"  # mov ax,ax
			b"\xc3",
		):  # ret
			return 0x20444D41
		elif machine_code == (
			b"\xb8\x02\x00\x00\x80",  # mov ax,0x80000002
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x657A7952
		elif machine_code == (
			b"\xb8\x02\x00\x00\x80",  # mov ax,0x80000002
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x2037206E
		elif machine_code == (
			b"\xb8\x02\x00\x00\x80",  # mov ax,0x80000002
			b"\x0f\xa2"  # cpuid
			b"\x89\xd0"  # mov ax,dx
			b"\xc3",
		):  # ret
			return 0x30303732
		elif machine_code == (
			b"\xb8\x03\x00\x00\x80",  # mov ax,0x80000003
			b"\x0f\xa2"  # cpuid
			b"\x89\xc0"  # mov ax,ax
			b"\xc3",
		):  # ret
			return 0x69452058
		elif machine_code == (
			b"\xb8\x03\x00\x00\x80",  # mov ax,0x80000003
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x2D746867
		elif machine_code == (
			b"\xb8\x03\x00\x00\x80",  # mov ax,0x80000003
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x65726F43
		elif machine_code == (
			b"\xb8\x03\x00\x00\x80",  # mov ax,0x80000003
			b"\x0f\xa2"  # cpuid
			b"\x89\xd0"  # mov ax,dx
			b"\xc3",
		):  # ret
			return 0x6F725020
		elif machine_code == (
			b"\xb8\x04\x00\x00\x80",  # mov ax,0x80000004
			b"\x0f\xa2"  # cpuid
			b"\x89\xc0"  # mov ax,ax
			b"\xc3",
		):  # ret
			return 0x73736563
		elif machine_code == (
			b"\xb8\x04\x00\x00\x80",  # mov ax,0x80000004
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x2020726F
		elif machine_code == (
			b"\xb8\x04\x00\x00\x80",  # mov ax,0x80000004
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x20202020
		elif machine_code == (
			b"\xb8\x04\x00\x00\x80",  # mov ax,0x80000004
			b"\x0f\xa2"  # cpuid
			b"\x89\xd0"  # mov ax,dx
			b"\xc3",
		):  # ret
			return 0x202020

		# get_vendor_id
		if machine_code == (
			b"\x31\xc0",  # xor eax,eax
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x68747541
		elif machine_code == (
			b"\x31\xc0",  # xor eax,eax
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x444D4163
		elif machine_code == (
			b"\x31\xc0",  # xor eax,eax
			b"\x0f\xa2"  # cpuid
			b"\x89\xd0"  # mov ax,dx
			b"\xc3",
		):  # ret
			return 0x69746E65

		# get_flags
		if machine_code == (
			b"\xb8\x01\x00\x00\x00",  # mov eax,0x1"
			b"\x0f\xa2"  # cpuid
			b"\x89\xd0"  # mov ax,dx
			b"\xc3",
		):  # ret
			return 0x178BFBFF
		elif machine_code == (
			b"\xb8\x01\x00\x00\x00",  # mov eax,0x1"
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x7ED8320B
		elif machine_code == (
			b"\x31\xc9",  # xor ecx,ecx
			b"\xb8\x07\x00\x00\x00"  # mov eax,7
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x209C01A9
		elif machine_code == (
			b"\x31\xc9",  # xor ecx,ecx
			b"\xb8\x07\x00\x00\x00"  # mov eax,7
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x0
		elif machine_code == (
			b"\xb8\x01\x00\x00\x80"  # mov ax,0x80000001
			b"\x0f\xa2"  # cpuid
			b"\x89\xd8"  # mov ax,bx
			b"\xc3",
		):  # ret
			return 0x20000000
		elif machine_code == (
			b"\xb8\x01\x00\x00\x80"  # mov ax,0x80000001
			b"\x0f\xa2"  # cpuid
			b"\x89\xc8"  # mov ax,cx
			b"\xc3",
		):  # ret
			return 0x35C233FF

		# get_ticks
		# 32 bit
		if machine_code == (
			b"\x55",  # push bp
			b"\x89\xe5",  # mov bp,sp
			b"\x31\xc0",  # xor ax,ax
			b"\x0f\xa2",  # cpuid
			b"\x0f\x31",  # rdtsc
			b"\x8b\x5d\x08",  # mov bx,[di+0x8]
			b"\x8b\x4d\x0c",  # mov cx,[di+0xc]
			b"\x89\x13",  # mov [bp+di],dx
			b"\x89\x01",  # mov [bx+di],ax
			b"\x5d",  # pop bp
			b"\xc3",
		):  # ret
			raise Exception("FIXME: Add ticks for 32bit get_ticks")
		# 64 bit
		elif machine_code == (
			b"\x48",  # dec ax
			b"\x31\xc0",  # xor ax,ax
			b"\x0f\xa2",  # cpuid
			b"\x0f\x31",  # rdtsc
			b"\x48",  # dec ax
			b"\xc1\xe2\x20",  # shl dx,byte 0x20
			b"\x48",  # dec ax
			b"\x09\xd0",  # or ax,dx
			b"\xc3",
		):  # ret
			MockASM.is_first = not MockASM.is_first
			if MockASM.is_first:
				return 19233706151817
			else:
				return 19237434253761

		raise Exception("Unexpected machine code")

	def free(self):
		self.func = None


class MockDataSource:
	bits = '64bit'
	cpu_count = 1
	is_windows = platform.system().lower() == 'windows'
	arch_string_raw = 'INVALID'
	uname_string_raw = 'INVALID'
	can_cpuid = True


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)

	helpers.monkey_patch_asm(cpuinfo, MockASM, monkeypatch)


# Make sure this returns {} on an invalid arch
def test_return_empty():
	assert cpuinfo._get_cpu_info_from_cpuid() == {}


def test_normal():
	cpuid = CPUID()
	assert cpuid is not None

	assert not cpuid.is_selinux_enforcing

	max_extension_support = cpuid.get_max_extension_support()
	assert max_extension_support == 2147483679

	cache_info = cpuid.get_cache(max_extension_support)
	assert cache_info == {'size_b': (64 * 1024), 'line_size_b': 512, 'associativity': 6}

	info = cpuid.get_info()
	assert info == {'stepping': 2, 'model': 8, 'family': 23, 'processor_type': 0}

	processor_brand = cpuid.get_processor_brand(max_extension_support)
	assert processor_brand == 'AMD Ryzen 7 2700X Eight-Core Processor'

	hz_actual = cpuid.get_raw_hz()
	assert hz_actual == 3728101944

	vendor_id = cpuid.get_vendor_id()
	assert vendor_id == 'AuthenticAMD'

	flags = cpuid.get_flags(max_extension_support)
	assert flags == [
		'3dnowprefetch',
		'abm',
		'adx',
		'aes',
		'apic',
		'avx',
		'avx2',
		'bmi1',
		'bmi2',
		'clflush',
		'clflushopt',
		'cmov',
		'cmp_legacy',
		'cr8_legacy',
		'cx16',
		'cx8',
		'dbx',
		'de',
		'extapic',
		'f16c',
		'fma',
		'fpu',
		'fxsr',
		'ht',
		'lahf_lm',
		'lm',
		'mca',
		'mce',
		'misalignsse',
		'mmx',
		'monitor',
		'movbe',
		'msr',
		'mtrr',
		'osvw',
		'osxsave',
		'pae',
		'pat',
		'pci_l2i',
		'pclmulqdq',
		'perfctr_core',
		'perfctr_nb',
		'pge',
		'pni',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
		'rdseed',
		'sep',
		'sha',
		'skinit',
		'smap',
		'smep',
		'sse',
		'sse2',
		'sse4_1',
		'sse4_2',
		'sse4a',
		'ssse3',
		'svm',
		'tce',
		'topoext',
		'tsc',
		'vme',
		'wdt',
		'xsave',
	]
