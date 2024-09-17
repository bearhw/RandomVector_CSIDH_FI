#Fault injection attack on CSIDH

This codebase implements a real-then-dummy and dynamic random vector CSIDH, and provide the fault injection python scripts, including extract optimal fault injection parameters, and recover CSIDH private key.

This repository is the source code for the paper ``Practical Fault Injection Attacks on Constant Time CSIDH and Mitigation Techniques" Tinghung Chiu, Jason LeGrow, and  Wenjie Xiong, ASHES 2024.

##Background

Commutative Supersingular Isogeny Diffie-Hellman (CSIDH) is an isogeny-based key exchange protocol.To secure CSIDH against side-channel attacks, constant-time implementations with additional dummy isogeny computations are employed.

In our paper, we mentioned two types of constant time CSIDH, real-then-dummy and dynamic random vector.

The concept of real-then-dummy CSIDH involves adding dummy isogeny operations to ensure that each degree of isogeny operation is performed the same number of times. Specifically, each computation processes a real isogeny operation first, followed by a dummy isogeny operation. This approach helps prevent side-channel attacks, which could otherwise potentially recover the private key.

The conecpt of dynamic random vector CSIDH is using the random vector to control the order of real and dummy isogeny operation. This make the attacker cannot recover the private key with binary search.The concept of dynamic random vector constant-time CSIDH is based on the paper "(Short Paper) Analysis of a Strong Fault Attack on Static/Ephemeral CSIDH"(https://link.springer.com/chapter/10.1007/978-3-030-85987-9_12).

###How to do the fault injection attack on constant time CSIDH?

For real-then-dummy CSIDH, the order of real and dummy isogeny operation of each degree is same. Moreover, the number of real isogeny operation is decided by private key value, e.g. if the max value of degree-359 is 5 and private key value of it is 3, then the order of isogeny operation will be real-real-real-dummy-dummy. 
Obviously, we can use the binary search to locate the last real isogeny operation to recover the private key value.

For the dynamic random vector, the order of real and dummy isogeny operations for each degree is controlled by a random vector. Moreover, the ratio of real to dummy isogenies is related to the private key value. For example, if the maximum value for degree-359 is 5 and the private key value for it is 3, the ratio of real to dummy isogenies will be 1.5. An attacker can process a number of fault injection attacks to determine this ratio and potentially recover the private key.

## CSIDH Implementation
In our paper, we evluated two types of constant-time CSIDH, real-then-dummy and dynamic random vector, and processed fault injeciton attack on both types. For fault injection tests, we use code of real-then-dummy CSIDH in [csidhfi repository](https://github.com/csidhfi/csidhfi).

For dynamic random vector CSIDH (i.e., the code in CSIDH/code/random-vector_csidh), we use randomVector function to process dynamic random vector CSIDH, and remain CSIDH part is also based on [csidhfi repository](https://github.com/csidhfi/csidhfi). 


To execute dynamic random vector CSIDH
```
    cd CSIDH/code/random-vector_csidh
    make
    ./test
```

## Reproducing Paper Results
In our paper, we shows some result with figures.
Figure 1 and 2 are the result with processing "1-fault_injection_position.py" that the attack can use to extract optimal fault injection time.

Table 2-4 are the result with processing "3-injection_time-353.py" and "3-injection_time-359.py". This python script will output the result of fault injection attack during degree-353/359 isogeny with choosen parameter.

Table 5 is the result with processing "4-binary_search_recover_key.py", which is the result of recover private key of real-then-dummy CSIDH.

Table 6 is the result with processing "5-recover_key_of_random_vector.py", which is the result of recover private key of dynamic random vector CSIDH.

##License
The code is released under GNU GPL v3.

##Citation
```
@inproceedings{chiu2024practical,
  title={Practical Fault Injection Attacks on Constant Time CSIDH and Mitigation Techniques},
  author={Chiu, Tinghung and LeGrow, Jason and Xiong, Wenjie},
  booktitle={Proceedings of the 2024 Workshop on Attacks and Solutions in Hardware Security},
  year={2024}
}
```
##Disclaimer

This open source project is for proof of concept purposes only and should not be used in production environments. The code has not been officially vetted for security vulnerabilities and provides no guarantees of correctness or security. Users should carefully review the code and conduct their own security assessments before using the software.
