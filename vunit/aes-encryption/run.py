#!/usr/bin/env python3

import os
import sys
import string
# Importing main vunit library
from vunit import VUnit

# Add additional module
import rand_enc
from rand_enc import prepare_data

#os.environ['VUNIT_SIMULATOR'] = 'rivierapro'
#os.environ['VUNIT_RIVIERAPRO_PATH'] = '/edatools/Aldec/Riviera-PRO-2024.04-x64/bin'

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

rand_data_test = 3

# Invoke a function to prepare randomized data test cases
# Provide another argument to make different number of test cases
data_list = rand_enc.prepare_data(rand_data_test)

encryption_tests_data = [
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
        )
    ]

# Ask for contribution tests or all tests
CONTRIBUTION='0'
if "CONTRIBUTION" in os.environ:
	CONTRIBUTION=os.environ["CONTRIBUTION"]
	
if CONTRIBUTION=='1':
    print("Following contribution tests will be conducted:")
    test_list = []
    with open("contribution.txt", "r") as f:
        for x in f:
            print(x)
            # Read contribution.txt file and add tests to the list
            test_list.append(x.strip())
    
    
    
    # Tests lists declaration
    encryption_tests_list = ['aes_specification', 'zero_inputs', "cryptographic_standard_doc", "one_two_three", "test_vector_1", "test_vector_2" ]
    random_encryption_tests_list = [f"random_test_number_{x}" for x in range(rand_data_test)]
    
    # If x is one of the tests declared in contribution.txt, a specific test case will be conducted
    for x in test_list:
        if x=='hardcoded encryption test':
            tb = lib.test_bench("tb_enc_hardcoded")
            test = tb.test("hardcoded encryption test")
        elif x in encryption_tests_list:
            tb = lib.test_bench("tb_enc_generics")
            test = tb.test("generic encryption test")
            
            generic_encryption_test_data = [k for k in encryption_tests_data if k[0]==x][0]
            
            test.add_config(
                name=generic_encryption_test_data[0],
                generics=dict(key=generic_encryption_test_data[1], plaintext=generic_encryption_test_data[2], expected_ciphertext=generic_encryption_test_data[3]),
            )
        elif x in random_encryption_tests_list:
            tb = lib.test_bench("tb_enc_generics")
            test = tb.test("random generic encryption test")
            
            for k in data_list:
                if k[0]==x:
                    random_generic_encryption_test_data = k
                    break
            
            test.add_config(
                name=random_generic_encryption_test_data[0],
                generics=dict(key=random_generic_encryption_test_data[1], plaintext=random_generic_encryption_test_data[2], expected_ciphertext=random_generic_encryption_test_data[3]),
            )

# Run all tests      
else:
    # Hardcoded test
    tb = lib.test_bench("tb_enc_hardcoded")
    test = tb.test("hardcoded encryption test")

    # Create configuration of the encryption test using golden references from different sources
    tb = lib.test_bench("tb_enc_generics")
    test = tb.test("generic encryption test")

    for source, key, plaintext, ciphertext in encryption_tests_data:
        test.add_config(
            name=source,
            generics=dict(key=key, plaintext=plaintext, expected_ciphertext=ciphertext),
        )

    # Create configuration of the encryption test using random input vectors
    tb = lib.test_bench("tb_enc_generics")
    test = tb.test("random generic encryption test")

    for source, key, plaintext, ciphertext in data_list:
        test.add_config(
            name=source,
            generics=dict(key=key, plaintext=plaintext, expected_ciphertext=ciphertext),
        )

lib.set_sim_option("enable_coverage", True)

lib.set_compile_option("rivierapro.vcom_flags", ["-coverage","sb"])
lib.set_sim_option("rivierapro.vsim_flags", ["-acdb_cov sbaecmtf"])

# Run vunit main function
vu.main()
