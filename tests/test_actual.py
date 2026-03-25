from cpuinfo import cpuinfo
from tests import helpers


def test_all():
	os_type = helpers.get_os_type()

	if os_type == 'BeOS':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert len(cpuinfo._get_cpu_info_from_sysinfo()) > 0
		# self.assertTrue(len(cpuinfo._get_cpu_info_from_cpuid()) > 0)
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'BSD':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert len(cpuinfo._get_cpu_info_from_dmesg()) > 0
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# FIXME: This fails by segfaulting for some reason
		# self.assertEqual({}, cpuinfo._get_cpu_info_from_cpuid())
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'Cygwin':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) > 0
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# FIXME: This fails by segfaulting for some reason
		# self.assertEqual({}, cpuinfo._get_cpu_info_from_cpuid())
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'MacOS':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
		assert len(cpuinfo._get_cpu_info_from_sysctl()) > 0
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# FIXME: This fails by segfaulting for some reason
		# self.assertEqual({}, cpuinfo._get_cpu_info_from_cpuid())
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'Linux':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		# self.assertTrue(len(cpuinfo._get_cpu_info_from_lscpu()) > 0)
		assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) > 0
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# self.assertTrue(len(cpuinfo._get_cpu_info_from_cpuid()) > 0)
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'Solaris':
		assert cpuinfo._get_cpu_info_from_registry() == {}
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert len(cpuinfo._get_cpu_info_from_kstat()) > 0
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# FIXME: This fails by segfaulting for some reason
		# self.assertEqual({}, cpuinfo._get_cpu_info_from_cpuid())
		assert len(cpuinfo.get_cpu_info()) > 0
	elif os_type == 'Windows':
		assert len(cpuinfo._get_cpu_info_from_registry()) > 0
		assert cpuinfo._get_cpu_info_from_cpufreq_info() == {}
		assert cpuinfo._get_cpu_info_from_lscpu() == {}
		assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
		assert cpuinfo._get_cpu_info_from_sysctl() == {}
		assert cpuinfo._get_cpu_info_from_kstat() == {}
		assert cpuinfo._get_cpu_info_from_dmesg() == {}
		assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
		assert cpuinfo._get_cpu_info_from_sysinfo() == {}
		# self.assertTrue(len(cpuinfo._get_cpu_info_from_cpuid()) > 0)
		assert len(cpuinfo.get_cpu_info()) > 0
	else:
		raise AssertionError('Unexpected OS type "{0}".'.format(os_type))
