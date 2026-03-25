from cpuinfo import cpuinfo


def test_to_decimal_string():
	assert cpuinfo._to_decimal_string('2.80') == '2.8'
	assert cpuinfo._to_decimal_string('2') == '2.0'
	assert cpuinfo._to_decimal_string(3) == '3.0'
	assert cpuinfo._to_decimal_string(6.5) == '6.5'
	assert cpuinfo._to_decimal_string(7.002) == '7.002'
	assert cpuinfo._to_decimal_string('4.00000000001') == '4.00000000001'
	assert cpuinfo._to_decimal_string('5.000000000000') == '5.0'

	assert cpuinfo._to_decimal_string('invalid') == '0.0'
	assert cpuinfo._to_decimal_string('8.778.9') == '0.0'
	assert cpuinfo._to_decimal_string('') == '0.0'
	assert cpuinfo._to_decimal_string(None) == '0.0'


def test_hz_short_to_full():
	assert cpuinfo._hz_short_to_full('2.8', 9) == (2800000000, 0)
	assert cpuinfo._hz_short_to_full('1.2', 6) == (1200000, 0)
	assert cpuinfo._hz_short_to_full('3.2', 9) == (3200000000, 0)
	assert cpuinfo._hz_short_to_full('9001.2', 6) == (9001200000, 0)
	assert cpuinfo._hz_short_to_full('0.0', 0) == (0, 0)
	assert cpuinfo._hz_short_to_full('2.87', 0) == (2, 87)

	assert cpuinfo._hz_short_to_full('invalid', 0) == (0, 0)
	assert cpuinfo._hz_short_to_full('8.778.9', 0) == (0, 0)
	assert cpuinfo._hz_short_to_full('', 0) == (0, 0)
	assert cpuinfo._hz_short_to_full(None, 0) == (0, 0)


def test_hz_friendly_to_full():
	assert cpuinfo._hz_friendly_to_full('2.80GHz') == (2800000000, 0)
	assert cpuinfo._hz_friendly_to_full('1.20 mHz') == (1200000, 0)
	assert cpuinfo._hz_friendly_to_full('3693.15-MHz') == (3693150000, 0)
	assert cpuinfo._hz_friendly_to_full('12 GHz') == (12000000000, 0)
	assert cpuinfo._hz_friendly_to_full('2.6 Hz') == (2, 6)
	assert cpuinfo._hz_friendly_to_full('0 Hz') == (0, 0)

	assert cpuinfo._hz_friendly_to_full('invalid') == (0, 0)
	assert cpuinfo._hz_friendly_to_full('8.778.9') == (0, 0)
	assert cpuinfo._hz_friendly_to_full('') == (0, 0)
	assert cpuinfo._hz_friendly_to_full(None) == (0, 0)


def test_hz_short_to_friendly():
	assert cpuinfo._hz_short_to_friendly('2.8', 9) == '2.8000 GHz'
	assert cpuinfo._hz_short_to_friendly('1.2', 6) == '1.2000 MHz'
	assert cpuinfo._hz_short_to_friendly('3.2', 9) == '3.2000 GHz'
	assert cpuinfo._hz_short_to_friendly('1.3', 0) == '1.3000 Hz'
	assert cpuinfo._hz_short_to_friendly('0.0', 0) == '0.0000 Hz'

	assert cpuinfo._hz_short_to_friendly('invalid', 0) == '0.0000 Hz'
	assert cpuinfo._hz_short_to_friendly('8.778.9', 0) == '0.0000 Hz'
	assert cpuinfo._hz_short_to_friendly('', 0) == '0.0000 Hz'
	assert cpuinfo._hz_short_to_friendly(None, 0) == '0.0000 Hz'


def test_parse_cpu_brand_string():
	hz, scale = cpuinfo._parse_cpu_brand_string('Intel(R) Pentium(R) CPU G640 @ 2.80GHz')
	assert (hz, scale) == ('2.8', 9)

	hz, scale = cpuinfo._parse_cpu_brand_string('Intel(R) Pentium(R) CPU @ 1.20MHz')
	assert (hz, scale) == ('1.2', 6)

	# NOTE: No @ symbol
	hz, scale = cpuinfo._parse_cpu_brand_string('Intel(R) Pentium(R) D CPU 3.20GHz')
	assert (hz, scale) == ('3.2', 9)

	# NOTE: No @ symbol and no Hz
	hz, scale = cpuinfo._parse_cpu_brand_string('AMD Ryzen 7 2700X Eight-Core Processor')
	assert (hz, scale) == ('0.0', 0)


def test_parse_cpu_brand_string_dx():
	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"Intel(R) Pentium(R) CPU G640 @ 2.80GHz (fam: 06, model: 2a, stepping: 07)"
	)
	assert brand == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert (hz, scale) == ('2.8', 9)
	assert (vendor_id, stepping, model, family) == (None, 7, 42, 6)

	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"Intel(R) Pentium(R) CPU G640 @ 2.80GHz (family: 0x6, model: 0x2a, stepping: 0x7)"
	)
	assert brand == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert (hz, scale) == ('2.8', 9)
	assert (vendor_id, stepping, model, family) == (None, 7, 42, 6)

	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz"
	)
	assert brand == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert (hz, scale) == ('2.93', 9)
	assert (vendor_id, stepping, model, family) == (None, None, None, None)

	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"Intel(R) Pentium(R) CPU G640 @ 2.80GHz (2793.73-MHz K8-class CPU)"
	)
	assert brand == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert (hz, scale) == ('2.8', 9)
	assert (vendor_id, stepping, model, family) == (None, None, None, None)

	# NOTE: No @ symbol
	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"Intel(R) Pentium(R) D CPU 3.20GHz"
	)
	assert brand == 'Intel(R) Pentium(R) D CPU 3.20GHz'
	assert (hz, scale) == ('3.2', 9)
	assert (vendor_id, stepping, model, family) == (None, None, None, None)

	# NOTE: No @ symbol and no Hz
	hz, scale, brand, vendor_id, stepping, model, family = cpuinfo._parse_cpu_brand_string_dx(
		"AMD Ryzen 7 2700X Eight-Core Processor          (3693.15-MHz K8-class CPU) (fam: 06, model: 2a, stepping: 07)"
	)
	assert brand == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert (hz, scale) == ('3693.15', 6)
	assert (vendor_id, stepping, model, family) == (None, 7, 42, 6)
