#!/usr/bin/env python3

# Importing main vunit library
from vunit import VUnit

# Add additional module
import rand_enc
from rand_enc import prepare_data

# Create VUnit instance by parsing command line arguments
vu = VUnit.from_argv()

# Optionally add VUnit's builtin HDL utilities for checking, logging, communication...
# See http://vunit.github.io/hdl_libraries.html.
vu.add_vhdl_builtins()

# Create library 'lib'
lib = vu.add_library("lib")

# Add all files ending in .vhd in src directory to library
lib.add_source_files("src/*.vhd")

# Add all files ending in .vhd in tb directory to library
lib.add_source_files("tb/*.vhd")

# Hardcoded test
tb = lib.test_bench("tb_enc_hardcoded")
test = tb.test("hardcoded encryption test")

# Create configuration of the encryption test using golden references from different sources
tb = lib.test_bench("tb_enc_generics")
test = tb.test("generic encryption test")

for source, key, plaintext, ciphertext in [
    (
        "aes_specification",
        'x"3c4fcf098815f7aba6d2ae2816157e2b"',
        'x"340737e0a29831318d305a88a8f64332"',
        'x"320b6a19978511dcfb09dc021d842539"',
    ),
    (
        "zero_inputs",
        'x"00000000000000000000000000000000"',
        'x"00000000000000000000000000000000"',
        'x"2e2b34ca59fa4c883b2c8aefd44be966"',
    ),
    (
        "cryptographic_standard_doc",
        'x"3c4fcf098815f7aba6d2ae2816157e2b"',
        'x"2a179373117e3de9969f402ee2bec16b"',
        'x"97ef6624f3ca9ea860367a0db47bd73a"',
    ),
    (
        "one_two_three",
        'x"32211332211332211332211332211332"',
        'x"12233112233112233112233112233112"',
        'x"4fdfcdf5481f204df7dc282d8f645119"',
    ),
    (
        "test_vector_1",
        'x"f74eb5c67f8ead89ce6fb4edac7b8392"',
        'x"320b8d7f6e2bcfad36d8bc8529837ead"',
        'x"6dc7fe4482c891d38faf915cbed856bf"',
    ),
    (
        "test_vector_2",
        'x"74c0563e4daa164875eda570cf29bb46"',
        'x"12d72ab5ad3f0972fd7e93cf9a8d6eb3"',
        'x"1eacbe7973a224fffba1f8cf42d77f99"',
    ),
]:
    test.add_config(
        name=source,
        generics=dict(key=key, plaintext=plaintext, expected_ciphertext=ciphertext),
    )

# Create configuration of the encryption test using random input vectors
tb = lib.test_bench("tb_enc_generics")
test = tb.test("random generic encryption test")

# Invoke a function to prepare randomized data test cases
# Provide another argument to make different number of test cases
data_list = rand_enc.prepare_data(20)

for source, key, plaintext, ciphertext in data_list:
    test.add_config(
        name=source,
        generics=dict(key=key, plaintext=plaintext, expected_ciphertext=ciphertext),
    )

#Enable design profiler for Aldec's simulators
#lib.set_sim_option("enable_profiler", True)

# Run vunit main function
vu.main()
