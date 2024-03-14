## 🪄 magick-py

<br>
<br>

* **cli for single server PIR and LWE experiments in python, based on [*"simple and fast single-server private information retrieval"*,  by a. henzinger et al.](https://eprint.iacr.org/2022/949.pdf)**
* **to learn more, check my [mirror write-up about this project](https://mirror.xyz/Mia Stein.eth/4G5bsqUkjLxhQ0M9so3f25o4cABwN--tC40N3jkReug).**

<br> 


----

### theoretical background

<br>

#### what’s PIR

private information retrieval refers to the **ability to query a database without revealing which item is looked up or whether it exists**, by using cryptographic primitives. [b. chor et al.](https://www.wisdom.weizmann.ac.il/~oded/p_pir.html) first introduced the concept in 1995.

PIR schemes are generally divided into **single-server schemes** and **multiple-server schemes** (which allows you to remove the trust from a subset of the servers).

in this research, we will look at simple single-server PIR protocol setups, where a server holds an embedded database `D` represented by a `n x n` square matrix (whose elements are under a constant modulo), and a client wants to privately read the `ith` database item (`Di`, with `n` elements) without letting the server learn about `i`.

<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-science-py/assets/1130416/129266fe-78c0-4923-ba6a-748034ae4278" width="70%" align="center"/>
</p>



<br>


<br>

#### homomorphic encryption schemes

suppose a server that can `XOR` client’s data. the client would send their cipher `c0`, obtained from their plaintext data `m0` and their key `k0`:

```
c = m0 ⌖ k0
```

**homomorphism** is the property that if a client sends two encrypted messages, `c1` and `c2` (from messages `m0` and `m1`, respectively), the server can return `c1 ⌖ c2` so the client can retrieve `m0 ⌖ m1`.

**additive homomorphism** occurs when, given two ciphertexts `(a0, c0)` and `(a1, c1)`, their sum `(a0 + a1, c0 + c1)` decrypts to the sum of the plaintexts (provided that the error remains sufficiently small).

**partially homomorphic encryption** can be easily achieved as it accepts the possibility that not all data is encrypted (or homomorphic) through other operations (such as multiplication). 

**fully homomorphic encryption (FWE)**, which is much harder to achieve, would occur if a server operated on encrypted data **without seeing ANY of its content.**

<br>

> 💡 *in a more formal definition, **homomorphic encryption** is a form of encryption with evaluation capability for computing over encrypted data without access to the secret key, i.e., supporting arbitrary computation on ciphers. **fully homomorphic encryption** could be said to be the evaluation of arbitrary circuits of multiple types of (unbounded depth) gates (relevant to zero-knowledge proof setups). also, check out [vitalik's post on the subject](https://vitalik.eth.limo/general/2020/07/20/homomorphic.html).*

<br>

#### learning with errors (LWE)

PIR is also a subset of the broad topic of **lattice-based cryptography**. it refers to a series of **quantum-resistant cryptographic primitives** involving lattices, either in their construction or in the security proof.

<br>

> 💡 *over an n-dimensional vector space, a lattice is an infinite set of points represented by a collection of vectors.*

<br>

in a [2005 seminal PIR paper](https://dl.acm.org/doi/10.1145/1060590.1060603), oded regev introduced the **first lattice-based public-key encryption scheme** and the **learning with errors (LWE) problem**. 

the LWE problem relies on the **hardness of distinguishing between a message with added noise and a random sample**. it can be thought of as **a search in a (noisy) modular set of equations whose solutions can be very difficult to solve**. in other words, given `m` samples of coefficients `(bi, ai)` in the linear equation `bi = <ai, s> + ei`, with the error `ei` sampled from a small range `[-bound, bound]`, finding the secret key `s` is "hard". 

note, however, that LWE-based encryption schemes have a **significant drawback due to noise growth**. as the ciphertexts produced by these schemes are noisy encodings of the plaintext, **homomorphic operations between ciphertexts increase the magnitude of the noise**. if the noise exceeds a certain threshold, the correctness of the decryption may no longer hold. despite this problem, **regev encryption** can be very efficient for PIR as it is additively homomorphic.

in the past decades, regev's security proof and the LWE scheme's efficiency have been the subject of intense research among cryptographers, including [craig gentry's thesis (2009)](https://crypto.stanford.edu/craig/craig-thesis.pdf), on the **first fully homomorphic encryption scheme**.


<br>

#### a simple implementation of the PIR protocol

a PIR protocol aims to design **schemes that satisfy privacy and correctness constraints while achieving the minimum possible download cost**. 

<br>

> 💡 *the **download cost** of a PIR scheme is defined as **the total number of bits downloaded by the user from all the databases, normalized by the message size**. the **PIR rate** is defined as **the reciprocal of the PIR download cost**.*

<br>

one possible implementation approach is to choose a suitable polynomial and then have a single server preprocess the data. this preprocessing depends only on the database `D` and the public parameters of the regev encryption scheme, so that the server can reuse the work across many queries from many independent clients.

after the preprocessing step, to answer a client's query, the server must compute only roughly `N 32-bit` integer multiplications and additions on a database of `N bytes`. the catch is that the client must download a *hint* matrix about the database contents after this preprocessing.

therefore, a simple serve PIR scheme would comprise two phases:

* **the offline phase**, with pre-computations and the exchange of *hints*, and

* **the online phase**, with the query processing on the server and response decoding on the client.

the practicality of PIR-based applications is primarily impacted by the query processing time and the hint exchange phase. the theoretical query size grows as the square root of the number of field elements representing the database. for example, the largest query size for a database of `32 GB` is around `600 KB`.


<br>

#### possible applications of PIR

once PIR becomes less expensive or prohibitive (*i.e.*, cheaper computation with a small cipher, as PIR inherently has a high cost for server-side computation), these are some of the possible applications that could utilize the protocol:

- **searching IP databases**: when filing a new IP, the author must search the IP database to check that no previous entry significantly overlaps with their invention. PIR could allow the search to be performed without leaving search terms on the query log of the IP database.

- **real-time asset quotes**: investors interested in a particular asset often monitor the market to determine when to purchase. PIR could allow their interest to be confidential.

- **safe browsing and private oracles, checking passwords over breached databases (or any type of credentials), certificate transparency (CT) checks, certificate revocation checks,** among many others.

<br>

#### why PIR is still not feasible

although modern PIR schemes require surprisingly little communication and the protocol works well enough at smaller scales, the time needed to scan it grows proportionally as the database grows. for bigger databases, the process becomes prohibitively inefficient (fetching a database record grows only polylogarithmically with the number of records, `N`).

after preprocessing the database, the server can answer a query in time sublinear in `N`. thus, the current hard limit on the throughput of PIR schemes is the ratio between the database size and the server time to answer a query (the speed with which the PIR server can read the database from memory).

finally, it's important to note that PIR protocols do not ensure data integrity or authentication. an authenticated PIR scheme could combine an unauthenticated multi-server PIR scheme with a standard integrity-protection mechanism, such as merkle trees.

in this approach, PIR servers download the data from the blockchain to construct PIR databases. dor each database, the PIR server creates a description file (usually called a *manifest file*). the user collects all available block headers and fetches the manifest files from the PIR servers to query the PIR database later efficiently.

<br>

---

### ["simple and fast single-server private information retrieval", by alexandra henzinger et. al (2022)](https://eprint.iacr.org/2022/949) 

<br>

* this paper introduces a design for **SimplePIR**, **the fastest single-server PIR scheme known to date**.

* the security holds under a **Learning with Errors scheme** that requires no polynomial arithmetic or fast fourier transforms. regev encryption gives a secret-key encryption scheme that is secure under the LWE assumption.

* to answer a client’s query, the server performs fewer than **one 32-bit multiplication** and **one 32-bit addition** per **database byte**, achieving **10 GB/s/core server throughput**.

* the first approach to **query a 1 GB database** demands the client to first download a **121 MB "hint" about the database contents**. then, the client can make any number of queries, each requiring **242 KB of communication**.

* the second approach **shrinks the hint to 16 MB**. then, following queries demand **345 KB of communication**.

* finally, the scheme is applied, together with a novel data structure for approximate set membership, to **private auditing in certificate transparency**. the results can be compared to google chrome’s current approach, with **16 MB of downloads per month, and 150 bytes per TLS connection**.


<br>

#### a server and a query in simplePIR


in our code, the single-server database is represented by a square matrix `(m x m)`, while a query is a vector filled by `0s` except at the asking row and column `(m x 1)`. any result should have the same dimension as the query vector (*i.e.*, the space is reduced to the size of the column where the data is located).

the server retrieves the queried item by:

1. looping over every column and multiplying their values to the value in the same row of the query vector, and
2. adding the values found in each column in its own matrix.

a secret key regev encryption scheme using sampled errors to reproduce LWE is then built on top of the ideas above. privacy is guaranteed by checking that fully homomorphic encryption is held with respect to addition in this setup (*i.e.*, additive homomorphism).




<br>


----

### installation

<br>

#### requirements

```
python3 -m venv venv
source ./venv/bin/activate
make install_deps
```


#### set a `.env` file


add config and LWE parameters to:

```
cp .env.example .env
vim .env
```

LWE parameters needed are:


* size of msg vector, `m` and `n`
* message’s modulo `mod` and `p`
* a work around the sampling errors (*i.e.*, the standard variation sigma of a Gaussian distribution with zero mean sigma) by setting a bound range for them


to pick adequate parameters, you can use tools such as a [lattice estimator](https://github.com/malb/lattice-estimator).


#### install 

```
make install
```


#### test your installation

```
magick

usage: magick [-h] [-e] [-s] [-a] [-i] [-t] [-p]

✨ Magick ✨

options:
  -h, --help  show this help message and exit
  -e          Run simple linear key Regev encryption experiment with sampled error. Example: magick -e
  -s          Run simple linear key Regev encryption experiment with scaled msg. Example: magick -s
  -a          Prove that the Regev scheme is additive homomorphic. Example: magick -s
  -i          Prove that the Regev scheme supports plaintext inner product. Example: magick -i
  -t          Run a very simple PIR explanation (without encryption). Example: magick -t
  -p          Run a secret key Regev PIR experiment. Example: magick -p
```


<br>

----

### experiments

<br>



#### simple linear encryption and decryption of a msg vector with a sampled error vector

in this simple experiment of learning with error (LWE), we operate our message vector over a ring modulo `mod`, so some information is lost. 

luckily, gaussian elimination can still be used to recover the original message vector as it works over a ring modulo `mod`.

the steps of this experiment are the following:

1. represent a message vector `m0` of size `m`, where each element has modulo `mod`.
2. encrypt this message with a simple `B = A * s + e + m0`, where `s` is the secret and `e` is the error vector.
3. set the ciphertext as the tuple `c = (B, A)`
4. decrypt `c = (B, A)` for a given `s`, such that `m1 = m0 + e`.

<br>

```
magick -e

✨ Original msg was successfully retrieved!

✨ m0: 
Rows: 200
Cols: 1
Vector: [220, 1105, 88, 1970, 490, 557, 86, 1882, 502, 1339, 148, 1851, 121, 348, 1187, 891, 1997, 1058, 1602, 1438, 211, 374, 254, 156, 1151, 356, 1587, 762, 1961, 1565, 233, 404, 1002, 337, 1380, 481, 1850, 1059, 366, 185, 321, 1548, 1351, 236, 205, 742, 483, 695, 1979, 1590, 1768, 143, 107, 1774, 324, 433, 733, 863, 1729, 1737, 423, 1663, 488, 2, 318, 88, 1961, 523, 315, 810, 127, 138, 295, 1573, 1179, 258, 758, 645, 1300, 211, 85, 592, 277, 1395, 1989, 1127, 1793, 1923, 866, 513, 713, 848, 834, 759, 411, 1609, 845, 1858, 368, 1696, 1504, 1136, 220, 1495, 1100, 1251, 312, 261, 952, 1302, 345, 526, 1203, 1339, 730, 424, 1687, 781, 369, 1219, 841, 470, 1391, 580, 830, 1395, 232, 1058, 199, 1062, 1805, 1818, 749, 540, 64, 1861, 1959, 1760, 1244, 602, 543, 1837, 1154, 1095, 801, 53, 1548, 493, 1903, 67, 1159, 1409, 809, 1301, 1689, 310, 1747, 1692, 1498, 1240, 1900, 1398, 960, 628, 1240, 1803, 1104, 954, 1945, 668, 1729, 1675, 1507, 1213, 1412, 143, 1533, 186, 1577, 1926, 1592, 922, 31, 774, 788, 730, 1886, 1802, 1998, 404, 70, 530, 1012, 1800, 836, 1862, 1257, 788, 84, 1145]


✨ m0 + e: 
Rows: 200
Cols: 1
Vector: [220, 1105, 88, 1970, 490, 557, 86, 1882, 502, 1339, 148, 1851, 121, 348, 1187, 891, 1997, 1058, 1602, 1438, 211, 374, 254, 156, 1151, 356, 1587, 762, 1961, 1565, 233, 404, 1002, 337, 1380, 481, 1850, 1059, 366, 185, 321, 1548, 1351, 236, 205, 742, 483, 695, 1979, 1590, 1768, 143, 107, 1774, 324, 433, 733, 863, 1729, 1737, 423, 1663, 488, 2, 318, 88, 1961, 523, 315, 810, 127, 138, 295, 1573, 1179, 258, 758, 645, 1300, 211, 85, 592, 277, 1395, 1989, 1127, 1793, 1923, 866, 513, 713, 848, 834, 759, 411, 1609, 845, 1858, 368, 1696, 1504, 1136, 220, 1495, 1100, 1251, 312, 261, 952, 1302, 345, 526, 1203, 1339, 730, 424, 1687, 781, 369, 1219, 841, 470, 1391, 580, 830, 1395, 232, 1058, 199, 1062, 1805, 1818, 749, 540, 64, 1861, 1959, 1760, 1244, 602, 543, 1837, 1154, 1095, 801, 53, 1548, 493, 1903, 67, 1159, 1409, 809, 1301, 1689, 310, 1747, 1692, 1498, 1240, 1900, 1398, 960, 628, 1240, 1803, 1104, 954, 1945, 668, 1729, 1675, 1507, 1213, 1412, 143, 1533, 186, 1577, 1926, 1592, 922, 31, 774, 788, 730, 1886, 1802, 1998, 404, 70, 530, 1012, 1800, 836, 1862, 1257, 788, 84, 1145]


✨ Parameters: 
mod: 2000 
n: 20 
m: 200 
p: 100 
bound: [-4, 4] 
```

<br>

----

#### secret key Regev encryption by scaling a message vector


in this simple example of learning with error (LWE), we lose information on the least significant bits by adding noise, *i.e.*, by scaling the message vector by `delta = mod / p` before adding it to encryption. then, during the decryption, we scale the message vector back by `1 / delta`. 

the scaling ensures that `m` is in the highest bits of the message vector, without losing information by adding the error vector `e`.

consequently, the message `m0` vector has each element module `p` (not `mod`), where `p < q`. The scaled message is now `m0_scaled = m0 * delta = m0 * mod / p`. 

the cipertext `c` is `B = A * s + e + m0_scaled`, which can be decrypted as `c = (B, A)`, *i.e.*, `m0 = (B - A * s) / delta = (delta * m0 + e) / delta`.


<br>  


```
magick -s

✨ Original msg was successfully retrieved!

✨ m0: 
Rows: 200
Cols: 1
Vector: [8, 20, 42, 88, 2, 73, 83, 94, 22, 28, 82, 89, 93, 6, 15, 69, 17, 10, 39, 13, 39, 16, 27, 89, 68, 18, 3, 29, 92, 5, 69, 51, 94, 68, 14, 72, 43, 36, 49, 91, 3, 96, 6, 4, 69, 26, 6, 95, 10, 37, 3, 30, 60, 40, 67, 45, 75, 20, 5, 70, 57, 66, 75, 19, 90, 80, 24, 26, 39, 36, 0, 86, 33, 79, 2, 6, 5, 39, 4, 74, 31, 52, 77, 57, 34, 55, 2, 33, 50, 66, 32, 75, 35, 26, 65, 89, 12, 52, 42, 81, 56, 35, 20, 51, 76, 16, 12, 77, 78, 29, 77, 4, 72, 30, 68, 0, 52, 50, 95, 2, 4, 46, 16, 98, 97, 6, 65, 69, 77, 88, 23, 60, 98, 87, 75, 1, 90, 25, 83, 38, 23, 89, 92, 25, 45, 76, 90, 52, 86, 2, 61, 50, 66, 60, 67, 7, 56, 35, 96, 85, 66, 45, 22, 16, 14, 22, 89, 42, 83, 65, 39, 2, 98, 37, 30, 3, 54, 78, 7, 86, 96, 77, 27, 80, 48, 92, 78, 43, 59, 78, 15, 60, 88, 17, 1, 78, 35, 38, 89, 67]


✨ scaled m1: 
Rows: 200
Cols: 1
Vector: [8, 20, 42, 88, 2, 73, 83, 94, 22, 28, 82, 89, 93, 6, 15, 69, 17, 10, 39, 13, 39, 16, 27, 89, 68, 18, 3, 29, 92, 5, 69, 51, 94, 68, 14, 72, 43, 36, 49, 91, 3, 96, 6, 4, 69, 26, 6, 95, 10, 37, 3, 30, 60, 40, 67, 45, 75, 20, 5, 70, 57, 66, 75, 19, 90, 80, 24, 26, 39, 36, 0, 86, 33, 79, 2, 6, 5, 39, 4, 74, 31, 52, 77, 57, 34, 55, 2, 33, 50, 66, 32, 75, 35, 26, 65, 89, 12, 52, 42, 81, 56, 35, 20, 51, 76, 16, 12, 77, 78, 29, 77, 4, 72, 30, 68, 0, 52, 50, 95, 2, 4, 46, 16, 98, 97, 6, 65, 69, 77, 88, 23, 60, 98, 87, 75, 1, 90, 25, 83, 38, 23, 89, 92, 25, 45, 76, 90, 52, 86, 2, 61, 50, 66, 60, 67, 7, 56, 35, 96, 85, 66, 45, 22, 16, 14, 22, 89, 42, 83, 65, 39, 2, 98, 37, 30, 3, 54, 78, 7, 86, 96, 77, 27, 80, 48, 92, 78, 43, 59, 78, 15, 60, 88, 17, 1, 78, 35, 38, 89, 67]


✨ Parameters: 
mod: 2000 
n: 20 
m: 200 
p: 100 
bound: [-4, 4] 
```


<br>

----

#### proving that the secret key Regev encryption scheme supports additive homomorphism

additive homomorphism means that if `c0` is the encryption of `m1` under secret key `s` and `c2` is the encryption of `m2` under the same secret key `s`, then `c0 + c1` is the encryption of `m0 + m1` under `s`.

for a large number of `ci`, noise can be introduced from error, so the correctness of the results will depend on the values of `m, n, mod, and p`, such that
`|sum ei| < mod/(2p)`.


```
magick -a

✨ Original msg was successfully retrieved!

✨ m0 + m1: 
Rows: 200
Cols: 1
Vector: [77, 84, 63, 93, 14, 60, 79, 40, 46, 89, 58, 3, 18, 51, 39, 85, 58, 35, 52, 19, 84, 70, 65, 76, 74, 27, 33, 53, 12, 59, 65, 18, 12, 2, 36, 10, 21, 59, 93, 8, 71, 25, 15, 27, 55, 82, 46, 85, 66, 35, 48, 33, 48, 50, 0, 37, 52, 62, 85, 99, 31, 80, 25, 96, 42, 78, 45, 14, 95, 24, 19, 70, 7, 73, 37, 76, 99, 13, 28, 14, 32, 28, 82, 46, 99, 31, 90, 94, 56, 19, 17, 83, 85, 17, 37, 33, 35, 72, 5, 42, 79, 77, 76, 25, 1, 40, 46, 38, 94, 35, 69, 55, 38, 66, 94, 87, 21, 6, 92, 10, 69, 76, 44, 95, 36, 29, 92, 35, 10, 5, 79, 6, 9, 31, 47, 30, 87, 77, 69, 80, 26, 72, 30, 90, 63, 63, 5, 27, 29, 63, 1, 60, 34, 55, 16, 57, 1, 45, 81, 78, 96, 60, 40, 95, 93, 56, 67, 79, 51, 52, 85, 20, 68, 61, 72, 52, 36, 2, 10, 83, 21, 6, 27, 21, 95, 14, 39, 75, 50, 43, 58, 51, 46, 2, 28, 63, 16, 11, 75, 52]


✨ m2: 
Rows: 200
Cols: 1
Vector: [77, 84, 63, 93, 14, 60, 79, 40, 46, 89, 58, 3, 18, 51, 39, 85, 58, 35, 52, 19, 84, 70, 65, 76, 74, 27, 33, 53, 12, 59, 65, 18, 12, 2, 36, 10, 21, 59, 93, 8, 71, 25, 15, 27, 55, 82, 46, 85, 66, 35, 48, 33, 48, 50, 0, 37, 52, 62, 85, 99, 31, 80, 25, 96, 42, 78, 45, 14, 95, 24, 19, 70, 7, 73, 37, 76, 99, 13, 28, 14, 32, 28, 82, 46, 99, 31, 90, 94, 56, 19, 17, 83, 85, 17, 37, 33, 35, 72, 5, 42, 79, 77, 76, 25, 1, 40, 46, 38, 94, 35, 69, 55, 38, 66, 94, 87, 21, 6, 92, 10, 69, 76, 44, 95, 36, 29, 92, 35, 10, 5, 79, 6, 9, 31, 47, 30, 87, 77, 69, 80, 26, 72, 30, 90, 63, 63, 5, 27, 29, 63, 1, 60, 34, 55, 16, 57, 1, 45, 81, 78, 96, 60, 40, 95, 93, 56, 67, 79, 51, 52, 85, 20, 68, 61, 72, 52, 36, 2, 10, 83, 21, 6, 27, 21, 95, 14, 39, 75, 50, 43, 58, 51, 46, 2, 28, 63, 16, 11, 75, 52]


✨ Parameters: 
mod: 2000 
n: 20 
m: 200 
p: 100 
bound: [-4, 4] 
```


<br>

----

#### proving that the secret key Regev encryption scheme supports plaintext inner product

this experiment shows that given a cipher `c` and a message vector `m0`, `c -> c1` can be transformed such that it also encrypts the **inner product** of `m0` with a plaintext vector `k` of size `m` and element modulo `p`.

because of **noise growth** with the vector `k`, fine-tuning the initial parameters is crucial for the message to be successfully retrieved. More specifically, to guarantee correct decryption, the following must hold:

```
k * e0 < mod / (2 * p)
```

here is an example of a successful decryption:

```
magick -i

 Original msg was successfully retrieved!

✨ scaled m1: 
Rows: 1000
Cols: 1
Vector: [5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5]


✨ scaled k * m0: 
Rows: 1000
Cols: 1
Vector: [5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5]


✨ Parameters: 
mod: 1000 
n: 100 
m: 1000 
p: 10 
bound: [-4, 4] 

✨ Correct decryption for Delta / 2: 50.0? True
✨ Noise growth: 985
```

now, changing `MOD_P` from 10 to 100, we see a failed case:

```
🚨 Original msg was not retrieved.
✨ scaled m1: 
Rows: 1000
Cols: 1
Vector: [44, 74, 56, 86, 71, 49, 95, 69, 37, 90, 90, 86, 10, 93, 71, 49, 6, 15, 10, 15, 17, 86, 10, 15, 54, 83, 47, 15, 96, 54, 25, 62, 42, 98, 47, 5, 5, 34, 93, 0, 44, 22, 47, 8, 74, 10, 47, 10, 47, 32, 30, 39, 17, 20, 83, 40, 34, 56, 93, 66, 91, 76, 10, 71, 56, 10, 42, 24, 12, 84, 78, 61, 35, 57, 44, 86, 81, 61, 12, 15, 71, 0, 18, 54, 71, 83, 15, 40, 96, 47, 98, 66, 74, 42, 71, 47, 54, 47, 10, 98, 81, 29, 83, 20, 32, 47, 95, 62, 25, 15, 47, 37, 27, 69, 8, 51, 93, 56, 15, 42, 18, 84, 76, 71, 35, 3, 98, 10, 3, 88, 59, 6, 84, 12, 59, 64, 78, 56, 15, 69, 0, 37, 27, 83, 93, 32, 10, 42, 3, 25, 15, 15, 96, 20, 79, 59, 22, 98, 34, 76, 64, 20, 84, 68, 66, 20, 56, 42, 20, 39, 95, 66, 5, 81, 98, 83, 83, 15, 93, 88, 79, 69, 12, 42, 3, 3, 84, 37, 51, 27, 15, 69, 88, 93, 15, 37, 74, 51, 13, 32, 42, 69, 69, 51, 88, 84, 27, 91, 40, 49, 0, 84, 69, 52, 27, 3, 47, 54, 15, 98, 79, 8, 46, 39, 56, 47, 56, 73, 42, 83, 20, 22, 42, 54, 15, 27, 88, 86, 32, 8, 6, 96, 37, 15, 15, 61, 42, 78, 44, 91, 32, 12, 20, 20, 0, 29, 69, 13, 27, 61, 32, 61, 20, 71, 88, 81, 98, 66, 5, 6, 42, 37, 49, 51, 84, 49, 29, 0, 62, 1, 47, 79, 66, 22, 20, 86, 5, 15, 44, 51, 22, 49, 27, 74, 18, 6, 68, 86, 78, 61, 88, 22, 15, 15, 44, 6, 69, 64, 8, 84, 69, 98, 18, 98, 98, 27, 78, 81, 86, 66, 20, 22, 42, 69, 10, 76, 10, 79, 47, 88, 88, 8, 90, 22, 74, 91, 13, 81, 79, 93, 71, 8, 29, 96, 78, 66, 64, 32, 93, 0, 12, 69, 84, 76, 81, 76, 32, 17, 93, 88, 3, 78, 54, 78, 13, 15, 71, 37, 10, 8, 88, 52, 35, 86, 83, 17, 88, 5, 18, 12, 30, 52, 44, 62, 42, 78, 83, 30, 69, 18, 42, 64, 49, 3, 64, 5, 22, 10, 54, 76, 42, 74, 90, 17, 73, 20, 52, 98, 20, 81, 84, 15, 64, 54, 61, 8, 37, 13, 83, 52, 10, 20, 64, 98, 91, 20, 24, 81, 66, 88, 47, 81, 10, 81, 24, 83, 44, 15, 25, 22, 20, 15, 61, 64, 78, 6, 42, 93, 73, 37, 86, 22, 10, 88, 42, 98, 8, 88, 37, 95, 81, 81, 0, 64, 18, 30, 13, 42, 49, 81, 8, 95, 18, 6, 59, 47, 29, 78, 27, 44, 88, 49, 10, 46, 29, 25, 35, 6, 37, 83, 66, 74, 59, 83, 56, 20, 15, 15, 62, 52, 34, 95, 10, 56, 10, 74, 74, 20, 64, 47, 71, 91, 90, 68, 12, 35, 54, 20, 15, 62, 76, 35, 20, 69, 5, 30, 25, 52, 20, 37, 62, 54, 3, 10, 96, 81, 8, 32, 27, 49, 40, 24, 83, 76, 61, 61, 84, 56, 51, 91, 79, 42, 74, 88, 47, 98, 20, 74, 54, 78, 44, 52, 71, 39, 66, 22, 46, 27, 96, 78, 61, 66, 59, 44, 88, 24, 78, 91, 83, 5, 86, 88, 22, 61, 42, 73, 10, 59, 40, 24, 20, 18, 30, 61, 78, 13, 0, 10, 59, 56, 51, 68, 52, 10, 83, 98, 32, 49, 52, 98, 61, 30, 0, 22, 8, 37, 37, 15, 96, 25, 83, 79, 0, 42, 22, 44, 15, 93, 64, 64, 76, 52, 30, 29, 93, 22, 10, 59, 54, 59, 37, 32, 27, 27, 52, 8, 22, 69, 8, 27, 57, 57, 25, 74, 37, 71, 17, 37, 32, 84, 90, 73, 20, 83, 0, 98, 74, 56, 15, 47, 18, 22, 56, 78, 34, 96, 76, 46, 49, 88, 1, 3, 66, 93, 39, 59, 69, 25, 52, 54, 30, 88, 98, 54, 42, 71, 39, 5, 98, 18, 10, 5, 54, 1, 71, 32, 5, 13, 88, 3, 98, 22, 34, 93, 76, 13, 59, 5, 95, 42, 54, 42, 3, 78, 10, 42, 30, 76, 74, 34, 49, 15, 59, 27, 49, 47, 44, 32, 74, 64, 52, 59, 69, 57, 52, 64, 51, 5, 20, 15, 1, 69, 71, 62, 35, 1, 88, 22, 69, 37, 52, 13, 66, 8, 3, 96, 93, 30, 29, 20, 81, 83, 32, 68, 15, 1, 6, 52, 32, 3, 5, 15, 37, 22, 17, 98, 42, 54, 79, 10, 88, 95, 1, 83, 8, 3, 74, 54, 96, 98, 20, 98, 27, 71, 81, 24, 32, 78, 88, 34, 30, 54, 59, 20, 39, 49, 78, 44, 6, 25, 74, 86, 76, 20, 66, 22, 88, 24, 84, 44, 68, 30, 20, 64, 27, 56, 90, 64, 37, 62, 47, 66, 8, 52, 57, 56, 5, 59, 86, 54, 78, 73, 42, 47, 17, 74, 49, 1, 84, 47, 37, 44, 32, 71, 47, 81, 44, 37, 18, 57, 6, 1, 83, 32, 27, 54, 78, 20, 66, 10, 10, 54, 86, 66, 83, 93, 61, 30, 59, 98, 69, 98, 1, 59, 37, 83, 54, 96, 78, 46, 61, 22, 84, 66, 49, 37, 5, 30, 3, 25, 44, 49, 10, 15, 5, 10, 27, 71, 52, 15, 59, 61, 61, 86, 46, 51, 10, 83, 93, 27, 98, 61, 27, 1, 96, 15, 88, 74, 83, 52, 56, 29, 34, 52, 61, 22, 25, 32, 91, 56, 32, 73, 84, 47, 68, 91, 3, 30, 25, 13, 47, 64, 47, 78, 13, 61, 59, 15, 29, 52, 15, 32, 81, 42, 64, 56, 96, 59, 32, 93, 83, 47, 18, 93, 40, 29, 6, 64, 32, 3, 96, 71, 40, 61, 25, 32, 54, 24, 34, 76]


✨ scaled k * m0: 
Rows: 1000
Cols: 1
Vector: [24, 60, 40, 64, 64, 40, 84, 44, 12, 80, 80, 76, 96, 64, 52, 40, 80, 12, 8, 0, 8, 64, 96, 12, 44, 68, 32, 0, 72, 32, 96, 32, 40, 92, 20, 4, 92, 28, 64, 88, 36, 0, 20, 0, 48, 8, 20, 96, 20, 8, 12, 32, 8, 16, 80, 20, 28, 52, 64, 60, 68, 68, 8, 52, 40, 8, 28, 20, 4, 56, 76, 56, 16, 28, 36, 76, 60, 44, 4, 0, 64, 0, 96, 32, 64, 68, 88, 20, 72, 20, 80, 48, 60, 28, 64, 20, 44, 20, 84, 80, 60, 24, 80, 4, 20, 32, 84, 32, 8, 12, 20, 36, 16, 56, 88, 48, 64, 52, 88, 40, 96, 56, 68, 64, 16, 96, 92, 84, 96, 60, 36, 80, 56, 4, 48, 52, 76, 40, 12, 44, 0, 24, 4, 80, 76, 8, 8, 28, 96, 8, 0, 0, 72, 4, 52, 36, 0, 92, 28, 68, 52, 16, 56, 68, 48, 4, 40, 28, 92, 32, 84, 60, 92, 72, 80, 80, 68, 12, 64, 60, 52, 44, 4, 40, 96, 84, 56, 36, 48, 4, 0, 44, 72, 88, 12, 36, 48, 48, 92, 20, 28, 44, 56, 48, 72, 56, 16, 68, 20, 40, 88, 56, 44, 24, 16, 96, 32, 32, 0, 80, 52, 88, 44, 32, 40, 32, 40, 72, 40, 80, 92, 12, 28, 44, 12, 4, 84, 76, 20, 88, 80, 72, 12, 12, 12, 44, 40, 64, 36, 68, 8, 4, 4, 92, 88, 24, 44, 92, 16, 44, 20, 56, 16, 52, 84, 72, 80, 60, 4, 80, 16, 12, 28, 48, 56, 28, 24, 0, 32, 76, 20, 52, 48, 0, 16, 76, 4, 88, 36, 48, 12, 28, 16, 48, 96, 80, 68, 76, 64, 44, 72, 12, 0, 0, 24, 80, 56, 40, 88, 56, 44, 80, 96, 92, 92, 4, 64, 60, 76, 60, 92, 0, 28, 44, 96, 56, 84, 52, 20, 60, 60, 88, 80, 0, 48, 68, 92, 72, 52, 64, 52, 88, 24, 72, 76, 60, 52, 8, 64, 88, 4, 44, 56, 56, 72, 68, 8, 8, 76, 72, 96, 76, 44, 76, 92, 88, 52, 12, 96, 0, 72, 24, 16, 76, 68, 8, 72, 4, 96, 4, 12, 36, 24, 32, 28, 76, 80, 12, 44, 96, 16, 40, 40, 84, 52, 4, 0, 96, 44, 56, 16, 48, 80, 8, 72, 4, 36, 80, 4, 72, 56, 88, 52, 44, 56, 0, 24, 92, 68, 24, 96, 4, 40, 92, 68, 92, 20, 72, 60, 84, 32, 60, 8, 60, 20, 80, 36, 0, 96, 12, 4, 12, 44, 40, 64, 80, 28, 64, 72, 12, 76, 0, 84, 60, 28, 80, 0, 84, 36, 84, 72, 60, 0, 52, 96, 12, 92, 16, 28, 72, 0, 84, 96, 80, 48, 20, 24, 76, 4, 24, 60, 28, 8, 44, 24, 8, 16, 80, 24, 80, 60, 60, 48, 80, 40, 4, 0, 0, 32, 36, 28, 84, 84, 40, 8, 60, 48, 16, 40, 32, 52, 68, 80, 68, 4, 16, 32, 92, 12, 32, 56, 16, 4, 44, 4, 12, 96, 24, 4, 36, 32, 32, 84, 8, 72, 72, 0, 8, 16, 28, 20, 20, 80, 68, 56, 56, 56, 52, 48, 68, 52, 28, 48, 72, 32, 92, 4, 60, 32, 76, 36, 24, 64, 32, 60, 0, 44, 16, 72, 64, 56, 48, 48, 24, 60, 20, 64, 68, 80, 92, 64, 72, 0, 56, 16, 72, 96, 36, 20, 20, 16, 96, 12, 44, 64, 92, 0, 96, 36, 40, 48, 68, 36, 8, 68, 80, 20, 40, 36, 80, 44, 12, 0, 12, 0, 36, 12, 88, 72, 8, 68, 52, 0, 28, 12, 36, 12, 64, 52, 52, 56, 24, 12, 24, 64, 12, 8, 36, 32, 36, 12, 20, 4, 16, 36, 88, 12, 56, 88, 16, 28, 28, 96, 48, 12, 64, 8, 24, 8, 56, 80, 72, 92, 68, 88, 80, 48, 40, 12, 20, 96, 12, 52, 76, 28, 72, 56, 44, 28, 84, 76, 84, 48, 64, 32, 48, 56, 8, 36, 44, 12, 60, 80, 32, 28, 64, 32, 92, 92, 96, 84, 4, 32, 76, 64, 20, 4, 92, 72, 96, 92, 12, 28, 88, 68, 92, 48, 92, 84, 16, 32, 28, 96, 64, 8, 40, 12, 68, 60, 28, 28, 88, 48, 16, 40, 20, 36, 20, 60, 40, 24, 36, 56, 28, 24, 52, 48, 92, 16, 88, 76, 44, 64, 32, 16, 76, 84, 12, 56, 12, 36, 92, 60, 0, 84, 72, 88, 12, 24, 16, 72, 68, 20, 68, 12, 76, 80, 36, 8, 96, 4, 0, 24, 0, 8, 80, 16, 44, 52, 84, 84, 84, 76, 80, 0, 96, 48, 44, 72, 92, 92, 80, 16, 64, 60, 20, 20, 76, 60, 28, 12, 32, 36, 92, 32, 40, 64, 36, 80, 96, 48, 64, 56, 4, 60, 12, 60, 20, 56, 24, 68, 12, 92, 52, 4, 52, 80, 52, 12, 32, 32, 60, 88, 24, 28, 52, 92, 36, 64, 32, 64, 72, 40, 20, 8, 60, 40, 76, 56, 20, 36, 36, 8, 64, 20, 72, 24, 24, 96, 28, 80, 76, 68, 20, 16, 32, 76, 92, 48, 84, 84, 32, 64, 48, 80, 88, 44, 12, 36, 80, 56, 92, 76, 36, 12, 68, 32, 72, 64, 44, 56, 12, 56, 60, 28, 24, 4, 12, 84, 96, 24, 28, 84, 88, 92, 96, 16, 52, 24, 88, 48, 44, 44, 76, 44, 48, 8, 68, 64, 4, 80, 44, 16, 76, 72, 0, 60, 60, 80, 36, 52, 24, 28, 36, 44, 0, 8, 20, 68, 40, 20, 72, 56, 32, 68, 68, 96, 12, 8, 92, 32, 40, 32, 64, 92, 44, 48, 0, 24, 36, 12, 20, 60, 28, 52, 52, 72, 36, 20, 64, 80, 20, 96, 88, 20, 24, 80, 52, 8, 84, 72, 64, 20, 56, 96, 20, 32, 20, 28, 56]


✨ Parameters: 
mod: 1000 
n: 100 
m: 1000 
p: 100 
bound: [-4, 4] 

✨ Correct decryption for Delta / 2: 5.0? False
✨ Noise growth: 204
```


<br>

----

#### run an intro tutorial on how PIR should work (without encryption)

in this experiment, we get the first taste of how PIR works, but without encryption yet.

we define our server's database as a square vector of size `m x m` with each entry module `p`. 

we query a value at a specific row `r` and col `c` in plaintext, by creating a query vector of size `m x `` that is filled with `0`, with the exception of the desired column index `c`.

we then show that computing the **dot product** of the database vector to the query vector will give a result vector with all rows in the column index `c`, where you can retrieve the row `r`.

```
magick -t

✨ In this PIR tutorial, we represent a database as a square matrix, where columns are the database entries and rows are the database attributes.
✨ We intantiate the class Message(), creating a random database with mod 500, and 20 entries and 20 attributes.

✨ db: 
Rows: 20
Cols: 20
Vector: [378, 222, 276, 380, 316, 194, 454, 404, 383, 497, 237, 27, 122, 375, 491, 233, 142, 396, 8, 309, 115, 419, 288, 395, 60, 58, 292, 31, 303, 354, 58, 478, 29, 136, 49, 398, 210, 250, 461, 174, 387, 341, 123, 467, 127, 100, 66, 282, 392, 374, 40, 194, 168, 303, 364, 110, 325, 493, 308, 87, 377, 42, 265, 31, 233, 127, 72, 227, 23, 297, 24, 177, 370, 460, 115, 439, 122, 363, 493, 384, 281, 360, 317, 455, 132, 361, 190, 147, 139, 490, 351, 378, 35, 440, 464, 385, 38, 70, 441, 84, 100, 56, 275, 499, 480, 76, 418, 202, 364, 44, 16, 228, 337, 162, 232, 331, 317, 64, 355, 223, 260, 75, 432, 450, 116, 336, 474, 220, 484, 275, 454, 29, 446, 177, 186, 240, 426, 213, 392, 261, 150, 414, 401, 17, 164, 149, 148, 422, 81, 95, 88, 307, 363, 178, 468, 212, 113, 149, 318, 356, 324, 378, 22, 414, 420, 163, 393, 0, 313, 424, 461, 315, 223, 439, 243, 377, 245, 144, 64, 463, 290, 24, 290, 182, 401, 476, 88, 315, 318, 127, 13, 56, 342, 30, 359, 311, 99, 141, 138, 426, 369, 60, 283, 194, 133, 134, 184, 29, 356, 427, 318, 82, 324, 202, 28, 298, 40, 115, 194, 242, 10, 120, 64, 375, 466, 440, 253, 389, 381, 181, 73, 58, 39, 481, 274, 254, 256, 479, 205, 283, 107, 204, 328, 345, 12, 247, 95, 118, 116, 347, 260, 62, 442, 481, 80, 428, 176, 425, 480, 63, 339, 281, 185, 39, 218, 295, 341, 141, 360, 468, 280, 491, 218, 448, 430, 7, 210, 161, 203, 148, 68, 420, 245, 153, 433, 451, 456, 220, 77, 153, 196, 488, 354, 432, 470, 37, 129, 420, 305, 355, 452, 402, 188, 470, 282, 192, 466, 223, 14, 341, 143, 96, 228, 35, 115, 432, 130, 448, 253, 266, 367, 443, 150, 318, 104, 97, 444, 168, 393, 491, 236, 216, 117, 124, 420, 144, 410, 8, 435, 213, 284, 404, 97, 165, 243, 432, 155, 87, 408, 321, 473, 339, 112, 85, 361, 25, 300, 231, 69, 44, 79, 128, 321, 457, 411, 156, 355, 196, 259, 33, 93, 29, 165, 226, 49, 369, 144, 318, 448, 291, 245, 146, 135, 408, 147, 252, 46, 415, 482, 157, 99, 410, 499, 495, 406, 59, 380, 176, 169, 232]


✨ Now, let's create a random query value for row and column. Say, row 10 and column 10.
✨ query_row: 10
✨ query_col: 10

✨ Let's create a query message vector, of size 500, that is 1 at the query column and 0 elsewhere.
✨ query: 
Rows: 20
Cols: 1
Vector: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

✨ Let's compute the resulting message vector, which is the dot product of the database and the query.
✨ result = db * query: 
Rows: 20
Cols: 1
Vector: [237, 58, 40, 24, 351, 16, 454, 88, 461, 13, 318, 73, 260, 280, 196, 143, 236, 473, 93, 99]


✨ Finally, let's compute the message retrieved from the database, by getting the element at the query row and column.
✨ db.get_query_element(10, 10): 318

✨ This should be the same as the result message vector element at the query row.
✨ result.get_query_element(10, 0): 318

✨ Are they the same? Did we get a correct retrieval? True
```

<br>


----

#### run a simple PIR experiment with secret key Regev encryption

we are ready to run our first simple PIR experiment, where we build a query vector as in the previous experiment, but encrypt it using the secret key `s` from the Regev encryption scheme.


```
magick -p

✨ 1. We start by magicreating a random message vector as a square m x m database with mod p
✨ db: 
Rows: 100
Cols: 100
Vector: [1, 1, 1, 2, 0, 3, 1, 3, 2, 2, 3, 2, 1, 1, 1, 1, 2, 0, 3, 2, 1, 0, 1, 2, 1, 3, 2, 0, 0, 1, 1, 0, 2, 2, 3, 3, 3, 0, 0, 0, 3, 1, 2, 0, 3, 3, 0, 2, 2, 2, 3, 3, 3, 1, 0, 3, 1, 3, 1, 3, 1, 1, 0, 3, 0, 1, 1, 2, 2, 3, 0, 1, 1, 0, 2, 3, 0, 3, 3, 1, 0, 3, 0, 3, 1, 1, 0, 3, 3, 2, 2, 1, 1, 1, 3, 2, 2, 3, 3, 1, 1, 3, 1, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 2, 1, 2, 1, 0, 0, 1, 3, 0, 2, 3, 0, 2, 0, 2, 1, 1, 1, 2, 1, 1, 3, 1, 1, 0, 1, 3, 2, 1, 3, 2, 3, 0, 2, 3, 0, 0, 1, 3, 3, 2, 0, 1, 0, 2, 0, 3, 2, 0, 0, 1, 0, 1, 1, 1, 2, 0, 2, 1, 2, 1, 3, 3, 1, 3, 0, 3, 2, 0, 2, 0, 3, 2, 0, 2, 3, 2, 1, 0, 3, 1, 0, 2, 1, 3, 0, 3, 1, 1, 2, 0, 3, 1, 3, 1, 0, 1, 2, 1, 3, 1, 2, 3, 3, 3, 2, 3, 0, 3, 3, 1, 1, 0, 2, 0, 2, 3, 2, 0, 3, 3, 1, 3, 1, 2, 0, 3, 2, 3, 3, 1, 1, 2, 0, 1, 2, 1, 1, 0, 3, 0, 2, 0, 0, 1, 0, 2, 0, 0, 2, 2, 0, 1, 1, 0, 2, 0, 0, 1, 1, 0, 3, 3, 2, 1, 3, 2, 1, 3, 0, 2, 3, 3, 3, 0, 3, 1, 1, 3, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 3, 3, 2, 1, 1, 0, 2, 3, 3, 2, 1, 3, 2, 0, 2, 3, 1, 2, 3, 3, 0, 3, 3, 2, 1, 1, 1, 3, 1, 2, 3, 2, 3, 1, 1, 3, 2, 2, 2, 3, 0, 0, 0, 3, 0, 1, 0, 2, 0, 2, 3, 3, 3, 0, 3, 2, 1, 3, 2, 1, 0, 0, 3, 1, 2, 3, 0, 1, 2, 0, 3, 3, 1, 3, 3, 3, 1, 1, 2, 3, 3, 3, 1, 0, 3, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 3, 3, 3, 2, 2, 0, 0, 2, 1, 0, 3, 2, 2, 2, 0, 3, 2, 3, 0, 0, 3, 3, 1, 2, 1, 3, 3, 1, 1, 0, 3, 3, 2, 2, 3, 2, 2, 1, 0, 3, 1, 3, 0, 2, 1, 2, 3, 3, 3, 1, 1, 3, 0, 3, 1, 2, 1, 0, 1, 3, 2, 3, 0, 3, 3, 1, 2, 2, 1, 1, 3, 2, 0, 1, 1, 1, 2, 2, 3, 3, 0, 0, 0, 1, 0, 1, 1, 3, 1, 2, 0, 2, 2, 2, 3, 0, 1, 2, 3, 3, 2, 3, 0, 2, 2, 2, 0, 0, 1, 2, 1, 3, 3, 2, 1, 2, 3, 0, 3, 2, 1, 0, 2, 2, 2, 0, 0, 2, 0, 0, 3, 2, 3, 3, 0, 0, 3, 3, 0, 1, 3, 1, 0, 0, 3, 3, 1, 2, 3, 2, 0, 3, 1, 3, 3, 0, 1, 3, 2, 1, 2, 1, 1, 0, 0, 3, 3, 2, 1, 2, 1, 2, 0, 2, 2, 2, 3, 2, 1, 3, 2, 2, 2, 3, 2, 2, 2, 1, 0, 2, 3, 0, 3, 0, 1, 2, 3, 1, 2, 3, 0, 0, 3, 3, 0, 1, 0, 3, 1, 0, 1, 1, 2, 0, 3, 3, 0, 0, 3, 1, 0, 2, 0, 1, 3, 0, 1, 3, 2, 2, 0, 0, 0, 1, 1, 3, 3, 0, 3, 1, 2, 1, 0, 0, 2, 0, 3, 1, 3, 1, 3, 3, 1, 3, 3, 0, 1, 2, 1, 2, 2, 1, 0, 0, 1, 3, 1, 0, 2, 2, 0, 2, 3, 1, 1, 2, 1, 0, 1, 3, 1, 1, 1, 3, 3, 1, 1, 2, 0, 3, 1, 1, 2, 0, 3, 2, 2, 1, 3, 3, 1, 0, 1, 1, 3, 3, 0, 1, 0, 3, 3, 0, 3, 3, 3, 3, 1, 2, 1, 1, 3, 3, 2, 3, 2, 0, 0, 1, 3, 0, 3, 3, 2, 2, 2, 1, 3, 2, 3, 1, 1, 2, 2, 2, 3, 2, 1, 0, 2, 2, 2, 3, 2, 0, 0, 1, 0, 1, 2, 1, 3, 1, 2, 2, 3, 3, 3, 0, 0, 1, 3, 1, 2, 0, 3, 2, 1, 2, 0, 1, 0, 3, 2, 0, 1, 1, 3, 1, 2, 3, 3, 0, 2, 2, 0, 2, 1, 3, 1, 2, 0, 0, 2, 2, 3, 3, 3, 3, 0, 3, 0, 1, 0, 1, 2, 0, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 3, 2, 1, 3, 2, 0, 3, 1, 2, 0, 0, 1, 1, 0, 3, 2, 2, 0, 1, 0, 2, 2, 0, 1, 0, 1, 1, 3, 0, 0, 1, 2, 1, 2, 1, 1, 1, 3, 2, 0, 0, 2, 3, 0, 2, 3, 2, 0, 3, 1, 1, 0, 1, 3, 0, 1, 3, 3, 3, 0, 3, 3, 3, 1, 3, 0, 1, 0, 0, 3, 0, 3, 2, 2, 2, 1, 2, 0, 1, 2, 1, 3, 2, 1, 3, 1, 3, 1, 0, 3, 0, 0, 1, 2, 3, 3, 2, 0, 0, 0, 0, 3, 1, 3, 0, 1, 3, 3, 2, 0, 3, 1, 1, 3, 1, 2, 0, 2, 2, 0, 1, 1, 0, 3, 1, 2, 3, 2, 2, 0, 2, 1, 0, 0, 0, 0, 2, 3, 1, 1, 3, 1, 3, 2, 0, 3, 1, 0, 3, 1, 0, 2, 2, 2, 3, 0, 3, 0, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 1, 2, 0, 3, 3, 0, 1, 2, 2, 2, 1, 0, 0, 3, 3, 2, 2, 3, 1, 1, 2, 3, 0, 0, 0, 3, 0, 0, 2, 3, 1, 0, 2, 0, 2, 0, 2, 0, 1, 1, 2, 3, 0, 2, 0, 0, 1, 1, 2, 1, 0, 3, 0, 3, 1, 1, 2, 3, 1, 3, 0, 1, 1, 0, 1, 1, 3, 1, 3, 0, 3, 3, 0, 3, 1, 2, 1, 0, 3, 1, 3, 3, 0, 0, 2, 0, 3, 2, 3, 3, 3, 3, 1, 2, 3, 3, 1, 3, 3, 3, 0, 1, 1, 0, 3, 0, 3, 0, 0, 2, 2, 1, 0, 3, 0, 1, 0, 2, 0, 3, 2, 1, 2, 2, 1, 2, 0, 0, 0, 2, 1, 2, 3, 3, 1, 1, 3, 1, 0, 3, 1, 0, 2, 2, 3, 2, 3, 3, 1, 0, 0, 0, 0, 3, 2, 3, 0, 2, 2, 3, 3, 1, 1, 2, 0, 1, 2, 3, 1, 3, 2, 0, 2, 3, 3, 1, 0, 1, 2, 1, 1, 3, 0, 1, 0, 1, 2, 1, 0, 2, 0, 2, 1, 2, 1, 1, 1, 2, 3, 3, 2, 0, 2, 1, 0, 0, 1, 3, 2, 2, 1, 3, 3, 0, 0, 1, 2, 0, 2, 2, 0, 0, 0, 3, 3, 3, 0, 2, 3, 2, 3, 0, 3, 3, 3, 0, 3, 0, 3, 3, 1, 3, 1, 0, 3, 3, 0, 3, 1, 0, 3, 3, 2, 2, 3, 1, 3, 2, 0, 1, 1, 0, 3, 1, 0, 0, 3, 1, 3, 2, 3, 2, 1, 0, 3, 3, 1, 2, 3, 2, 0, 3, 2, 3, 3, 0, 3, 2, 2, 3, 1, 1, 0, 2, 2, 0, 2, 2, 0, 2, 2, 2, 1, 1, 3, 2, 3, 2, 3, 2, 1, 0, 2, 0, 1, 1, 3, 2, 0, 0, 0, 1, 0, 3, 2, 3, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 3, 0, 1, 1, 1, 0, 2, 2, 1, 0, 2, 2, 2, 2, 3, 0, 3, 3, 0, 3, 2, 0, 2, 3, 1, 1, 3, 2, 3, 2, 3, 1, 0, 0, 3, 1, 0, 3, 1, 1, 2, 0, 0, 3, 2, 0, 0, 1, 0, 3, 3, 2, 2, 3, 1, 3, 2, 1, 3, 2, 2, 2, 0, 3, 0, 1, 0, 3, 3, 0, 0, 3, 3, 3, 0, 2, 3, 3, 1, 1, 3, 1, 2, 1, 2, 2, 0, 0, 1, 0, 1, 2, 2, 0, 2, 2, 3, 0, 3, 2, 2, 3, 1, 0, 0, 0, 0, 0, 1, 1, 3, 2, 2, 1, 1, 2, 3, 0, 2, 1, 3, 0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 1, 0, 3, 2, 2, 2, 2, 0, 0, 1, 1, 2, 0, 1, 0, 1, 0, 0, 0, 3, 3, 2, 1, 1, 2, 0, 3, 1, 0, 0, 3, 1, 1, 0, 0, 2, 1, 0, 0, 1, 3, 2, 1, 2, 1, 1, 3, 2, 3, 3, 0, 2, 2, 2, 2, 1, 2, 3, 0, 0, 3, 0, 2, 1, 3, 2, 1, 3, 3, 1, 3, 3, 2, 2, 3, 0, 1, 0, 2, 1, 3, 0, 2, 0, 1, 0, 0, 3, 3, 0, 3, 1, 1, 1, 0, 1, 0, 2, 0, 1, 1, 2, 0, 0, 1, 0, 1, 0, 0, 2, 3, 0, 3, 2, 0, 2, 2, 1, 1, 3, 1, 2, 1, 0, 2, 0, 3, 3, 3, 2, 0, 1, 3, 0, 3, 3, 2, 3, 0, 1, 3, 3, 1, 1, 1, 3, 3, 3, 2, 1, 3, 2, 0, 0, 2, 2, 2, 0, 0, 2, 1, 1, 2, 3, 3, 1, 0, 0, 3, 2, 1, 0, 2, 2, 3, 2, 1, 3, 0, 1, 2, 3, 2, 3, 0, 1, 0, 1, 1, 0, 1, 2, 2, 3, 1, 0, 3, 3, 1, 0, 2, 0, 2, 2, 0, 3, 0, 0, 0, 2, 2, 1, 1, 2, 0, 3, 1, 2, 0, 2, 0, 2, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 2, 3, 0, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 2, 3, 3, 1, 2, 2, 2, 2, 0, 3, 2, 2, 0, 1, 1, 2, 3, 1, 2, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 2, 1, 0, 3, 2, 0, 2, 3, 1, 2, 0, 0, 3, 3, 0, 0, 3, 3, 1, 0, 3, 2, 2, 1, 2, 0, 1, 3, 1, 1, 3, 0, 3, 1, 3, 0, 3, 0, 1, 3, 0, 0, 0, 0, 2, 3, 3, 1, 3, 0, 1, 0, 1, 3, 2, 2, 1, 0, 1, 2, 2, 1, 2, 1, 1, 3, 3, 0, 1, 0, 3, 1, 2, 2, 2, 0, 3, 3, 3, 3, 0, 3, 2, 2, 2, 3, 3, 1, 1, 3, 2, 3, 3, 0, 1, 3, 1, 1, 3, 2, 0, 1, 3, 2, 1, 2, 1, 2, 0, 0, 3, 1, 0, 2, 2, 1, 2, 0, 3, 2, 0, 1, 1, 2, 2, 3, 3, 1, 2, 3, 1, 2, 0, 2, 0, 3, 2, 1, 2, 3, 3, 0, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 0, 1, 2, 1, 1, 3, 3, 3, 2, 3, 2, 1, 0, 2, 0, 2, 3, 1, 1, 0, 2, 0, 2, 1, 1, 0, 3, 1, 2, 2, 3, 2, 2, 2, 1, 2, 2, 1, 2, 2, 3, 1, 3, 0, 2, 3, 2, 1, 1, 1, 0, 0, 1, 1, 0, 3, 0, 2, 2, 1, 3, 2, 1, 2, 0, 3, 3, 2, 3, 3, 3, 2, 0, 2, 3, 2, 2, 1, 1, 3, 3, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 0, 2, 1, 3, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 0, 1, 2, 3, 2, 2, 3, 0, 1, 1, 1, 0, 0, 0, 2, 0, 3, 0, 1, 3, 2, 2, 2, 0, 2, 3, 0, 2, 1, 1, 0, 0, 1, 3, 2, 2, 3, 3, 2, 3, 2, 2, 1, 3, 0, 1, 1, 2, 2, 3, 3, 0, 1, 2, 0, 3, 2, 3, 3, 1, 1, 0, 2, 0, 2, 0, 0, 0, 3, 3, 1, 2, 1, 1, 0, 0, 1, 0, 2, 3, 3, 2, 0, 0, 1, 1, 0, 2, 1, 3, 2, 0, 1, 3, 0, 0, 1, 0, 3, 1, 0, 0, 1, 0, 3, 2, 1, 0, 2, 2, 0, 2, 3, 0, 0, 1, 3, 0, 0, 0, 2, 1, 0, 2, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0, 3, 2, 0, 1, 1, 2, 3, 0, 1, 2, 3, 3, 3, 1, 0, 2, 3, 1, 2, 1, 1, 3, 0, 3, 2, 3, 1, 1, 3, 3, 0, 2, 0, 2, 0, 0, 3, 2, 1, 0, 3, 1, 3, 2, 3, 1, 0, 2, 2, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0, 3, 3, 0, 2, 3, 0, 3, 2, 0, 3, 2, 3, 1, 2, 1, 1, 0, 0, 1, 2, 1, 2, 0, 0, 0, 2, 2, 0, 2, 0, 2, 3, 3, 1, 1, 1, 1, 0, 0, 3, 0, 3, 0, 1, 3, 2, 2, 2, 3, 0, 3, 1, 1, 1, 1, 1, 1, 0, 3, 2, 1, 2, 2, 0, 2, 0, 1, 2, 1, 1, 2, 2, 1, 2, 0, 3, 0, 0, 3, 2, 2, 0, 2, 0, 1, 1, 0, 3, 2, 3, 3, 1, 2, 1, 2, 3, 3, 1, 0, 1, 2, 3, 3, 3, 1, 1, 2, 3, 1, 3, 1, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 2, 2, 3, 1, 2, 0, 2, 1, 3, 1, 3, 2, 0, 3, 1, 1, 3, 1, 1, 3, 1, 2, 3, 0, 2, 3, 2, 0, 2, 0, 1, 2, 3, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1, 0, 0, 0, 3, 3, 1, 2, 3, 0, 2, 3, 0, 0, 1, 3, 2, 0, 1, 2, 3, 2, 0, 3, 0, 1, 2, 1, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 3, 2, 3, 1, 0, 3, 1, 2, 0, 2, 3, 0, 3, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 3, 0, 0, 2, 1, 3, 3, 1, 3, 2, 1, 3, 0, 0, 0, 1, 3, 0, 2, 0, 2, 2, 1, 3, 2, 2, 1, 0, 1, 0, 1, 1, 1, 1, 2, 0, 1, 3, 0, 3, 1, 0, 2, 2, 3, 1, 3, 3, 0, 3, 0, 2, 0, 3, 2, 1, 2, 2, 3, 2, 0, 1, 2, 3, 1, 1, 2, 3, 2, 3, 1, 0, 3, 2, 0, 0, 3, 3, 0, 2, 2, 2, 1, 2, 2, 0, 2, 0, 0, 2, 1, 1, 0, 1, 2, 0, 0, 3, 2, 3, 0, 2, 1, 3, 3, 0, 1, 1, 1, 1, 3, 3, 2, 0, 2, 0, 0, 0, 1, 3, 2, 2, 0, 0, 0, 0, 2, 0, 0, 1, 3, 0, 3, 0, 0, 3, 0, 2, 2, 3, 3, 3, 3, 1, 0, 0, 3, 2, 0, 3, 0, 1, 1, 3, 3, 2, 1, 2, 0, 2, 1, 0, 0, 3, 1, 2, 2, 2, 2, 1, 3, 2, 0, 3, 2, 1, 1, 3, 1, 0, 1, 3, 1, 2, 1, 2, 3, 1, 2, 0, 2, 0, 3, 2, 3, 0, 3, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 2, 3, 3, 0, 3, 1, 1, 3, 2, 1, 2, 1, 1, 0, 3, 0, 3, 0, 3, 2, 1, 0, 1, 0, 3, 0, 1, 3, 0, 0, 3, 1, 3, 3, 2, 2, 2, 1, 1, 0, 1, 1, 3, 3, 1, 1, 2, 2, 0, 1, 2, 3, 2, 3, 0, 1, 1, 1, 0, 2, 2, 2, 3, 2, 1, 3, 0, 3, 0, 0, 0, 0, 3, 1, 1, 2, 0, 2, 2, 3, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 1, 1, 0, 0, 1, 2, 1, 1, 1, 0, 1, 1, 1, 0, 3, 2, 3, 2, 2, 1, 3, 3, 0, 2, 3, 2, 0, 1, 2, 3, 0, 1, 0, 3, 2, 2, 3, 0, 0, 0, 0, 3, 3, 2, 0, 3, 0, 3, 1, 1, 3, 1, 1, 1, 1, 0, 2, 2, 2, 1, 0, 0, 3, 3, 1, 2, 0, 0, 3, 1, 1, 3, 2, 3, 2, 1, 1, 2, 2, 1, 1, 3, 2, 1, 2, 1, 1, 2, 1, 3, 2, 3, 1, 0, 2, 1, 2, 1, 3, 1, 0, 3, 3, 1, 2, 1, 0, 2, 0, 3, 1, 3, 0, 2, 1, 3, 0, 3, 0, 0, 0, 3, 0, 0, 3, 3, 2, 1, 2, 0, 2, 1, 0, 3, 1, 1, 0, 1, 2, 1, 3, 3, 1, 1, 3, 3, 2, 1, 2, 1, 0, 0, 3, 2, 2, 0, 1, 2, 1, 3, 2, 3, 1, 3, 3, 2, 3, 1, 3, 1, 3, 0, 2, 0, 3, 0, 0, 2, 2, 1, 1, 1, 0, 1, 2, 2, 0, 1, 0, 1, 2, 0, 1, 0, 2, 3, 0, 0, 3, 0, 1, 1, 0, 2, 1, 2, 3, 1, 0, 0, 3, 1, 1, 0, 3, 3, 2, 2, 3, 0, 2, 3, 3, 3, 3, 0, 2, 0, 3, 2, 3, 1, 0, 1, 3, 2, 1, 3, 2, 1, 3, 3, 1, 2, 2, 2, 1, 0, 0, 1, 2, 3, 2, 0, 1, 1, 2, 0, 2, 0, 1, 0, 3, 3, 1, 3, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 3, 3, 2, 1, 2, 1, 2, 2, 2, 1, 0, 1, 2, 3, 0, 3, 1, 0, 3, 3, 1, 1, 2, 0, 0, 1, 3, 1, 0, 3, 2, 1, 2, 0, 2, 2, 2, 2, 2, 1, 2, 1, 0, 2, 3, 2, 1, 2, 1, 2, 1, 2, 3, 2, 2, 2, 1, 3, 1, 2, 2, 2, 2, 3, 2, 1, 0, 3, 2, 3, 3, 3, 0, 2, 0, 3, 0, 0, 0, 2, 1, 3, 0, 0, 0, 3, 2, 0, 1, 1, 0, 0, 2, 3, 1, 2, 0, 0, 2, 0, 3, 3, 0, 3, 1, 3, 1, 2, 2, 1, 1, 0, 3, 3, 1, 2, 2, 1, 1, 1, 2, 0, 2, 3, 1, 0, 0, 1, 1, 1, 2, 0, 1, 0, 0, 2, 2, 0, 0, 2, 2, 3, 0, 0, 2, 1, 3, 1, 2, 2, 1, 0, 2, 3, 1, 3, 1, 3, 3, 1, 2, 3, 0, 1, 2, 0, 1, 3, 2, 2, 0, 2, 1, 3, 3, 2, 0, 3, 0, 1, 3, 3, 3, 2, 3, 0, 3, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 0, 3, 3, 0, 0, 1, 3, 2, 0, 1, 0, 1, 2, 1, 2, 3, 3, 2, 3, 0, 0, 2, 1, 3, 2, 0, 1, 0, 1, 3, 1, 3, 2, 3, 1, 2, 3, 2, 1, 3, 1, 3, 0, 1, 2, 0, 1, 1, 1, 1, 3, 1, 1, 3, 2, 1, 2, 0, 0, 3, 2, 3, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0, 0, 1, 0, 0, 3, 3, 1, 3, 3, 3, 1, 3, 3, 0, 0, 3, 2, 2, 1, 0, 1, 2, 2, 1, 0, 2, 0, 1, 1, 2, 1, 1, 0, 2, 0, 0, 3, 1, 0, 1, 2, 3, 3, 0, 1, 0, 2, 2, 1, 1, 1, 2, 3, 3, 1, 3, 0, 0, 1, 1, 1, 2, 3, 1, 3, 3, 3, 1, 3, 0, 1, 2, 0, 1, 0, 2, 3, 1, 3, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 3, 1, 3, 3, 1, 0, 3, 0, 1, 2, 0, 0, 1, 0, 0, 2, 1, 3, 1, 0, 1, 3, 2, 3, 3, 3, 1, 2, 3, 3, 3, 1, 1, 0, 3, 0, 2, 1, 3, 3, 1, 1, 3, 1, 3, 0, 3, 3, 1, 1, 2, 1, 3, 3, 3, 0, 3, 3, 0, 2, 3, 2, 3, 1, 2, 3, 2, 3, 0, 1, 2, 1, 3, 1, 3, 2, 1, 0, 3, 3, 1, 0, 2, 3, 0, 0, 3, 3, 0, 0, 1, 0, 2, 2, 1, 0, 3, 2, 0, 2, 0, 2, 1, 3, 2, 3, 0, 0, 0, 0, 0, 3, 1, 2, 2, 0, 2, 2, 1, 3, 1, 3, 0, 1, 1, 0, 3, 1, 1, 3, 0, 0, 2, 1, 0, 0, 2, 1, 0, 3, 0, 2, 2, 0, 1, 0, 2, 2, 3, 3, 0, 0, 1, 1, 1, 2, 0, 3, 1, 2, 0, 2, 3, 0, 1, 1, 2, 3, 3, 1, 0, 2, 1, 0, 1, 0, 3, 1, 0, 1, 1, 2, 2, 2, 0, 1, 3, 2, 2, 3, 2, 1, 0, 1, 3, 0, 0, 1, 2, 2, 2, 3, 2, 1, 0, 2, 3, 3, 1, 1, 3, 2, 0, 1, 1, 0, 0, 2, 3, 3, 1, 2, 3, 1, 1, 2, 2, 3, 0, 2, 3, 1, 1, 3, 1, 2, 1, 0, 1, 2, 0, 0, 0, 1, 3, 1, 0, 1, 1, 3, 2, 2, 3, 1, 2, 2, 2, 1, 1, 0, 2, 2, 1, 3, 1, 1, 1, 2, 1, 1, 1, 3, 2, 0, 0, 2, 0, 2, 0, 0, 3, 1, 1, 0, 3, 1, 1, 2, 0, 1, 1, 0, 0, 1, 1, 3, 0, 0, 0, 2, 2, 1, 2, 3, 3, 3, 0, 2, 2, 0, 2, 1, 3, 0, 1, 1, 1, 1, 1, 1, 3, 2, 0, 0, 0, 2, 2, 1, 0, 1, 0, 3, 2, 2, 1, 3, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 0, 2, 1, 1, 1, 2, 0, 0, 2, 1, 2, 2, 0, 3, 0, 1, 0, 1, 1, 0, 2, 1, 0, 1, 3, 1, 0, 1, 2, 2, 3, 1, 2, 3, 3, 0, 0, 1, 3, 1, 3, 1, 3, 3, 1, 0, 2, 1, 2, 1, 3, 2, 2, 1, 2, 3, 3, 2, 0, 1, 1, 3, 1, 3, 2, 3, 0, 0, 3, 1, 3, 3, 0, 0, 2, 2, 2, 2, 2, 1, 0, 3, 1, 3, 3, 2, 2, 1, 3, 2, 3, 2, 1, 0, 1, 2, 0, 3, 2, 2, 1, 1, 1, 3, 0, 0, 3, 2, 1, 1, 0, 2, 0, 0, 1, 0, 0, 2, 1, 2, 1, 2, 3, 3, 0, 2, 1, 3, 2, 3, 2, 0, 2, 0, 3, 3, 1, 0, 3, 2, 0, 3, 2, 0, 2, 3, 0, 1, 1, 3, 2, 3, 0, 0, 3, 1, 3, 2, 1, 2, 2, 0, 3, 3, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 2, 2, 1, 3, 0, 0, 3, 0, 3, 1, 3, 2, 2, 1, 1, 1, 3, 2, 3, 0, 1, 2, 2, 3, 1, 3, 3, 3, 2, 3, 1, 0, 2, 1, 3, 3, 2, 3, 1, 2, 1, 3, 3, 2, 3, 2, 1, 0, 2, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 0, 3, 2, 1, 1, 3, 3, 3, 2, 1, 0, 1, 3, 3, 1, 3, 0, 3, 2, 1, 3, 0, 0, 1, 2, 1, 0, 2, 0, 0, 2, 1, 1, 0, 0, 3, 0, 0, 3, 3, 1, 3, 3, 3, 2, 2, 1, 3, 1, 1, 2, 1, 0, 1, 2, 1, 1, 2, 3, 0, 2, 0, 2, 0, 0, 2, 1, 3, 2, 1, 1, 1, 1, 0, 1, 2, 1, 2, 2, 1, 2, 0, 1, 3, 1, 2, 2, 3, 3, 3, 1, 3, 3, 2, 2, 3, 1, 1, 0, 2, 3, 2, 3, 2, 1, 0, 2, 3, 2, 0, 0, 3, 0, 2, 2, 3, 3, 2, 3, 0, 0, 0, 3, 1, 2, 0, 0, 2, 0, 1, 3, 1, 3, 3, 3, 3, 0, 3, 2, 2, 3, 0, 2, 2, 3, 0, 3, 0, 3, 1, 1, 2, 3, 2, 2, 3, 0, 2, 3, 2, 1, 0, 0, 2, 3, 0, 0, 3, 0, 0, 2, 1, 2, 1, 3, 1, 0, 0, 3, 0, 3, 0, 3, 2, 3, 0, 1, 3, 0, 2, 2, 1, 1, 3, 1, 2, 3, 1, 2, 2, 2, 1, 2, 3, 2, 1, 3, 2, 0, 0, 3, 1, 0, 1, 0, 0, 1, 0, 2, 2, 2, 1, 1, 2, 3, 0, 2, 0, 3, 2, 1, 3, 0, 3, 0, 2, 2, 3, 0, 0, 0, 0, 3, 0, 3, 0, 2, 1, 2, 2, 0, 0, 1, 1, 2, 3, 3, 3, 2, 0, 2, 2, 0, 3, 0, 1, 2, 2, 3, 2, 2, 2, 1, 3, 1, 2, 1, 0, 2, 1, 3, 2, 1, 1, 3, 0, 3, 1, 1, 0, 3, 1, 2, 2, 0, 2, 1, 1, 0, 2, 0, 3, 0, 2, 2, 2, 0, 2, 3, 1, 0, 1, 0, 0, 1, 1, 1, 0, 3, 3, 2, 2, 2, 1, 3, 2, 0, 1, 3, 0, 1, 1, 2, 3, 2, 3, 0, 3, 0, 1, 3, 0, 1, 1, 1, 0, 2, 1, 3, 3, 2, 2, 0, 0, 3, 1, 1, 2, 1, 3, 0, 0, 2, 2, 3, 1, 0, 0, 2, 0, 2, 1, 0, 0, 2, 0, 1, 1, 1, 0, 2, 3, 1, 0, 2, 2, 1, 0, 3, 3, 3, 0, 1, 2, 3, 3, 1, 2, 1, 0, 1, 0, 2, 0, 0, 3, 3, 1, 2, 1, 1, 2, 0, 1, 2, 2, 2, 3, 0, 2, 3, 2, 0, 3, 2, 1, 2, 2, 1, 1, 3, 0, 3, 2, 1, 2, 0, 1, 1, 3, 1, 0, 1, 3, 1, 3, 1, 3, 3, 0, 0, 2, 2, 1, 3, 0, 3, 3, 1, 1, 0, 3, 3, 3, 1, 2, 3, 2, 0, 0, 2, 1, 3, 1, 0, 1, 1, 0, 0, 2, 0, 1, 2, 0, 0, 0, 1, 1, 2, 3, 0, 2, 0, 1, 2, 3, 2, 2, 2, 0, 2, 1, 1, 2, 3, 3, 1, 3, 2, 2, 0, 1, 2, 0, 0, 3, 0, 1, 1, 2, 0, 2, 2, 2, 0, 3, 2, 0, 3, 2, 0, 3, 3, 1, 0, 1, 2, 0, 0, 0, 2, 2, 3, 2, 2, 0, 3, 3, 1, 3, 1, 1, 0, 1, 2, 3, 3, 0, 0, 1, 1, 3, 3, 0, 2, 2, 0, 3, 2, 2, 3, 2, 0, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 2, 2, 3, 0, 3, 0, 1, 2, 0, 1, 3, 3, 2, 3, 0, 1, 2, 2, 1, 3, 2, 3, 2, 2, 1, 2, 2, 3, 1, 1, 0, 2, 0, 0, 3, 3, 1, 0, 1, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 1, 3, 2, 1, 1, 1, 2, 0, 2, 2, 0, 3, 1, 3, 3, 2, 3, 3, 1, 3, 1, 1, 0, 3, 3, 0, 2, 0, 3, 2, 2, 3, 3, 2, 2, 3, 2, 3, 3, 3, 0, 2, 1, 1, 2, 1, 3, 1, 2, 3, 1, 2, 0, 3, 1, 0, 0, 0, 3, 2, 1, 1, 3, 3, 0, 3, 2, 0, 1, 2, 2, 0, 0, 2, 2, 3, 0, 1, 1, 0, 1, 0, 1, 3, 1, 1, 3, 2, 2, 1, 3, 0, 1, 1, 2, 0, 3, 2, 1, 0, 3, 0, 0, 0, 3, 2, 2, 1, 3, 3, 3, 1, 3, 1, 2, 3, 1, 0, 3, 0, 2, 0, 0, 2, 1, 0, 0, 3, 3, 0, 2, 0, 3, 1, 1, 0, 1, 2, 0, 3, 3, 1, 1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 1, 1, 0, 2, 0, 0, 1, 1, 0, 3, 2, 0, 0, 2, 3, 2, 3, 1, 2, 1, 3, 2, 1, 1, 3, 3, 2, 2, 3, 3, 0, 0, 0, 2, 0, 2, 3, 0, 3, 1, 0, 3, 1, 2, 1, 2, 3, 3, 2, 3, 1, 0, 3, 3, 1, 3, 3, 0, 2, 2, 1, 3, 1, 2, 0, 1, 0, 1, 0, 0, 3, 3, 2, 1, 0, 2, 2, 0, 0, 1, 0, 2, 1, 0, 1, 2, 0, 3, 0, 0, 3, 2, 3, 0, 3, 2, 3, 2, 1, 3, 1, 1, 0, 3, 3, 2, 1, 2, 3, 1, 2, 1, 1, 3, 0, 2, 2, 2, 0, 2, 1, 1, 0, 3, 1, 2, 3, 3, 2, 1, 3, 1, 1, 2, 1, 3, 0, 1, 3, 0, 2, 2, 2, 1, 0, 1, 1, 1, 1, 2, 3, 0, 0, 2, 3, 3, 0, 1, 3, 1, 0, 0, 3, 0, 0, 0, 1, 2, 1, 1, 0, 0, 3, 1, 1, 1, 2, 2, 2, 1, 2, 0, 3, 0, 2, 0, 0, 0, 2, 3, 1, 2, 2, 0, 2, 0, 2, 2, 0, 3, 1, 0, 0, 2, 1, 0, 0, 0, 3, 0, 0, 3, 0, 3, 3, 3, 2, 1, 2, 3, 2, 0, 1, 2, 2, 0, 0, 2, 2, 3, 2, 1, 3, 2, 0, 3, 1, 0, 0, 3, 3, 1, 0, 0, 1, 2, 3, 1, 1, 3, 0, 2, 3, 3, 2, 1, 3, 3, 2, 3, 1, 3, 0, 0, 1, 3, 0, 1, 2, 3, 0, 1, 3, 0, 0, 1, 1, 3, 0, 1, 3, 0, 2, 2, 3, 3, 3, 1, 2, 2, 1, 1, 2, 0, 1, 3, 3, 0, 1, 3, 0, 0, 3, 0, 3, 1, 2, 0, 0, 0, 1, 1, 2, 0, 1, 2, 0, 1, 3, 0, 3, 1, 1, 2, 3, 0, 3, 0, 3, 3, 1, 2, 2, 0, 1, 0, 1, 2, 1, 3, 3, 2, 3, 2, 0, 1, 2, 1, 1, 3, 1, 0, 0, 1, 3, 1, 2, 1, 2, 0, 0, 2, 1, 3, 3, 1, 2, 0, 0, 2, 3, 3, 0, 1, 0, 1, 1, 0, 1, 2, 2, 3, 2, 3, 0, 1, 1, 2, 3, 1, 2, 1, 1, 2, 2, 2, 3, 2, 3, 0, 1, 2, 3, 3, 3, 1, 2, 2, 1, 2, 1, 2, 3, 3, 0, 3, 3, 3, 0, 3, 0, 0, 0, 1, 2, 1, 1, 3, 0, 2, 3, 2, 2, 1, 1, 1, 0, 3, 0, 3, 3, 1, 0, 2, 3, 2, 1, 1, 1, 3, 2, 0, 3, 0, 3, 3, 2, 2, 0, 3, 1, 1, 1, 3, 0, 0, 3, 0, 3, 1, 2, 1, 3, 1, 1, 0, 0, 1, 2, 3, 3, 2, 2, 0, 1, 3, 3, 3, 2, 0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 2, 2, 3, 3, 1, 1, 1, 0, 3, 0, 3, 2, 2, 3, 1, 1, 0, 3, 3, 2, 1, 1, 2, 2, 1, 3, 0, 3, 0, 0, 2, 1, 2, 1, 1, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 3, 1, 0, 3, 0, 0, 0, 2, 1, 0, 2, 2, 1, 1, 0, 3, 3, 3, 2, 3, 1, 3, 1, 3, 3, 2, 1, 3, 0, 3, 2, 1, 0, 3, 1, 2, 2, 1, 3, 0, 1, 0, 0, 1, 2, 0, 0, 0, 3, 1, 2, 0, 0, 1, 0, 2, 3, 0, 2, 2, 2, 3, 2, 2, 2, 3, 1, 2, 2, 3, 1, 0, 1, 2, 2, 2, 1, 0, 0, 1, 1, 1, 0, 3, 2, 0, 0, 1, 2, 3, 1, 3, 0, 2, 3, 2, 0, 1, 0, 2, 0, 2, 3, 3, 1, 1, 3, 3, 2, 2, 1, 3, 0, 0, 0, 3, 1, 0, 2, 0, 0, 3, 2, 1, 3, 3, 3, 0, 1, 1, 3, 3, 0, 0, 1, 1, 3, 1, 3, 2, 3, 1, 0, 1, 3, 0, 3, 3, 1, 0, 0, 3, 0, 1, 0, 2, 1, 0, 0, 0, 1, 1, 3, 2, 1, 1, 0, 2, 1, 1, 2, 3, 2, 1, 2, 2, 0, 2, 2, 0, 1, 0, 1, 3, 2, 0, 0, 3, 2, 0, 3, 2, 0, 2, 3, 2, 2, 1, 2, 2, 3, 2, 2, 1, 2, 3, 0, 1, 0, 3, 2, 3, 0, 2, 0, 3, 0, 0, 1, 2, 2, 2, 0, 3, 0, 3, 2, 3, 3, 0, 2, 3, 2, 3, 3, 2, 3, 1, 1, 3, 1, 0, 3, 0, 3, 3, 2, 1, 2, 3, 1, 1, 1, 2, 3, 3, 0, 2, 3, 1, 3, 3, 1, 2, 1, 0, 0, 0, 3, 1, 2, 0, 2, 3, 0, 3, 1, 1, 1, 0, 1, 3, 0, 3, 2, 3, 3, 0, 2, 0, 2, 2, 1, 1, 1, 3, 2, 0, 2, 3, 2, 3, 0, 1, 0, 1, 0, 2, 1, 2, 2, 0, 1, 3, 0, 2, 3, 1, 1, 0, 3, 3, 3, 0, 2, 0, 3, 1, 3, 2, 2, 1, 2, 0, 1, 2, 3, 2, 1, 3, 2, 3, 2, 1, 2, 2, 2, 3, 2, 0, 0, 3, 1, 2, 3, 1, 3, 3, 0, 0, 3, 1, 1, 0, 1, 3, 3, 1, 3, 2, 2, 0, 2, 1, 0, 1, 1, 2, 0, 2, 2, 0, 1, 1, 1, 3, 3, 2, 3, 0, 1, 0, 3, 3, 3, 1, 1, 0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 3, 0, 3, 1, 2, 1, 0, 1, 1, 0, 0, 3, 3, 0, 1, 0, 2, 0, 1, 1, 2, 3, 2, 1, 3, 3, 1, 3, 0, 3, 2, 0, 3, 2, 2, 0, 2, 0, 3, 3, 3, 3, 3, 3, 0, 3, 1, 3, 0, 3, 1, 0, 1, 0, 3, 3, 1, 2, 0, 2, 1, 1, 0, 0, 0, 3, 1, 1, 1, 1, 2, 2, 2, 3, 2, 1, 0, 2, 2, 0, 0, 3, 0, 2, 0, 1, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 0, 1, 1, 2, 3, 3, 0, 0, 2, 0, 1, 1, 0, 2, 2, 1, 2, 3, 1, 3, 0, 0, 3, 1, 3, 0, 1, 2, 0, 3, 0, 2, 1, 1, 0, 2, 3, 0, 0, 1, 2, 0, 1, 3, 1, 1, 2, 1, 3, 2, 3, 3, 3, 1, 2, 2, 1, 0, 0, 1, 2, 3, 3, 1, 3, 0, 1, 1, 0, 1, 0, 0, 3, 0, 2, 3, 1, 3, 3, 1, 1, 3, 1, 2, 1, 0, 3, 0, 2, 2, 2, 1, 2, 1, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 1, 3, 2, 2, 0, 3, 1, 0, 2, 3, 1, 2, 2, 2, 1, 1, 1, 1, 2, 3, 3, 2, 1, 2, 2, 3, 2, 0, 3, 3, 2, 2, 2, 1, 0, 2, 0, 2, 0, 0, 1, 0, 3, 1, 0, 2, 0, 3, 3, 3, 1, 3, 2, 0, 2, 3, 0, 1, 1, 0, 3, 1, 0, 0, 0, 2, 0, 3, 2, 1, 1, 0, 3, 1, 3, 1, 3, 2, 1, 3, 2, 3, 3, 0, 2, 1, 3, 1, 1, 0, 0, 3, 3, 1, 0, 0, 2, 1, 0, 3, 0, 2, 3, 1, 2, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 3, 0, 0, 0, 2, 2, 1, 0, 1, 2, 1, 2, 1, 0, 2, 0, 1, 3, 3, 3, 0, 3, 3, 2, 3, 2, 3, 1, 1, 3, 0, 3, 0, 3, 2, 3, 2, 3, 1, 2, 2, 3, 2, 2, 0, 0, 2, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 3, 3, 2, 3, 1, 0, 2, 3, 3, 0, 1, 0, 0, 2, 3, 3, 1, 3, 3, 0, 1, 0, 1, 0, 2, 0, 3, 0, 1, 3, 1, 3, 0, 0, 1, 2, 1, 3, 3, 1, 1, 0, 1, 1, 3, 3, 2, 0, 0, 0, 1, 3, 1, 1, 2, 3, 1, 0, 3, 1, 3, 3, 2, 0, 3, 3, 0, 3, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 3, 0, 0, 1, 3, 3, 3, 2, 1, 1, 2, 1, 3, 3, 0, 2, 2, 2, 1, 0, 1, 2, 1, 2, 1, 3, 2, 0, 3, 3, 2, 1, 0, 1, 1, 0, 0, 1, 0, 2, 3, 0, 3, 2, 1, 0, 3, 1, 2, 3, 3, 3, 2, 3, 3, 1, 1, 1, 0, 2, 0, 0, 3, 1, 1, 1, 2, 2, 2, 1, 0, 2, 1, 0, 3, 1, 2, 2, 0, 2, 3, 1, 2, 3, 3, 0, 1, 3, 2, 3, 2, 0, 0, 3, 3, 2, 1, 2, 0, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1, 0, 2, 1, 2, 1, 0, 1, 3, 2, 0, 3, 0, 1, 0, 0, 1, 0, 0, 1, 3, 1, 2, 0, 2, 3, 0, 2, 2, 1, 3, 0, 3, 0, 1, 3, 0, 3, 3, 3, 2, 0, 1, 2, 2, 0, 2, 2, 2, 2, 2, 0, 1, 0, 2, 3, 2, 0, 0, 0, 1, 0, 3, 1, 3, 1, 0, 2, 2, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 0, 1, 3, 1, 3, 1, 3, 2, 1, 2, 3, 3, 1, 1, 0, 3, 3, 3, 3, 1, 0, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0, 3, 1, 3, 1, 1, 2, 3, 0, 3, 3, 1, 1, 0, 0, 1, 3, 2, 3, 1, 0, 1, 3, 1, 0, 1, 2, 1, 1, 1, 0, 2, 1, 2, 0, 1, 1, 2, 1, 2, 1, 3, 1, 1, 3, 0, 0, 2, 3, 2, 0, 2, 0, 3, 0, 3, 2, 0, 0, 2, 2, 2, 0, 2, 1, 3, 3, 1, 3, 1, 1, 2, 2, 0, 2, 3, 1, 1, 0, 1, 3, 1, 0, 3, 3, 2, 3, 3, 3, 0, 2, 2, 1, 1, 3, 0, 0, 0, 3, 2, 1, 0, 3, 0, 0, 0, 2, 0, 3, 2, 0, 3, 0, 3, 0, 1, 1, 1, 0, 2, 3, 3, 2, 1, 1, 0, 0, 3, 0, 0, 2, 0, 1, 2, 1, 3, 3, 2, 2, 2, 0, 2, 3, 3, 0, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 3, 1, 0, 2, 3, 2, 0, 3, 1, 2, 3, 3, 1, 3, 1, 1, 1, 2, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 2, 2, 1, 3, 3, 3, 1, 1, 3, 1, 0, 3, 3, 0, 0, 0, 3, 2, 0, 3, 3, 3, 0, 1, 0, 1, 2, 2, 0, 2, 2, 0, 2, 0, 3, 1, 1, 0, 3, 0, 0, 3, 0, 3, 0, 1, 3, 3, 1, 2, 0, 2, 0, 3, 3, 0, 2, 2, 0, 2, 2, 3, 0, 3, 3, 0, 2, 0, 2, 2, 0, 3, 0, 1, 3, 2, 3, 1, 3, 1, 2, 1, 0, 1, 2, 2, 1, 0, 0, 1, 2, 1, 3, 0, 0, 3, 0, 2, 2, 3, 0, 0, 2, 0, 0, 2, 2, 1, 2, 3, 3, 3, 0, 1, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 0, 3, 1, 1, 1, 0, 2, 0, 0, 2, 3, 3, 1, 2, 1, 1, 0, 3, 2, 0, 0, 3, 3, 1, 1, 2, 1, 2, 0, 1, 1, 3, 1, 3, 1, 3, 0, 0, 0, 3, 1, 1, 2, 0, 2, 3, 2, 0, 1, 2, 2, 0, 1, 2, 0, 2, 0, 1, 3, 3, 3, 1, 0, 1, 2, 1, 2, 3, 2, 1, 3, 3, 1, 0, 2, 0, 1, 2, 1, 3, 0, 0, 0, 0, 2, 1, 2, 2, 3, 1, 3, 0, 0, 0, 2, 3, 0, 1, 3, 2, 3, 1, 1, 1, 0, 2, 3, 0, 3, 2, 2, 0, 3, 3, 2, 1, 2, 1, 1, 2, 1, 0, 0, 1, 3, 2, 1, 3, 2, 2, 0, 3, 1, 3, 2, 3, 0, 0, 2, 0, 3, 0, 1, 2, 3, 3, 0, 2, 0, 2, 3, 1, 1, 3, 3, 2, 0, 0, 1, 3, 1, 3, 3, 1, 3, 3, 1, 2, 0, 1, 1, 2, 2, 0, 3, 2, 1, 1, 2, 2, 1, 2, 0, 2, 2, 0, 0, 2, 3, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 2, 2, 3, 2, 2, 2, 2, 1, 2, 3, 3, 1, 2, 0, 0, 2, 1, 3, 2, 2, 3, 1, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 1, 3, 3, 1, 3, 3, 3, 0, 0, 0, 0, 3, 2, 3, 2, 0, 2, 2, 1, 3, 3, 3, 0, 1, 3, 1, 1, 3, 3, 3, 2, 0, 1, 0, 3, 3, 1, 2, 0, 3, 0, 0, 3, 2, 0, 1, 2, 1, 3, 0, 3, 0, 3, 3, 0, 2, 1, 3, 0, 1, 0, 2, 0, 0, 3, 2, 3, 2, 2, 1, 2, 3, 1, 3, 3, 3, 3, 1, 1, 3, 1, 3, 3, 2, 1, 0, 3, 2, 0, 1, 2, 0, 1, 2, 3, 2, 2, 3, 2, 0, 0, 3, 2, 3, 2, 0, 2, 0, 1, 1, 3, 1, 2, 1, 0, 3, 2, 3, 3, 3, 1, 2, 1, 2, 2, 2, 0, 2, 3, 1, 1, 1, 3, 1, 0, 2, 2, 3, 1, 3, 1, 3, 1, 1, 3, 2, 0, 2, 2, 1, 2, 3, 1, 3, 0, 0, 2, 3, 3, 0, 0, 1, 3, 3, 3, 2, 3, 0, 3, 0, 0, 0, 1, 2, 2, 1, 1, 2, 3, 1, 2, 0, 1, 1, 0, 1, 1, 2, 2, 3, 3, 2, 1, 1, 0, 2, 0, 1, 0, 0, 2, 2, 2, 2, 0, 2, 0, 3, 3, 2, 3, 1, 0, 3, 0, 0, 3, 3, 2, 0, 0, 3, 0, 1, 2, 1, 0, 0, 0, 0, 2, 3, 3, 1, 3, 0, 0, 1, 1, 1, 1, 2, 2, 0, 2, 0, 0, 3, 1, 1, 2, 1, 0, 1, 0, 3, 3, 3, 2, 1, 2, 2, 0, 1, 3, 3, 3, 2, 0, 0, 3, 3, 3, 2, 0, 2, 3, 0, 0, 2, 0, 1, 2, 0, 2, 0, 3, 1, 0, 2, 2, 1, 3, 3, 2, 2, 3, 0, 2, 1, 2, 2, 0, 3, 1, 2, 2, 1, 1, 3, 1, 2, 3, 2, 2, 3, 3, 1, 3, 0, 3, 3, 3, 2, 0, 0, 1, 2, 2, 2, 1, 2, 1, 1, 3, 2, 3, 2, 1, 3, 3, 1, 1, 3, 0, 1, 2, 2, 2, 2, 0, 0, 1, 3, 1, 1, 1, 3, 3, 2, 0, 2, 3, 3, 1, 1, 3, 2, 1, 0, 0, 2, 0, 0, 2, 1, 0, 3, 2, 1, 3, 2, 2, 2, 3, 2, 3, 3, 3, 2, 2, 3, 1, 1, 3, 3, 3, 1, 3, 1, 3, 2, 1, 3, 3, 0, 3, 1, 2, 3, 3, 3, 3, 3, 0, 2, 1, 3, 0, 2, 2, 0, 3, 3, 1, 2, 3, 3, 3, 2, 0, 0, 2, 1, 2, 3, 0, 2, 3, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 0, 2, 1, 1, 3, 0, 3, 0, 2, 1, 1, 1, 2, 0, 0, 0, 2, 0, 1, 2, 1, 3, 0, 3, 0, 3, 1, 0, 0, 1, 3, 0, 0, 2, 1, 2, 1, 0, 1, 1, 0, 0, 0, 2, 0, 0, 3, 3, 0, 1, 3, 0, 0, 1, 2, 1, 3, 3, 1, 1, 2, 0, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 1, 1, 0, 1, 1, 3, 0, 1, 0, 0, 1, 2, 2, 2, 0, 1, 2, 1, 0, 3, 0, 1, 0, 0, 3, 2, 3, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 3, 1, 2, 0, 1, 3, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 0, 3, 2, 2, 0, 2, 1, 0, 0, 0, 2, 2, 1, 0, 1, 0, 2, 0, 2, 0, 3, 0, 1, 2, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 0, 3, 2, 0, 0, 3, 3, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 0, 1, 1, 1, 1, 2, 0, 1, 0, 2, 1, 3, 2, 3, 1, 1, 0, 3, 1, 3, 0, 1, 0, 3, 1, 0, 1, 2, 2, 1, 1, 0, 3, 1, 1, 3, 2, 1, 2, 1, 0, 1, 3, 2, 1, 2, 1, 1, 3, 2, 0, 3, 0, 1, 0, 3, 1, 1, 2, 0, 0, 2, 0, 0, 2, 3, 3, 2, 0, 2, 3, 1, 1, 0, 3, 2, 1, 2, 1, 0, 3, 2, 3, 0, 1, 2, 3, 1, 2, 3, 0, 2, 1, 2, 0, 3, 2, 3, 2, 1, 2, 0, 2, 2, 3, 0, 3, 3, 2, 0, 1, 0, 2, 3, 2, 3, 0, 3, 2, 2, 3, 1, 0, 1, 3, 2, 2, 0, 2, 3, 2, 2, 2, 2, 1, 1, 3, 0, 2, 2, 0, 0, 1, 3, 1, 0, 3, 0, 3, 1, 0, 0, 2, 2, 2, 1, 2, 3, 2, 3, 2, 2, 2, 3, 3, 1, 2, 3, 2, 0, 2, 2, 3, 3, 2, 2, 0, 3, 0, 3, 1, 2, 0, 3, 0, 0, 1, 3, 3, 3, 3, 2, 1, 0, 3, 2, 2, 2, 2, 3, 1, 1, 1, 2, 2, 2, 3, 3, 0, 2, 0, 3, 0, 3, 0, 3, 2, 3, 2, 1, 2, 3, 0, 0, 2, 0, 2, 2, 2, 0, 1, 0, 3, 0, 0, 1, 1, 2, 0, 1, 0, 2, 3, 1, 3, 0, 1, 1, 2, 2, 0, 1, 2, 2, 3, 2, 3, 0, 3, 1, 3, 3, 2, 2, 0, 1, 1, 0, 2, 1, 2, 2, 0, 0, 0, 3, 2, 2, 3, 3, 1, 3, 0, 1, 2, 0, 2, 2, 2, 3, 2, 1, 3, 1, 2, 3, 1, 2, 3, 2, 3, 3, 1, 3, 3, 3, 3, 2, 3, 0, 3, 1, 1, 1, 0, 2, 3, 3, 2, 3, 1, 2, 0, 2, 3, 2, 0, 1, 2, 1, 3, 1, 3, 2, 0, 2, 1, 3, 0, 2, 1, 3, 3, 3, 3, 0, 2, 2, 1, 3, 1, 0, 0, 2, 1, 1, 1, 3, 0, 1, 1, 2, 2, 2, 0, 1, 2, 1, 0, 2, 2, 0, 3, 1, 1, 1, 2, 0, 1, 1, 2, 3, 3, 1, 1, 1, 2, 0, 3, 0, 3, 3, 0, 3, 1, 2, 3, 0, 2, 3, 3, 3, 2, 0, 0, 0, 2, 3, 2, 3, 2, 2, 2, 0, 3, 2, 1, 0, 0, 0, 2, 3, 1, 3, 1, 3, 1, 3, 2, 3, 1, 1, 3, 1, 2, 1, 2, 0, 3, 2, 0, 0, 1, 1, 3, 0, 2, 1, 2, 2, 2, 1, 2, 2, 3, 0, 2, 1, 0, 0, 2, 0, 2, 0, 3, 0, 1, 2, 1, 3, 2, 1, 3, 1, 2, 0, 1, 2, 2, 3, 3, 1, 2, 0, 0, 0, 3, 0, 2, 1, 0, 0, 0, 3, 2, 0, 3, 0, 2, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 3, 2, 0, 1, 1, 0, 0, 2, 1, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 0, 2, 1, 1, 2, 2, 0, 1, 3, 2, 3, 1, 1, 2, 3, 3, 3, 3, 1, 0, 2, 2, 3, 2, 0, 1, 3, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 0, 2, 0, 2, 2, 3, 0, 0, 3, 0, 2, 3, 3, 0, 0, 0, 3, 0, 1, 0, 0, 0, 1, 1, 1, 3, 3, 3, 2, 3, 2, 1, 2, 2, 1, 1, 1, 0, 2, 2, 2, 1, 2, 3, 2, 0, 0, 0, 2, 1, 0, 1, 3, 3, 2, 3, 3, 3, 0, 0, 2, 1, 2, 1, 1, 0, 3, 1, 2, 3, 1, 0, 3, 3, 2, 2, 1, 0, 1, 0, 3, 0, 2, 0, 3, 2, 3, 0, 2, 1, 0, 2, 3, 0, 1, 3, 0, 2, 0, 1, 2, 3, 2, 0, 2, 1, 2, 2, 0, 0, 2, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 3, 2, 2, 3, 3, 0, 2, 0, 0, 3, 1, 3, 1, 0, 3, 1, 3, 3, 0, 2, 0, 3, 3, 2, 1, 1, 0, 2, 1, 3, 3, 2, 0, 1, 0, 0, 0, 2, 1, 1, 1, 0, 2, 0, 2, 3, 0, 0, 0, 3, 2, 0, 0, 0, 2, 3, 1, 1, 3, 1, 0, 1, 0, 3, 2, 3, 0, 1, 1, 0, 3, 3, 1, 1, 3, 1, 1, 2, 1, 0, 3, 0, 1, 1, 1, 3, 0, 1, 1, 1, 3, 0, 2, 3, 0, 0, 3, 3, 3, 2, 3, 2, 2, 3, 1, 1, 1, 0, 2, 3, 2, 1, 2, 0, 2, 0, 1, 3, 3, 0, 2, 0, 2, 2, 2, 0, 3, 3, 0, 1, 2, 3, 2, 0, 0, 0, 1, 1, 2, 2, 3, 2, 1, 2, 0, 2, 2, 0, 0, 0, 3, 1, 0, 2, 3, 2, 1, 0, 0, 0, 1, 0, 2, 1, 3, 0, 1, 0, 0, 1, 2, 1, 3, 1, 3, 1, 1, 3, 0, 3, 2, 0, 3, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 2, 1, 2, 3, 0, 2, 2, 2, 3, 0, 3, 1, 0, 0, 0, 1, 0, 3, 1, 0, 1, 1, 3, 0, 1, 1, 3, 0, 1, 2, 1, 1, 0, 3, 3, 2, 1, 2, 1, 0, 2, 1, 3, 1, 1, 3, 1, 0, 2, 0, 1, 3, 1, 1, 2, 2, 2, 2, 1, 3, 2, 3, 2, 1, 2, 1, 3, 3, 0, 0, 3, 3, 1, 2, 1, 0, 1, 2, 2, 2, 0, 0, 3, 3, 1, 1, 0, 1, 0, 3, 3, 2, 0, 3, 2, 2, 2, 2, 1, 3, 3, 3, 1, 1, 2, 0, 1, 0, 3, 0, 3, 1, 0, 1, 1, 0, 0, 1, 3, 0, 1, 1, 3, 0, 0, 1, 3, 0, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 0, 3, 2, 3, 3, 1, 2, 2, 2, 2, 2, 0, 0, 2, 1, 0, 0, 2, 2, 1, 3, 0, 1, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 1, 3, 0, 2, 1, 3, 0, 2, 0, 3, 0, 2, 3, 3, 0, 0, 1, 0, 3, 3, 1, 1, 0, 3, 0, 3, 3, 1, 3, 1, 2, 3, 3, 1, 1, 0, 1, 2, 3, 2, 3, 1, 0, 0, 2, 2, 0, 3, 3, 3, 2, 3, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 2, 0, 0, 3, 3, 2, 3, 1, 1, 0, 2, 2, 3, 3, 0, 0, 2, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 0, 2, 0, 1, 0, 1, 2, 2, 3, 0, 2, 0, 2, 2, 0, 3, 3, 1, 2, 2, 2, 1, 2, 2, 3, 3, 1, 2, 1, 1, 1, 3, 3, 1, 0, 3, 3, 1, 3, 2, 0, 0, 3, 1, 0, 1, 2, 1, 0, 3, 0, 1, 3, 0, 3, 1, 0, 0, 2, 3, 0, 1, 3, 3, 3, 1, 1, 0, 3, 0, 3, 0, 3, 3, 0, 1, 2, 3, 0, 1, 1, 3, 2, 3, 2, 0, 1, 0, 0, 1, 3, 2, 2, 0, 3, 3, 1, 1, 1, 2, 2, 0, 2, 0, 0, 3, 2, 2, 3, 3, 0, 2, 2, 2, 0, 2, 0, 3, 0, 2, 2, 2, 2, 2, 1, 2, 1, 3, 2, 1, 2, 1, 1, 1, 3, 0, 2, 0, 0, 2, 3, 3, 3, 2, 1, 1, 2, 1, 2, 1, 2, 3, 2, 0, 2, 3, 0, 1, 2, 3, 2, 3, 0, 3, 0, 1, 2, 0, 1, 2, 1, 0, 2, 0, 2, 3, 1, 1, 1, 1, 1, 2, 2, 0, 2, 3, 1, 3, 0, 2, 3, 0, 1, 2, 2, 1, 3, 3, 3, 1, 1, 3, 0, 2, 2, 0, 0, 0, 3, 2, 2, 0, 1, 3, 2, 3, 3, 2, 3, 3, 3, 2, 2, 2, 1, 0, 2, 0, 3, 0, 3, 0, 3, 3, 2, 1, 2, 0, 1, 2, 1, 0, 0, 2, 1, 0, 2, 3, 3, 0, 3, 0, 2, 0, 1, 2, 2, 0, 1, 2, 3, 3, 3, 2, 1, 1, 2, 0, 3, 0, 0, 3, 1, 3, 0, 3, 0, 2, 3, 1, 0, 1, 2, 1, 3, 3, 3, 2, 0, 2, 2, 1, 2, 0, 3, 1, 1, 2, 2, 1, 2, 3, 0, 2, 0, 1, 2, 3, 0, 2, 1, 0, 3, 2, 2, 2, 0, 2, 0, 0, 3, 0, 3, 3, 0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 1, 1, 2, 0, 3, 1, 3, 2, 1, 0, 3, 1, 0, 2, 2, 2, 1, 2, 0, 2, 0, 1, 1, 2, 3, 3, 2, 1, 3, 2, 1, 1, 0, 1, 3, 2, 2, 3, 2, 3, 0, 3, 2, 3, 1, 1, 3, 1, 0, 3, 3, 2, 3, 0, 2, 2, 0, 3, 3, 2, 0, 3, 3, 3, 2, 3, 3, 3, 2, 0, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 3, 0, 1, 3, 3, 1, 3, 3, 0, 0, 1, 2, 0, 3, 2, 2, 3, 3, 1, 3, 3, 1, 0, 3, 0, 3, 2, 0, 1, 1, 1, 2, 0, 3, 0, 3, 0, 2, 2, 1, 1, 0, 3, 0, 2, 1, 1, 1, 1, 1, 3, 1, 0, 0, 2, 1, 3, 3, 0, 2, 3, 1, 0, 1, 0, 3, 3, 3, 3, 0, 3, 3, 1, 0, 3, 2, 0, 3, 2, 2, 2, 3, 0, 2, 0, 3, 2, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3, 0, 0, 0, 2, 2, 3, 2, 0, 0, 0, 1, 2, 0, 0, 0, 1, 3, 2, 3, 3, 1, 2, 1, 2, 3, 3, 2, 1, 3, 2, 0, 3, 3, 2, 3, 3, 2, 1, 2, 1, 3, 0, 1, 2, 0, 1, 0, 2, 0, 3, 1, 0, 2, 3, 2, 3, 0, 2, 3, 3, 3, 0, 0, 1, 1, 0, 2, 2, 2, 3, 0, 2, 3, 1, 1, 3, 0, 3, 0, 1, 0, 0, 2, 2, 2, 3, 3, 1, 3, 0, 1, 2, 2, 0, 3, 1, 1, 0, 3, 3, 0, 1, 3, 0, 2, 3, 1, 2, 1, 0, 0, 2, 1, 1, 3, 0, 0, 3, 3, 2, 2, 2, 1, 3, 3, 0, 2, 3, 3, 2, 1, 2, 0, 2, 1, 2, 1, 0, 2, 2, 0, 0, 2, 2, 0, 2, 1, 3, 0, 0, 1, 0, 3, 1, 1, 3, 2, 1, 0, 3, 2, 2, 2, 1, 0, 3, 3, 1, 0, 0, 2, 3, 0, 3, 1, 0, 0, 1, 3, 0, 1, 3, 0, 0, 1, 0, 2, 3, 2, 0, 3, 2, 2, 3, 1, 1, 0, 2, 1, 2, 1, 3, 2, 0, 3, 0, 3, 2, 3, 1, 1, 0, 0, 3, 1, 3, 1, 3, 1, 2, 0, 1, 3, 0, 0, 1, 0, 2, 2, 0, 2, 0, 1, 1, 3, 2, 2, 3, 3, 3, 1, 1, 2, 0, 3, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 1, 2, 3, 0, 2, 3, 2, 3, 1, 0, 0, 3, 3, 2, 3, 3, 1, 3, 2, 2, 2, 3, 2, 0, 0, 0, 0, 2, 3, 0, 2, 0, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 1, 2, 3, 3, 3, 0, 3, 0, 3, 1, 2, 3, 0, 3, 0, 2, 3, 0, 1, 3, 2, 2, 0, 0, 2, 2, 3, 2, 2, 2, 1, 3, 2, 0, 1, 1, 0, 3, 2, 0, 2, 3, 2, 1, 3, 1, 1, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 1, 3, 0, 2, 1, 2, 2, 3, 2, 2, 3, 2, 1, 0, 3, 2, 1, 0, 0, 1, 3, 2, 0, 2, 2, 3, 2, 3, 1, 2, 3, 1, 1, 2, 1, 0, 3, 0, 2, 2, 0, 2, 1, 2, 2, 0, 2, 1, 1, 1, 3, 3, 1, 3, 3, 2, 2, 3, 1, 3, 3, 0, 2, 1, 0, 0, 2, 1, 3, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 0, 0, 1, 3, 3, 3, 1, 2, 3, 2, 1, 2, 0, 1, 0, 3, 1, 0, 1, 3, 1, 0, 3, 0, 3, 2, 1, 1, 2, 1, 3, 3, 3, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 0, 3, 1, 0, 0, 2, 2, 3, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 0, 1, 0, 3, 3, 0, 0, 0, 3, 3, 2, 1, 1, 0, 0, 1, 2, 1, 0, 2, 1, 2, 3, 2, 1, 3, 3, 3, 1, 3, 0, 3, 0, 2, 1, 0, 3, 0, 1, 3, 2, 2, 2, 2, 3, 2, 3, 3, 3, 0, 1, 1, 3, 1, 3, 2, 1, 2, 0, 1, 0, 1, 0, 0, 1, 3, 3, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 2, 0, 2, 2, 1, 0, 1, 0, 3, 2, 3, 3, 3, 2, 2, 0, 2, 0, 2, 0, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 2, 3, 2, 3, 3, 0, 0, 1, 0, 1, 3, 3, 0, 1, 0, 3, 0, 3, 2, 0, 2, 3, 1, 1, 1, 1, 3, 2, 2, 0, 3, 0, 3, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 2, 0, 0, 0, 2, 3, 1, 1, 2, 3, 3, 1, 3, 3, 1, 0, 3, 2, 2, 1, 0, 2, 0, 1, 3, 1, 2, 1, 3, 1, 1, 1, 3, 2, 2, 1, 0, 3, 2, 1, 0, 2, 0, 2, 2, 3, 1, 3, 0, 3, 3, 2, 2, 3, 2, 1]


✨ 2. Now, let's create a random query value for row and column.
✨ query_row: 5, query_col: 5

✨ 3. Let's create a query message vector, of size m, that is 1 at the query column and 0 elsewhere.
✨ query vector: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

✨ 4. Let's encrypt the query message vector, calculating A and e.
✨ The encrypted query vector is: 
Rows: 100
Cols: 1
Vector: [312, 175, 328, 381, 687, 681, 136, 814, 785, 441, 867, 601, 857, 961, 404, 209, 2, 555, 648, 437, 589, 391, 592, 318, 340, 94, 460, 981, 359, 968, 941, 171, 346, 812, 402, 413, 697, 278, 534, 808, 616, 606, 273, 849, 857, 198, 221, 81, 720, 890, 213, 364, 481, 93, 219, 324, 657, 391, 860, 865, 663, 194, 660, 298, 1, 677, 346, 164, 509, 564, 854, 1, 295, 197, 811, 175, 874, 944, 140, 641, 417, 379, 569, 532, 229, 934, 914, 889, 287, 134, 14, 360, 377, 728, 223, 335, 272, 24, 293, 777]


✨ 5. We scale the query vector by delta=mod/p and db vector to 1/p
✨ scaled_query: 
Rows: 100
Cols: 1
Vector: [0, 750, 0, 250, 750, 250, 0, 500, 250, 250, 750, 250, 250, 250, 0, 250, 500, 750, 0, 250, 250, 750, 0, 500, 0, 500, 0, 250, 750, 0, 250, 750, 500, 0, 500, 250, 250, 500, 500, 0, 0, 500, 250, 250, 250, 500, 250, 250, 0, 500, 250, 0, 250, 250, 750, 0, 250, 750, 0, 250, 750, 500, 0, 500, 250, 250, 500, 0, 250, 0, 500, 250, 750, 250, 750, 750, 500, 0, 0, 250, 250, 750, 250, 0, 250, 500, 500, 250, 750, 500, 500, 0, 250, 0, 750, 750, 0, 0, 250, 250]

✨ scaled_db: 
Rows: 100
Cols: 100
Vector: [1, 1, 1, 2, 0, 3, 1, 3, 2, 2, 3, 2, 1, 1, 1, 1, 2, 0, 3, 2, 1, 0, 1, 2, 1, 3, 2, 0, 0, 1, 1, 0, 2, 2, 3, 3, 3, 0, 0, 0, 3, 1, 2, 0, 3, 3, 0, 2, 2, 2, 3, 3, 3, 1, 0, 3, 1, 3, 1, 3, 1, 1, 0, 3, 0, 1, 1, 2, 2, 3, 0, 1, 1, 0, 2, 3, 0, 3, 3, 1, 0, 3, 0, 3, 1, 1, 0, 3, 3, 2, 2, 1, 1, 1, 3, 2, 2, 3, 3, 1, 1, 3, 1, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 2, 1, 2, 1, 0, 0, 1, 3, 0, 2, 3, 0, 2, 0, 2, 1, 1, 1, 2, 1, 1, 3, 1, 1, 0, 1, 3, 2, 1, 3, 2, 3, 0, 2, 3, 0, 0, 1, 3, 3, 2, 0, 1, 0, 2, 0, 3, 2, 0, 0, 1, 0, 1, 1, 1, 2, 0, 2, 1, 2, 1, 3, 3, 1, 3, 0, 3, 2, 0, 2, 0, 3, 2, 0, 2, 3, 2, 1, 0, 3, 1, 0, 2, 1, 3, 0, 3, 1, 1, 2, 0, 3, 1, 3, 1, 0, 1, 2, 1, 3, 1, 2, 3, 3, 3, 2, 3, 0, 3, 3, 1, 1, 0, 2, 0, 2, 3, 2, 0, 3, 3, 1, 3, 1, 2, 0, 3, 2, 3, 3, 1, 1, 2, 0, 1, 2, 1, 1, 0, 3, 0, 2, 0, 0, 1, 0, 2, 0, 0, 2, 2, 0, 1, 1, 0, 2, 0, 0, 1, 1, 0, 3, 3, 2, 1, 3, 2, 1, 3, 0, 2, 3, 3, 3, 0, 3, 1, 1, 3, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 3, 3, 2, 1, 1, 0, 2, 3, 3, 2, 1, 3, 2, 0, 2, 3, 1, 2, 3, 3, 0, 3, 3, 2, 1, 1, 1, 3, 1, 2, 3, 2, 3, 1, 1, 3, 2, 2, 2, 3, 0, 0, 0, 3, 0, 1, 0, 2, 0, 2, 3, 3, 3, 0, 3, 2, 1, 3, 2, 1, 0, 0, 3, 1, 2, 3, 0, 1, 2, 0, 3, 3, 1, 3, 3, 3, 1, 1, 2, 3, 3, 3, 1, 0, 3, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 3, 3, 3, 2, 2, 0, 0, 2, 1, 0, 3, 2, 2, 2, 0, 3, 2, 3, 0, 0, 3, 3, 1, 2, 1, 3, 3, 1, 1, 0, 3, 3, 2, 2, 3, 2, 2, 1, 0, 3, 1, 3, 0, 2, 1, 2, 3, 3, 3, 1, 1, 3, 0, 3, 1, 2, 1, 0, 1, 3, 2, 3, 0, 3, 3, 1, 2, 2, 1, 1, 3, 2, 0, 1, 1, 1, 2, 2, 3, 3, 0, 0, 0, 1, 0, 1, 1, 3, 1, 2, 0, 2, 2, 2, 3, 0, 1, 2, 3, 3, 2, 3, 0, 2, 2, 2, 0, 0, 1, 2, 1, 3, 3, 2, 1, 2, 3, 0, 3, 2, 1, 0, 2, 2, 2, 0, 0, 2, 0, 0, 3, 2, 3, 3, 0, 0, 3, 3, 0, 1, 3, 1, 0, 0, 3, 3, 1, 2, 3, 2, 0, 3, 1, 3, 3, 0, 1, 3, 2, 1, 2, 1, 1, 0, 0, 3, 3, 2, 1, 2, 1, 2, 0, 2, 2, 2, 3, 2, 1, 3, 2, 2, 2, 3, 2, 2, 2, 1, 0, 2, 3, 0, 3, 0, 1, 2, 3, 1, 2, 3, 0, 0, 3, 3, 0, 1, 0, 3, 1, 0, 1, 1, 2, 0, 3, 3, 0, 0, 3, 1, 0, 2, 0, 1, 3, 0, 1, 3, 2, 2, 0, 0, 0, 1, 1, 3, 3, 0, 3, 1, 2, 1, 0, 0, 2, 0, 3, 1, 3, 1, 3, 3, 1, 3, 3, 0, 1, 2, 1, 2, 2, 1, 0, 0, 1, 3, 1, 0, 2, 2, 0, 2, 3, 1, 1, 2, 1, 0, 1, 3, 1, 1, 1, 3, 3, 1, 1, 2, 0, 3, 1, 1, 2, 0, 3, 2, 2, 1, 3, 3, 1, 0, 1, 1, 3, 3, 0, 1, 0, 3, 3, 0, 3, 3, 3, 3, 1, 2, 1, 1, 3, 3, 2, 3, 2, 0, 0, 1, 3, 0, 3, 3, 2, 2, 2, 1, 3, 2, 3, 1, 1, 2, 2, 2, 3, 2, 1, 0, 2, 2, 2, 3, 2, 0, 0, 1, 0, 1, 2, 1, 3, 1, 2, 2, 3, 3, 3, 0, 0, 1, 3, 1, 2, 0, 3, 2, 1, 2, 0, 1, 0, 3, 2, 0, 1, 1, 3, 1, 2, 3, 3, 0, 2, 2, 0, 2, 1, 3, 1, 2, 0, 0, 2, 2, 3, 3, 3, 3, 0, 3, 0, 1, 0, 1, 2, 0, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 3, 2, 1, 3, 2, 0, 3, 1, 2, 0, 0, 1, 1, 0, 3, 2, 2, 0, 1, 0, 2, 2, 0, 1, 0, 1, 1, 3, 0, 0, 1, 2, 1, 2, 1, 1, 1, 3, 2, 0, 0, 2, 3, 0, 2, 3, 2, 0, 3, 1, 1, 0, 1, 3, 0, 1, 3, 3, 3, 0, 3, 3, 3, 1, 3, 0, 1, 0, 0, 3, 0, 3, 2, 2, 2, 1, 2, 0, 1, 2, 1, 3, 2, 1, 3, 1, 3, 1, 0, 3, 0, 0, 1, 2, 3, 3, 2, 0, 0, 0, 0, 3, 1, 3, 0, 1, 3, 3, 2, 0, 3, 1, 1, 3, 1, 2, 0, 2, 2, 0, 1, 1, 0, 3, 1, 2, 3, 2, 2, 0, 2, 1, 0, 0, 0, 0, 2, 3, 1, 1, 3, 1, 3, 2, 0, 3, 1, 0, 3, 1, 0, 2, 2, 2, 3, 0, 3, 0, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 1, 2, 0, 3, 3, 0, 1, 2, 2, 2, 1, 0, 0, 3, 3, 2, 2, 3, 1, 1, 2, 3, 0, 0, 0, 3, 0, 0, 2, 3, 1, 0, 2, 0, 2, 0, 2, 0, 1, 1, 2, 3, 0, 2, 0, 0, 1, 1, 2, 1, 0, 3, 0, 3, 1, 1, 2, 3, 1, 3, 0, 1, 1, 0, 1, 1, 3, 1, 3, 0, 3, 3, 0, 3, 1, 2, 1, 0, 3, 1, 3, 3, 0, 0, 2, 0, 3, 2, 3, 3, 3, 3, 1, 2, 3, 3, 1, 3, 3, 3, 0, 1, 1, 0, 3, 0, 3, 0, 0, 2, 2, 1, 0, 3, 0, 1, 0, 2, 0, 3, 2, 1, 2, 2, 1, 2, 0, 0, 0, 2, 1, 2, 3, 3, 1, 1, 3, 1, 0, 3, 1, 0, 2, 2, 3, 2, 3, 3, 1, 0, 0, 0, 0, 3, 2, 3, 0, 2, 2, 3, 3, 1, 1, 2, 0, 1, 2, 3, 1, 3, 2, 0, 2, 3, 3, 1, 0, 1, 2, 1, 1, 3, 0, 1, 0, 1, 2, 1, 0, 2, 0, 2, 1, 2, 1, 1, 1, 2, 3, 3, 2, 0, 2, 1, 0, 0, 1, 3, 2, 2, 1, 3, 3, 0, 0, 1, 2, 0, 2, 2, 0, 0, 0, 3, 3, 3, 0, 2, 3, 2, 3, 0, 3, 3, 3, 0, 3, 0, 3, 3, 1, 3, 1, 0, 3, 3, 0, 3, 1, 0, 3, 3, 2, 2, 3, 1, 3, 2, 0, 1, 1, 0, 3, 1, 0, 0, 3, 1, 3, 2, 3, 2, 1, 0, 3, 3, 1, 2, 3, 2, 0, 3, 2, 3, 3, 0, 3, 2, 2, 3, 1, 1, 0, 2, 2, 0, 2, 2, 0, 2, 2, 2, 1, 1, 3, 2, 3, 2, 3, 2, 1, 0, 2, 0, 1, 1, 3, 2, 0, 0, 0, 1, 0, 3, 2, 3, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 3, 0, 1, 1, 1, 0, 2, 2, 1, 0, 2, 2, 2, 2, 3, 0, 3, 3, 0, 3, 2, 0, 2, 3, 1, 1, 3, 2, 3, 2, 3, 1, 0, 0, 3, 1, 0, 3, 1, 1, 2, 0, 0, 3, 2, 0, 0, 1, 0, 3, 3, 2, 2, 3, 1, 3, 2, 1, 3, 2, 2, 2, 0, 3, 0, 1, 0, 3, 3, 0, 0, 3, 3, 3, 0, 2, 3, 3, 1, 1, 3, 1, 2, 1, 2, 2, 0, 0, 1, 0, 1, 2, 2, 0, 2, 2, 3, 0, 3, 2, 2, 3, 1, 0, 0, 0, 0, 0, 1, 1, 3, 2, 2, 1, 1, 2, 3, 0, 2, 1, 3, 0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 1, 0, 3, 2, 2, 2, 2, 0, 0, 1, 1, 2, 0, 1, 0, 1, 0, 0, 0, 3, 3, 2, 1, 1, 2, 0, 3, 1, 0, 0, 3, 1, 1, 0, 0, 2, 1, 0, 0, 1, 3, 2, 1, 2, 1, 1, 3, 2, 3, 3, 0, 2, 2, 2, 2, 1, 2, 3, 0, 0, 3, 0, 2, 1, 3, 2, 1, 3, 3, 1, 3, 3, 2, 2, 3, 0, 1, 0, 2, 1, 3, 0, 2, 0, 1, 0, 0, 3, 3, 0, 3, 1, 1, 1, 0, 1, 0, 2, 0, 1, 1, 2, 0, 0, 1, 0, 1, 0, 0, 2, 3, 0, 3, 2, 0, 2, 2, 1, 1, 3, 1, 2, 1, 0, 2, 0, 3, 3, 3, 2, 0, 1, 3, 0, 3, 3, 2, 3, 0, 1, 3, 3, 1, 1, 1, 3, 3, 3, 2, 1, 3, 2, 0, 0, 2, 2, 2, 0, 0, 2, 1, 1, 2, 3, 3, 1, 0, 0, 3, 2, 1, 0, 2, 2, 3, 2, 1, 3, 0, 1, 2, 3, 2, 3, 0, 1, 0, 1, 1, 0, 1, 2, 2, 3, 1, 0, 3, 3, 1, 0, 2, 0, 2, 2, 0, 3, 0, 0, 0, 2, 2, 1, 1, 2, 0, 3, 1, 2, 0, 2, 0, 2, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 2, 3, 0, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 2, 3, 3, 1, 2, 2, 2, 2, 0, 3, 2, 2, 0, 1, 1, 2, 3, 1, 2, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 2, 1, 0, 3, 2, 0, 2, 3, 1, 2, 0, 0, 3, 3, 0, 0, 3, 3, 1, 0, 3, 2, 2, 1, 2, 0, 1, 3, 1, 1, 3, 0, 3, 1, 3, 0, 3, 0, 1, 3, 0, 0, 0, 0, 2, 3, 3, 1, 3, 0, 1, 0, 1, 3, 2, 2, 1, 0, 1, 2, 2, 1, 2, 1, 1, 3, 3, 0, 1, 0, 3, 1, 2, 2, 2, 0, 3, 3, 3, 3, 0, 3, 2, 2, 2, 3, 3, 1, 1, 3, 2, 3, 3, 0, 1, 3, 1, 1, 3, 2, 0, 1, 3, 2, 1, 2, 1, 2, 0, 0, 3, 1, 0, 2, 2, 1, 2, 0, 3, 2, 0, 1, 1, 2, 2, 3, 3, 1, 2, 3, 1, 2, 0, 2, 0, 3, 2, 1, 2, 3, 3, 0, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 0, 1, 2, 1, 1, 3, 3, 3, 2, 3, 2, 1, 0, 2, 0, 2, 3, 1, 1, 0, 2, 0, 2, 1, 1, 0, 3, 1, 2, 2, 3, 2, 2, 2, 1, 2, 2, 1, 2, 2, 3, 1, 3, 0, 2, 3, 2, 1, 1, 1, 0, 0, 1, 1, 0, 3, 0, 2, 2, 1, 3, 2, 1, 2, 0, 3, 3, 2, 3, 3, 3, 2, 0, 2, 3, 2, 2, 1, 1, 3, 3, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 0, 2, 1, 3, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 0, 1, 2, 3, 2, 2, 3, 0, 1, 1, 1, 0, 0, 0, 2, 0, 3, 0, 1, 3, 2, 2, 2, 0, 2, 3, 0, 2, 1, 1, 0, 0, 1, 3, 2, 2, 3, 3, 2, 3, 2, 2, 1, 3, 0, 1, 1, 2, 2, 3, 3, 0, 1, 2, 0, 3, 2, 3, 3, 1, 1, 0, 2, 0, 2, 0, 0, 0, 3, 3, 1, 2, 1, 1, 0, 0, 1, 0, 2, 3, 3, 2, 0, 0, 1, 1, 0, 2, 1, 3, 2, 0, 1, 3, 0, 0, 1, 0, 3, 1, 0, 0, 1, 0, 3, 2, 1, 0, 2, 2, 0, 2, 3, 0, 0, 1, 3, 0, 0, 0, 2, 1, 0, 2, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0, 3, 2, 0, 1, 1, 2, 3, 0, 1, 2, 3, 3, 3, 1, 0, 2, 3, 1, 2, 1, 1, 3, 0, 3, 2, 3, 1, 1, 3, 3, 0, 2, 0, 2, 0, 0, 3, 2, 1, 0, 3, 1, 3, 2, 3, 1, 0, 2, 2, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0, 3, 3, 0, 2, 3, 0, 3, 2, 0, 3, 2, 3, 1, 2, 1, 1, 0, 0, 1, 2, 1, 2, 0, 0, 0, 2, 2, 0, 2, 0, 2, 3, 3, 1, 1, 1, 1, 0, 0, 3, 0, 3, 0, 1, 3, 2, 2, 2, 3, 0, 3, 1, 1, 1, 1, 1, 1, 0, 3, 2, 1, 2, 2, 0, 2, 0, 1, 2, 1, 1, 2, 2, 1, 2, 0, 3, 0, 0, 3, 2, 2, 0, 2, 0, 1, 1, 0, 3, 2, 3, 3, 1, 2, 1, 2, 3, 3, 1, 0, 1, 2, 3, 3, 3, 1, 1, 2, 3, 1, 3, 1, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 2, 2, 3, 1, 2, 0, 2, 1, 3, 1, 3, 2, 0, 3, 1, 1, 3, 1, 1, 3, 1, 2, 3, 0, 2, 3, 2, 0, 2, 0, 1, 2, 3, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1, 0, 0, 0, 3, 3, 1, 2, 3, 0, 2, 3, 0, 0, 1, 3, 2, 0, 1, 2, 3, 2, 0, 3, 0, 1, 2, 1, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 3, 2, 3, 1, 0, 3, 1, 2, 0, 2, 3, 0, 3, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 3, 0, 0, 2, 1, 3, 3, 1, 3, 2, 1, 3, 0, 0, 0, 1, 3, 0, 2, 0, 2, 2, 1, 3, 2, 2, 1, 0, 1, 0, 1, 1, 1, 1, 2, 0, 1, 3, 0, 3, 1, 0, 2, 2, 3, 1, 3, 3, 0, 3, 0, 2, 0, 3, 2, 1, 2, 2, 3, 2, 0, 1, 2, 3, 1, 1, 2, 3, 2, 3, 1, 0, 3, 2, 0, 0, 3, 3, 0, 2, 2, 2, 1, 2, 2, 0, 2, 0, 0, 2, 1, 1, 0, 1, 2, 0, 0, 3, 2, 3, 0, 2, 1, 3, 3, 0, 1, 1, 1, 1, 3, 3, 2, 0, 2, 0, 0, 0, 1, 3, 2, 2, 0, 0, 0, 0, 2, 0, 0, 1, 3, 0, 3, 0, 0, 3, 0, 2, 2, 3, 3, 3, 3, 1, 0, 0, 3, 2, 0, 3, 0, 1, 1, 3, 3, 2, 1, 2, 0, 2, 1, 0, 0, 3, 1, 2, 2, 2, 2, 1, 3, 2, 0, 3, 2, 1, 1, 3, 1, 0, 1, 3, 1, 2, 1, 2, 3, 1, 2, 0, 2, 0, 3, 2, 3, 0, 3, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 2, 3, 3, 0, 3, 1, 1, 3, 2, 1, 2, 1, 1, 0, 3, 0, 3, 0, 3, 2, 1, 0, 1, 0, 3, 0, 1, 3, 0, 0, 3, 1, 3, 3, 2, 2, 2, 1, 1, 0, 1, 1, 3, 3, 1, 1, 2, 2, 0, 1, 2, 3, 2, 3, 0, 1, 1, 1, 0, 2, 2, 2, 3, 2, 1, 3, 0, 3, 0, 0, 0, 0, 3, 1, 1, 2, 0, 2, 2, 3, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 1, 1, 0, 0, 1, 2, 1, 1, 1, 0, 1, 1, 1, 0, 3, 2, 3, 2, 2, 1, 3, 3, 0, 2, 3, 2, 0, 1, 2, 3, 0, 1, 0, 3, 2, 2, 3, 0, 0, 0, 0, 3, 3, 2, 0, 3, 0, 3, 1, 1, 3, 1, 1, 1, 1, 0, 2, 2, 2, 1, 0, 0, 3, 3, 1, 2, 0, 0, 3, 1, 1, 3, 2, 3, 2, 1, 1, 2, 2, 1, 1, 3, 2, 1, 2, 1, 1, 2, 1, 3, 2, 3, 1, 0, 2, 1, 2, 1, 3, 1, 0, 3, 3, 1, 2, 1, 0, 2, 0, 3, 1, 3, 0, 2, 1, 3, 0, 3, 0, 0, 0, 3, 0, 0, 3, 3, 2, 1, 2, 0, 2, 1, 0, 3, 1, 1, 0, 1, 2, 1, 3, 3, 1, 1, 3, 3, 2, 1, 2, 1, 0, 0, 3, 2, 2, 0, 1, 2, 1, 3, 2, 3, 1, 3, 3, 2, 3, 1, 3, 1, 3, 0, 2, 0, 3, 0, 0, 2, 2, 1, 1, 1, 0, 1, 2, 2, 0, 1, 0, 1, 2, 0, 1, 0, 2, 3, 0, 0, 3, 0, 1, 1, 0, 2, 1, 2, 3, 1, 0, 0, 3, 1, 1, 0, 3, 3, 2, 2, 3, 0, 2, 3, 3, 3, 3, 0, 2, 0, 3, 2, 3, 1, 0, 1, 3, 2, 1, 3, 2, 1, 3, 3, 1, 2, 2, 2, 1, 0, 0, 1, 2, 3, 2, 0, 1, 1, 2, 0, 2, 0, 1, 0, 3, 3, 1, 3, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 3, 3, 2, 1, 2, 1, 2, 2, 2, 1, 0, 1, 2, 3, 0, 3, 1, 0, 3, 3, 1, 1, 2, 0, 0, 1, 3, 1, 0, 3, 2, 1, 2, 0, 2, 2, 2, 2, 2, 1, 2, 1, 0, 2, 3, 2, 1, 2, 1, 2, 1, 2, 3, 2, 2, 2, 1, 3, 1, 2, 2, 2, 2, 3, 2, 1, 0, 3, 2, 3, 3, 3, 0, 2, 0, 3, 0, 0, 0, 2, 1, 3, 0, 0, 0, 3, 2, 0, 1, 1, 0, 0, 2, 3, 1, 2, 0, 0, 2, 0, 3, 3, 0, 3, 1, 3, 1, 2, 2, 1, 1, 0, 3, 3, 1, 2, 2, 1, 1, 1, 2, 0, 2, 3, 1, 0, 0, 1, 1, 1, 2, 0, 1, 0, 0, 2, 2, 0, 0, 2, 2, 3, 0, 0, 2, 1, 3, 1, 2, 2, 1, 0, 2, 3, 1, 3, 1, 3, 3, 1, 2, 3, 0, 1, 2, 0, 1, 3, 2, 2, 0, 2, 1, 3, 3, 2, 0, 3, 0, 1, 3, 3, 3, 2, 3, 0, 3, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 0, 3, 3, 0, 0, 1, 3, 2, 0, 1, 0, 1, 2, 1, 2, 3, 3, 2, 3, 0, 0, 2, 1, 3, 2, 0, 1, 0, 1, 3, 1, 3, 2, 3, 1, 2, 3, 2, 1, 3, 1, 3, 0, 1, 2, 0, 1, 1, 1, 1, 3, 1, 1, 3, 2, 1, 2, 0, 0, 3, 2, 3, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0, 0, 1, 0, 0, 3, 3, 1, 3, 3, 3, 1, 3, 3, 0, 0, 3, 2, 2, 1, 0, 1, 2, 2, 1, 0, 2, 0, 1, 1, 2, 1, 1, 0, 2, 0, 0, 3, 1, 0, 1, 2, 3, 3, 0, 1, 0, 2, 2, 1, 1, 1, 2, 3, 3, 1, 3, 0, 0, 1, 1, 1, 2, 3, 1, 3, 3, 3, 1, 3, 0, 1, 2, 0, 1, 0, 2, 3, 1, 3, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 3, 1, 3, 3, 1, 0, 3, 0, 1, 2, 0, 0, 1, 0, 0, 2, 1, 3, 1, 0, 1, 3, 2, 3, 3, 3, 1, 2, 3, 3, 3, 1, 1, 0, 3, 0, 2, 1, 3, 3, 1, 1, 3, 1, 3, 0, 3, 3, 1, 1, 2, 1, 3, 3, 3, 0, 3, 3, 0, 2, 3, 2, 3, 1, 2, 3, 2, 3, 0, 1, 2, 1, 3, 1, 3, 2, 1, 0, 3, 3, 1, 0, 2, 3, 0, 0, 3, 3, 0, 0, 1, 0, 2, 2, 1, 0, 3, 2, 0, 2, 0, 2, 1, 3, 2, 3, 0, 0, 0, 0, 0, 3, 1, 2, 2, 0, 2, 2, 1, 3, 1, 3, 0, 1, 1, 0, 3, 1, 1, 3, 0, 0, 2, 1, 0, 0, 2, 1, 0, 3, 0, 2, 2, 0, 1, 0, 2, 2, 3, 3, 0, 0, 1, 1, 1, 2, 0, 3, 1, 2, 0, 2, 3, 0, 1, 1, 2, 3, 3, 1, 0, 2, 1, 0, 1, 0, 3, 1, 0, 1, 1, 2, 2, 2, 0, 1, 3, 2, 2, 3, 2, 1, 0, 1, 3, 0, 0, 1, 2, 2, 2, 3, 2, 1, 0, 2, 3, 3, 1, 1, 3, 2, 0, 1, 1, 0, 0, 2, 3, 3, 1, 2, 3, 1, 1, 2, 2, 3, 0, 2, 3, 1, 1, 3, 1, 2, 1, 0, 1, 2, 0, 0, 0, 1, 3, 1, 0, 1, 1, 3, 2, 2, 3, 1, 2, 2, 2, 1, 1, 0, 2, 2, 1, 3, 1, 1, 1, 2, 1, 1, 1, 3, 2, 0, 0, 2, 0, 2, 0, 0, 3, 1, 1, 0, 3, 1, 1, 2, 0, 1, 1, 0, 0, 1, 1, 3, 0, 0, 0, 2, 2, 1, 2, 3, 3, 3, 0, 2, 2, 0, 2, 1, 3, 0, 1, 1, 1, 1, 1, 1, 3, 2, 0, 0, 0, 2, 2, 1, 0, 1, 0, 3, 2, 2, 1, 3, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 0, 2, 1, 1, 1, 2, 0, 0, 2, 1, 2, 2, 0, 3, 0, 1, 0, 1, 1, 0, 2, 1, 0, 1, 3, 1, 0, 1, 2, 2, 3, 1, 2, 3, 3, 0, 0, 1, 3, 1, 3, 1, 3, 3, 1, 0, 2, 1, 2, 1, 3, 2, 2, 1, 2, 3, 3, 2, 0, 1, 1, 3, 1, 3, 2, 3, 0, 0, 3, 1, 3, 3, 0, 0, 2, 2, 2, 2, 2, 1, 0, 3, 1, 3, 3, 2, 2, 1, 3, 2, 3, 2, 1, 0, 1, 2, 0, 3, 2, 2, 1, 1, 1, 3, 0, 0, 3, 2, 1, 1, 0, 2, 0, 0, 1, 0, 0, 2, 1, 2, 1, 2, 3, 3, 0, 2, 1, 3, 2, 3, 2, 0, 2, 0, 3, 3, 1, 0, 3, 2, 0, 3, 2, 0, 2, 3, 0, 1, 1, 3, 2, 3, 0, 0, 3, 1, 3, 2, 1, 2, 2, 0, 3, 3, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 2, 2, 1, 3, 0, 0, 3, 0, 3, 1, 3, 2, 2, 1, 1, 1, 3, 2, 3, 0, 1, 2, 2, 3, 1, 3, 3, 3, 2, 3, 1, 0, 2, 1, 3, 3, 2, 3, 1, 2, 1, 3, 3, 2, 3, 2, 1, 0, 2, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 0, 3, 2, 1, 1, 3, 3, 3, 2, 1, 0, 1, 3, 3, 1, 3, 0, 3, 2, 1, 3, 0, 0, 1, 2, 1, 0, 2, 0, 0, 2, 1, 1, 0, 0, 3, 0, 0, 3, 3, 1, 3, 3, 3, 2, 2, 1, 3, 1, 1, 2, 1, 0, 1, 2, 1, 1, 2, 3, 0, 2, 0, 2, 0, 0, 2, 1, 3, 2, 1, 1, 1, 1, 0, 1, 2, 1, 2, 2, 1, 2, 0, 1, 3, 1, 2, 2, 3, 3, 3, 1, 3, 3, 2, 2, 3, 1, 1, 0, 2, 3, 2, 3, 2, 1, 0, 2, 3, 2, 0, 0, 3, 0, 2, 2, 3, 3, 2, 3, 0, 0, 0, 3, 1, 2, 0, 0, 2, 0, 1, 3, 1, 3, 3, 3, 3, 0, 3, 2, 2, 3, 0, 2, 2, 3, 0, 3, 0, 3, 1, 1, 2, 3, 2, 2, 3, 0, 2, 3, 2, 1, 0, 0, 2, 3, 0, 0, 3, 0, 0, 2, 1, 2, 1, 3, 1, 0, 0, 3, 0, 3, 0, 3, 2, 3, 0, 1, 3, 0, 2, 2, 1, 1, 3, 1, 2, 3, 1, 2, 2, 2, 1, 2, 3, 2, 1, 3, 2, 0, 0, 3, 1, 0, 1, 0, 0, 1, 0, 2, 2, 2, 1, 1, 2, 3, 0, 2, 0, 3, 2, 1, 3, 0, 3, 0, 2, 2, 3, 0, 0, 0, 0, 3, 0, 3, 0, 2, 1, 2, 2, 0, 0, 1, 1, 2, 3, 3, 3, 2, 0, 2, 2, 0, 3, 0, 1, 2, 2, 3, 2, 2, 2, 1, 3, 1, 2, 1, 0, 2, 1, 3, 2, 1, 1, 3, 0, 3, 1, 1, 0, 3, 1, 2, 2, 0, 2, 1, 1, 0, 2, 0, 3, 0, 2, 2, 2, 0, 2, 3, 1, 0, 1, 0, 0, 1, 1, 1, 0, 3, 3, 2, 2, 2, 1, 3, 2, 0, 1, 3, 0, 1, 1, 2, 3, 2, 3, 0, 3, 0, 1, 3, 0, 1, 1, 1, 0, 2, 1, 3, 3, 2, 2, 0, 0, 3, 1, 1, 2, 1, 3, 0, 0, 2, 2, 3, 1, 0, 0, 2, 0, 2, 1, 0, 0, 2, 0, 1, 1, 1, 0, 2, 3, 1, 0, 2, 2, 1, 0, 3, 3, 3, 0, 1, 2, 3, 3, 1, 2, 1, 0, 1, 0, 2, 0, 0, 3, 3, 1, 2, 1, 1, 2, 0, 1, 2, 2, 2, 3, 0, 2, 3, 2, 0, 3, 2, 1, 2, 2, 1, 1, 3, 0, 3, 2, 1, 2, 0, 1, 1, 3, 1, 0, 1, 3, 1, 3, 1, 3, 3, 0, 0, 2, 2, 1, 3, 0, 3, 3, 1, 1, 0, 3, 3, 3, 1, 2, 3, 2, 0, 0, 2, 1, 3, 1, 0, 1, 1, 0, 0, 2, 0, 1, 2, 0, 0, 0, 1, 1, 2, 3, 0, 2, 0, 1, 2, 3, 2, 2, 2, 0, 2, 1, 1, 2, 3, 3, 1, 3, 2, 2, 0, 1, 2, 0, 0, 3, 0, 1, 1, 2, 0, 2, 2, 2, 0, 3, 2, 0, 3, 2, 0, 3, 3, 1, 0, 1, 2, 0, 0, 0, 2, 2, 3, 2, 2, 0, 3, 3, 1, 3, 1, 1, 0, 1, 2, 3, 3, 0, 0, 1, 1, 3, 3, 0, 2, 2, 0, 3, 2, 2, 3, 2, 0, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 2, 2, 3, 0, 3, 0, 1, 2, 0, 1, 3, 3, 2, 3, 0, 1, 2, 2, 1, 3, 2, 3, 2, 2, 1, 2, 2, 3, 1, 1, 0, 2, 0, 0, 3, 3, 1, 0, 1, 3, 2, 2, 3, 1, 3, 3, 2, 0, 1, 1, 3, 2, 1, 1, 1, 2, 0, 2, 2, 0, 3, 1, 3, 3, 2, 3, 3, 1, 3, 1, 1, 0, 3, 3, 0, 2, 0, 3, 2, 2, 3, 3, 2, 2, 3, 2, 3, 3, 3, 0, 2, 1, 1, 2, 1, 3, 1, 2, 3, 1, 2, 0, 3, 1, 0, 0, 0, 3, 2, 1, 1, 3, 3, 0, 3, 2, 0, 1, 2, 2, 0, 0, 2, 2, 3, 0, 1, 1, 0, 1, 0, 1, 3, 1, 1, 3, 2, 2, 1, 3, 0, 1, 1, 2, 0, 3, 2, 1, 0, 3, 0, 0, 0, 3, 2, 2, 1, 3, 3, 3, 1, 3, 1, 2, 3, 1, 0, 3, 0, 2, 0, 0, 2, 1, 0, 0, 3, 3, 0, 2, 0, 3, 1, 1, 0, 1, 2, 0, 3, 3, 1, 1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 1, 1, 0, 2, 0, 0, 1, 1, 0, 3, 2, 0, 0, 2, 3, 2, 3, 1, 2, 1, 3, 2, 1, 1, 3, 3, 2, 2, 3, 3, 0, 0, 0, 2, 0, 2, 3, 0, 3, 1, 0, 3, 1, 2, 1, 2, 3, 3, 2, 3, 1, 0, 3, 3, 1, 3, 3, 0, 2, 2, 1, 3, 1, 2, 0, 1, 0, 1, 0, 0, 3, 3, 2, 1, 0, 2, 2, 0, 0, 1, 0, 2, 1, 0, 1, 2, 0, 3, 0, 0, 3, 2, 3, 0, 3, 2, 3, 2, 1, 3, 1, 1, 0, 3, 3, 2, 1, 2, 3, 1, 2, 1, 1, 3, 0, 2, 2, 2, 0, 2, 1, 1, 0, 3, 1, 2, 3, 3, 2, 1, 3, 1, 1, 2, 1, 3, 0, 1, 3, 0, 2, 2, 2, 1, 0, 1, 1, 1, 1, 2, 3, 0, 0, 2, 3, 3, 0, 1, 3, 1, 0, 0, 3, 0, 0, 0, 1, 2, 1, 1, 0, 0, 3, 1, 1, 1, 2, 2, 2, 1, 2, 0, 3, 0, 2, 0, 0, 0, 2, 3, 1, 2, 2, 0, 2, 0, 2, 2, 0, 3, 1, 0, 0, 2, 1, 0, 0, 0, 3, 0, 0, 3, 0, 3, 3, 3, 2, 1, 2, 3, 2, 0, 1, 2, 2, 0, 0, 2, 2, 3, 2, 1, 3, 2, 0, 3, 1, 0, 0, 3, 3, 1, 0, 0, 1, 2, 3, 1, 1, 3, 0, 2, 3, 3, 2, 1, 3, 3, 2, 3, 1, 3, 0, 0, 1, 3, 0, 1, 2, 3, 0, 1, 3, 0, 0, 1, 1, 3, 0, 1, 3, 0, 2, 2, 3, 3, 3, 1, 2, 2, 1, 1, 2, 0, 1, 3, 3, 0, 1, 3, 0, 0, 3, 0, 3, 1, 2, 0, 0, 0, 1, 1, 2, 0, 1, 2, 0, 1, 3, 0, 3, 1, 1, 2, 3, 0, 3, 0, 3, 3, 1, 2, 2, 0, 1, 0, 1, 2, 1, 3, 3, 2, 3, 2, 0, 1, 2, 1, 1, 3, 1, 0, 0, 1, 3, 1, 2, 1, 2, 0, 0, 2, 1, 3, 3, 1, 2, 0, 0, 2, 3, 3, 0, 1, 0, 1, 1, 0, 1, 2, 2, 3, 2, 3, 0, 1, 1, 2, 3, 1, 2, 1, 1, 2, 2, 2, 3, 2, 3, 0, 1, 2, 3, 3, 3, 1, 2, 2, 1, 2, 1, 2, 3, 3, 0, 3, 3, 3, 0, 3, 0, 0, 0, 1, 2, 1, 1, 3, 0, 2, 3, 2, 2, 1, 1, 1, 0, 3, 0, 3, 3, 1, 0, 2, 3, 2, 1, 1, 1, 3, 2, 0, 3, 0, 3, 3, 2, 2, 0, 3, 1, 1, 1, 3, 0, 0, 3, 0, 3, 1, 2, 1, 3, 1, 1, 0, 0, 1, 2, 3, 3, 2, 2, 0, 1, 3, 3, 3, 2, 0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 2, 2, 3, 3, 1, 1, 1, 0, 3, 0, 3, 2, 2, 3, 1, 1, 0, 3, 3, 2, 1, 1, 2, 2, 1, 3, 0, 3, 0, 0, 2, 1, 2, 1, 1, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 3, 1, 0, 3, 0, 0, 0, 2, 1, 0, 2, 2, 1, 1, 0, 3, 3, 3, 2, 3, 1, 3, 1, 3, 3, 2, 1, 3, 0, 3, 2, 1, 0, 3, 1, 2, 2, 1, 3, 0, 1, 0, 0, 1, 2, 0, 0, 0, 3, 1, 2, 0, 0, 1, 0, 2, 3, 0, 2, 2, 2, 3, 2, 2, 2, 3, 1, 2, 2, 3, 1, 0, 1, 2, 2, 2, 1, 0, 0, 1, 1, 1, 0, 3, 2, 0, 0, 1, 2, 3, 1, 3, 0, 2, 3, 2, 0, 1, 0, 2, 0, 2, 3, 3, 1, 1, 3, 3, 2, 2, 1, 3, 0, 0, 0, 3, 1, 0, 2, 0, 0, 3, 2, 1, 3, 3, 3, 0, 1, 1, 3, 3, 0, 0, 1, 1, 3, 1, 3, 2, 3, 1, 0, 1, 3, 0, 3, 3, 1, 0, 0, 3, 0, 1, 0, 2, 1, 0, 0, 0, 1, 1, 3, 2, 1, 1, 0, 2, 1, 1, 2, 3, 2, 1, 2, 2, 0, 2, 2, 0, 1, 0, 1, 3, 2, 0, 0, 3, 2, 0, 3, 2, 0, 2, 3, 2, 2, 1, 2, 2, 3, 2, 2, 1, 2, 3, 0, 1, 0, 3, 2, 3, 0, 2, 0, 3, 0, 0, 1, 2, 2, 2, 0, 3, 0, 3, 2, 3, 3, 0, 2, 3, 2, 3, 3, 2, 3, 1, 1, 3, 1, 0, 3, 0, 3, 3, 2, 1, 2, 3, 1, 1, 1, 2, 3, 3, 0, 2, 3, 1, 3, 3, 1, 2, 1, 0, 0, 0, 3, 1, 2, 0, 2, 3, 0, 3, 1, 1, 1, 0, 1, 3, 0, 3, 2, 3, 3, 0, 2, 0, 2, 2, 1, 1, 1, 3, 2, 0, 2, 3, 2, 3, 0, 1, 0, 1, 0, 2, 1, 2, 2, 0, 1, 3, 0, 2, 3, 1, 1, 0, 3, 3, 3, 0, 2, 0, 3, 1, 3, 2, 2, 1, 2, 0, 1, 2, 3, 2, 1, 3, 2, 3, 2, 1, 2, 2, 2, 3, 2, 0, 0, 3, 1, 2, 3, 1, 3, 3, 0, 0, 3, 1, 1, 0, 1, 3, 3, 1, 3, 2, 2, 0, 2, 1, 0, 1, 1, 2, 0, 2, 2, 0, 1, 1, 1, 3, 3, 2, 3, 0, 1, 0, 3, 3, 3, 1, 1, 0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 3, 0, 3, 1, 2, 1, 0, 1, 1, 0, 0, 3, 3, 0, 1, 0, 2, 0, 1, 1, 2, 3, 2, 1, 3, 3, 1, 3, 0, 3, 2, 0, 3, 2, 2, 0, 2, 0, 3, 3, 3, 3, 3, 3, 0, 3, 1, 3, 0, 3, 1, 0, 1, 0, 3, 3, 1, 2, 0, 2, 1, 1, 0, 0, 0, 3, 1, 1, 1, 1, 2, 2, 2, 3, 2, 1, 0, 2, 2, 0, 0, 3, 0, 2, 0, 1, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 0, 1, 1, 2, 3, 3, 0, 0, 2, 0, 1, 1, 0, 2, 2, 1, 2, 3, 1, 3, 0, 0, 3, 1, 3, 0, 1, 2, 0, 3, 0, 2, 1, 1, 0, 2, 3, 0, 0, 1, 2, 0, 1, 3, 1, 1, 2, 1, 3, 2, 3, 3, 3, 1, 2, 2, 1, 0, 0, 1, 2, 3, 3, 1, 3, 0, 1, 1, 0, 1, 0, 0, 3, 0, 2, 3, 1, 3, 3, 1, 1, 3, 1, 2, 1, 0, 3, 0, 2, 2, 2, 1, 2, 1, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 1, 3, 2, 2, 0, 3, 1, 0, 2, 3, 1, 2, 2, 2, 1, 1, 1, 1, 2, 3, 3, 2, 1, 2, 2, 3, 2, 0, 3, 3, 2, 2, 2, 1, 0, 2, 0, 2, 0, 0, 1, 0, 3, 1, 0, 2, 0, 3, 3, 3, 1, 3, 2, 0, 2, 3, 0, 1, 1, 0, 3, 1, 0, 0, 0, 2, 0, 3, 2, 1, 1, 0, 3, 1, 3, 1, 3, 2, 1, 3, 2, 3, 3, 0, 2, 1, 3, 1, 1, 0, 0, 3, 3, 1, 0, 0, 2, 1, 0, 3, 0, 2, 3, 1, 2, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 3, 0, 0, 0, 2, 2, 1, 0, 1, 2, 1, 2, 1, 0, 2, 0, 1, 3, 3, 3, 0, 3, 3, 2, 3, 2, 3, 1, 1, 3, 0, 3, 0, 3, 2, 3, 2, 3, 1, 2, 2, 3, 2, 2, 0, 0, 2, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 3, 3, 2, 3, 1, 0, 2, 3, 3, 0, 1, 0, 0, 2, 3, 3, 1, 3, 3, 0, 1, 0, 1, 0, 2, 0, 3, 0, 1, 3, 1, 3, 0, 0, 1, 2, 1, 3, 3, 1, 1, 0, 1, 1, 3, 3, 2, 0, 0, 0, 1, 3, 1, 1, 2, 3, 1, 0, 3, 1, 3, 3, 2, 0, 3, 3, 0, 3, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 3, 0, 0, 1, 3, 3, 3, 2, 1, 1, 2, 1, 3, 3, 0, 2, 2, 2, 1, 0, 1, 2, 1, 2, 1, 3, 2, 0, 3, 3, 2, 1, 0, 1, 1, 0, 0, 1, 0, 2, 3, 0, 3, 2, 1, 0, 3, 1, 2, 3, 3, 3, 2, 3, 3, 1, 1, 1, 0, 2, 0, 0, 3, 1, 1, 1, 2, 2, 2, 1, 0, 2, 1, 0, 3, 1, 2, 2, 0, 2, 3, 1, 2, 3, 3, 0, 1, 3, 2, 3, 2, 0, 0, 3, 3, 2, 1, 2, 0, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1, 0, 2, 1, 2, 1, 0, 1, 3, 2, 0, 3, 0, 1, 0, 0, 1, 0, 0, 1, 3, 1, 2, 0, 2, 3, 0, 2, 2, 1, 3, 0, 3, 0, 1, 3, 0, 3, 3, 3, 2, 0, 1, 2, 2, 0, 2, 2, 2, 2, 2, 0, 1, 0, 2, 3, 2, 0, 0, 0, 1, 0, 3, 1, 3, 1, 0, 2, 2, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 0, 1, 3, 1, 3, 1, 3, 2, 1, 2, 3, 3, 1, 1, 0, 3, 3, 3, 3, 1, 0, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0, 3, 1, 3, 1, 1, 2, 3, 0, 3, 3, 1, 1, 0, 0, 1, 3, 2, 3, 1, 0, 1, 3, 1, 0, 1, 2, 1, 1, 1, 0, 2, 1, 2, 0, 1, 1, 2, 1, 2, 1, 3, 1, 1, 3, 0, 0, 2, 3, 2, 0, 2, 0, 3, 0, 3, 2, 0, 0, 2, 2, 2, 0, 2, 1, 3, 3, 1, 3, 1, 1, 2, 2, 0, 2, 3, 1, 1, 0, 1, 3, 1, 0, 3, 3, 2, 3, 3, 3, 0, 2, 2, 1, 1, 3, 0, 0, 0, 3, 2, 1, 0, 3, 0, 0, 0, 2, 0, 3, 2, 0, 3, 0, 3, 0, 1, 1, 1, 0, 2, 3, 3, 2, 1, 1, 0, 0, 3, 0, 0, 2, 0, 1, 2, 1, 3, 3, 2, 2, 2, 0, 2, 3, 3, 0, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 3, 1, 0, 2, 3, 2, 0, 3, 1, 2, 3, 3, 1, 3, 1, 1, 1, 2, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 2, 2, 1, 3, 3, 3, 1, 1, 3, 1, 0, 3, 3, 0, 0, 0, 3, 2, 0, 3, 3, 3, 0, 1, 0, 1, 2, 2, 0, 2, 2, 0, 2, 0, 3, 1, 1, 0, 3, 0, 0, 3, 0, 3, 0, 1, 3, 3, 1, 2, 0, 2, 0, 3, 3, 0, 2, 2, 0, 2, 2, 3, 0, 3, 3, 0, 2, 0, 2, 2, 0, 3, 0, 1, 3, 2, 3, 1, 3, 1, 2, 1, 0, 1, 2, 2, 1, 0, 0, 1, 2, 1, 3, 0, 0, 3, 0, 2, 2, 3, 0, 0, 2, 0, 0, 2, 2, 1, 2, 3, 3, 3, 0, 1, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 0, 3, 1, 1, 1, 0, 2, 0, 0, 2, 3, 3, 1, 2, 1, 1, 0, 3, 2, 0, 0, 3, 3, 1, 1, 2, 1, 2, 0, 1, 1, 3, 1, 3, 1, 3, 0, 0, 0, 3, 1, 1, 2, 0, 2, 3, 2, 0, 1, 2, 2, 0, 1, 2, 0, 2, 0, 1, 3, 3, 3, 1, 0, 1, 2, 1, 2, 3, 2, 1, 3, 3, 1, 0, 2, 0, 1, 2, 1, 3, 0, 0, 0, 0, 2, 1, 2, 2, 3, 1, 3, 0, 0, 0, 2, 3, 0, 1, 3, 2, 3, 1, 1, 1, 0, 2, 3, 0, 3, 2, 2, 0, 3, 3, 2, 1, 2, 1, 1, 2, 1, 0, 0, 1, 3, 2, 1, 3, 2, 2, 0, 3, 1, 3, 2, 3, 0, 0, 2, 0, 3, 0, 1, 2, 3, 3, 0, 2, 0, 2, 3, 1, 1, 3, 3, 2, 0, 0, 1, 3, 1, 3, 3, 1, 3, 3, 1, 2, 0, 1, 1, 2, 2, 0, 3, 2, 1, 1, 2, 2, 1, 2, 0, 2, 2, 0, 0, 2, 3, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 2, 2, 3, 2, 2, 2, 2, 1, 2, 3, 3, 1, 2, 0, 0, 2, 1, 3, 2, 2, 3, 1, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 1, 3, 3, 1, 3, 3, 3, 0, 0, 0, 0, 3, 2, 3, 2, 0, 2, 2, 1, 3, 3, 3, 0, 1, 3, 1, 1, 3, 3, 3, 2, 0, 1, 0, 3, 3, 1, 2, 0, 3, 0, 0, 3, 2, 0, 1, 2, 1, 3, 0, 3, 0, 3, 3, 0, 2, 1, 3, 0, 1, 0, 2, 0, 0, 3, 2, 3, 2, 2, 1, 2, 3, 1, 3, 3, 3, 3, 1, 1, 3, 1, 3, 3, 2, 1, 0, 3, 2, 0, 1, 2, 0, 1, 2, 3, 2, 2, 3, 2, 0, 0, 3, 2, 3, 2, 0, 2, 0, 1, 1, 3, 1, 2, 1, 0, 3, 2, 3, 3, 3, 1, 2, 1, 2, 2, 2, 0, 2, 3, 1, 1, 1, 3, 1, 0, 2, 2, 3, 1, 3, 1, 3, 1, 1, 3, 2, 0, 2, 2, 1, 2, 3, 1, 3, 0, 0, 2, 3, 3, 0, 0, 1, 3, 3, 3, 2, 3, 0, 3, 0, 0, 0, 1, 2, 2, 1, 1, 2, 3, 1, 2, 0, 1, 1, 0, 1, 1, 2, 2, 3, 3, 2, 1, 1, 0, 2, 0, 1, 0, 0, 2, 2, 2, 2, 0, 2, 0, 3, 3, 2, 3, 1, 0, 3, 0, 0, 3, 3, 2, 0, 0, 3, 0, 1, 2, 1, 0, 0, 0, 0, 2, 3, 3, 1, 3, 0, 0, 1, 1, 1, 1, 2, 2, 0, 2, 0, 0, 3, 1, 1, 2, 1, 0, 1, 0, 3, 3, 3, 2, 1, 2, 2, 0, 1, 3, 3, 3, 2, 0, 0, 3, 3, 3, 2, 0, 2, 3, 0, 0, 2, 0, 1, 2, 0, 2, 0, 3, 1, 0, 2, 2, 1, 3, 3, 2, 2, 3, 0, 2, 1, 2, 2, 0, 3, 1, 2, 2, 1, 1, 3, 1, 2, 3, 2, 2, 3, 3, 1, 3, 0, 3, 3, 3, 2, 0, 0, 1, 2, 2, 2, 1, 2, 1, 1, 3, 2, 3, 2, 1, 3, 3, 1, 1, 3, 0, 1, 2, 2, 2, 2, 0, 0, 1, 3, 1, 1, 1, 3, 3, 2, 0, 2, 3, 3, 1, 1, 3, 2, 1, 0, 0, 2, 0, 0, 2, 1, 0, 3, 2, 1, 3, 2, 2, 2, 3, 2, 3, 3, 3, 2, 2, 3, 1, 1, 3, 3, 3, 1, 3, 1, 3, 2, 1, 3, 3, 0, 3, 1, 2, 3, 3, 3, 3, 3, 0, 2, 1, 3, 0, 2, 2, 0, 3, 3, 1, 2, 3, 3, 3, 2, 0, 0, 2, 1, 2, 3, 0, 2, 3, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 0, 2, 1, 1, 3, 0, 3, 0, 2, 1, 1, 1, 2, 0, 0, 0, 2, 0, 1, 2, 1, 3, 0, 3, 0, 3, 1, 0, 0, 1, 3, 0, 0, 2, 1, 2, 1, 0, 1, 1, 0, 0, 0, 2, 0, 0, 3, 3, 0, 1, 3, 0, 0, 1, 2, 1, 3, 3, 1, 1, 2, 0, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 1, 1, 0, 1, 1, 3, 0, 1, 0, 0, 1, 2, 2, 2, 0, 1, 2, 1, 0, 3, 0, 1, 0, 0, 3, 2, 3, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 3, 1, 2, 0, 1, 3, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 0, 3, 2, 2, 0, 2, 1, 0, 0, 0, 2, 2, 1, 0, 1, 0, 2, 0, 2, 0, 3, 0, 1, 2, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 0, 3, 2, 0, 0, 3, 3, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 0, 1, 1, 1, 1, 2, 0, 1, 0, 2, 1, 3, 2, 3, 1, 1, 0, 3, 1, 3, 0, 1, 0, 3, 1, 0, 1, 2, 2, 1, 1, 0, 3, 1, 1, 3, 2, 1, 2, 1, 0, 1, 3, 2, 1, 2, 1, 1, 3, 2, 0, 3, 0, 1, 0, 3, 1, 1, 2, 0, 0, 2, 0, 0, 2, 3, 3, 2, 0, 2, 3, 1, 1, 0, 3, 2, 1, 2, 1, 0, 3, 2, 3, 0, 1, 2, 3, 1, 2, 3, 0, 2, 1, 2, 0, 3, 2, 3, 2, 1, 2, 0, 2, 2, 3, 0, 3, 3, 2, 0, 1, 0, 2, 3, 2, 3, 0, 3, 2, 2, 3, 1, 0, 1, 3, 2, 2, 0, 2, 3, 2, 2, 2, 2, 1, 1, 3, 0, 2, 2, 0, 0, 1, 3, 1, 0, 3, 0, 3, 1, 0, 0, 2, 2, 2, 1, 2, 3, 2, 3, 2, 2, 2, 3, 3, 1, 2, 3, 2, 0, 2, 2, 3, 3, 2, 2, 0, 3, 0, 3, 1, 2, 0, 3, 0, 0, 1, 3, 3, 3, 3, 2, 1, 0, 3, 2, 2, 2, 2, 3, 1, 1, 1, 2, 2, 2, 3, 3, 0, 2, 0, 3, 0, 3, 0, 3, 2, 3, 2, 1, 2, 3, 0, 0, 2, 0, 2, 2, 2, 0, 1, 0, 3, 0, 0, 1, 1, 2, 0, 1, 0, 2, 3, 1, 3, 0, 1, 1, 2, 2, 0, 1, 2, 2, 3, 2, 3, 0, 3, 1, 3, 3, 2, 2, 0, 1, 1, 0, 2, 1, 2, 2, 0, 0, 0, 3, 2, 2, 3, 3, 1, 3, 0, 1, 2, 0, 2, 2, 2, 3, 2, 1, 3, 1, 2, 3, 1, 2, 3, 2, 3, 3, 1, 3, 3, 3, 3, 2, 3, 0, 3, 1, 1, 1, 0, 2, 3, 3, 2, 3, 1, 2, 0, 2, 3, 2, 0, 1, 2, 1, 3, 1, 3, 2, 0, 2, 1, 3, 0, 2, 1, 3, 3, 3, 3, 0, 2, 2, 1, 3, 1, 0, 0, 2, 1, 1, 1, 3, 0, 1, 1, 2, 2, 2, 0, 1, 2, 1, 0, 2, 2, 0, 3, 1, 1, 1, 2, 0, 1, 1, 2, 3, 3, 1, 1, 1, 2, 0, 3, 0, 3, 3, 0, 3, 1, 2, 3, 0, 2, 3, 3, 3, 2, 0, 0, 0, 2, 3, 2, 3, 2, 2, 2, 0, 3, 2, 1, 0, 0, 0, 2, 3, 1, 3, 1, 3, 1, 3, 2, 3, 1, 1, 3, 1, 2, 1, 2, 0, 3, 2, 0, 0, 1, 1, 3, 0, 2, 1, 2, 2, 2, 1, 2, 2, 3, 0, 2, 1, 0, 0, 2, 0, 2, 0, 3, 0, 1, 2, 1, 3, 2, 1, 3, 1, 2, 0, 1, 2, 2, 3, 3, 1, 2, 0, 0, 0, 3, 0, 2, 1, 0, 0, 0, 3, 2, 0, 3, 0, 2, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 3, 2, 0, 1, 1, 0, 0, 2, 1, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 0, 2, 1, 1, 2, 2, 0, 1, 3, 2, 3, 1, 1, 2, 3, 3, 3, 3, 1, 0, 2, 2, 3, 2, 0, 1, 3, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 0, 2, 0, 2, 2, 3, 0, 0, 3, 0, 2, 3, 3, 0, 0, 0, 3, 0, 1, 0, 0, 0, 1, 1, 1, 3, 3, 3, 2, 3, 2, 1, 2, 2, 1, 1, 1, 0, 2, 2, 2, 1, 2, 3, 2, 0, 0, 0, 2, 1, 0, 1, 3, 3, 2, 3, 3, 3, 0, 0, 2, 1, 2, 1, 1, 0, 3, 1, 2, 3, 1, 0, 3, 3, 2, 2, 1, 0, 1, 0, 3, 0, 2, 0, 3, 2, 3, 0, 2, 1, 0, 2, 3, 0, 1, 3, 0, 2, 0, 1, 2, 3, 2, 0, 2, 1, 2, 2, 0, 0, 2, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 3, 2, 2, 3, 3, 0, 2, 0, 0, 3, 1, 3, 1, 0, 3, 1, 3, 3, 0, 2, 0, 3, 3, 2, 1, 1, 0, 2, 1, 3, 3, 2, 0, 1, 0, 0, 0, 2, 1, 1, 1, 0, 2, 0, 2, 3, 0, 0, 0, 3, 2, 0, 0, 0, 2, 3, 1, 1, 3, 1, 0, 1, 0, 3, 2, 3, 0, 1, 1, 0, 3, 3, 1, 1, 3, 1, 1, 2, 1, 0, 3, 0, 1, 1, 1, 3, 0, 1, 1, 1, 3, 0, 2, 3, 0, 0, 3, 3, 3, 2, 3, 2, 2, 3, 1, 1, 1, 0, 2, 3, 2, 1, 2, 0, 2, 0, 1, 3, 3, 0, 2, 0, 2, 2, 2, 0, 3, 3, 0, 1, 2, 3, 2, 0, 0, 0, 1, 1, 2, 2, 3, 2, 1, 2, 0, 2, 2, 0, 0, 0, 3, 1, 0, 2, 3, 2, 1, 0, 0, 0, 1, 0, 2, 1, 3, 0, 1, 0, 0, 1, 2, 1, 3, 1, 3, 1, 1, 3, 0, 3, 2, 0, 3, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 2, 1, 2, 3, 0, 2, 2, 2, 3, 0, 3, 1, 0, 0, 0, 1, 0, 3, 1, 0, 1, 1, 3, 0, 1, 1, 3, 0, 1, 2, 1, 1, 0, 3, 3, 2, 1, 2, 1, 0, 2, 1, 3, 1, 1, 3, 1, 0, 2, 0, 1, 3, 1, 1, 2, 2, 2, 2, 1, 3, 2, 3, 2, 1, 2, 1, 3, 3, 0, 0, 3, 3, 1, 2, 1, 0, 1, 2, 2, 2, 0, 0, 3, 3, 1, 1, 0, 1, 0, 3, 3, 2, 0, 3, 2, 2, 2, 2, 1, 3, 3, 3, 1, 1, 2, 0, 1, 0, 3, 0, 3, 1, 0, 1, 1, 0, 0, 1, 3, 0, 1, 1, 3, 0, 0, 1, 3, 0, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 0, 3, 2, 3, 3, 1, 2, 2, 2, 2, 2, 0, 0, 2, 1, 0, 0, 2, 2, 1, 3, 0, 1, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 1, 3, 0, 2, 1, 3, 0, 2, 0, 3, 0, 2, 3, 3, 0, 0, 1, 0, 3, 3, 1, 1, 0, 3, 0, 3, 3, 1, 3, 1, 2, 3, 3, 1, 1, 0, 1, 2, 3, 2, 3, 1, 0, 0, 2, 2, 0, 3, 3, 3, 2, 3, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 2, 0, 0, 3, 3, 2, 3, 1, 1, 0, 2, 2, 3, 3, 0, 0, 2, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 0, 2, 0, 1, 0, 1, 2, 2, 3, 0, 2, 0, 2, 2, 0, 3, 3, 1, 2, 2, 2, 1, 2, 2, 3, 3, 1, 2, 1, 1, 1, 3, 3, 1, 0, 3, 3, 1, 3, 2, 0, 0, 3, 1, 0, 1, 2, 1, 0, 3, 0, 1, 3, 0, 3, 1, 0, 0, 2, 3, 0, 1, 3, 3, 3, 1, 1, 0, 3, 0, 3, 0, 3, 3, 0, 1, 2, 3, 0, 1, 1, 3, 2, 3, 2, 0, 1, 0, 0, 1, 3, 2, 2, 0, 3, 3, 1, 1, 1, 2, 2, 0, 2, 0, 0, 3, 2, 2, 3, 3, 0, 2, 2, 2, 0, 2, 0, 3, 0, 2, 2, 2, 2, 2, 1, 2, 1, 3, 2, 1, 2, 1, 1, 1, 3, 0, 2, 0, 0, 2, 3, 3, 3, 2, 1, 1, 2, 1, 2, 1, 2, 3, 2, 0, 2, 3, 0, 1, 2, 3, 2, 3, 0, 3, 0, 1, 2, 0, 1, 2, 1, 0, 2, 0, 2, 3, 1, 1, 1, 1, 1, 2, 2, 0, 2, 3, 1, 3, 0, 2, 3, 0, 1, 2, 2, 1, 3, 3, 3, 1, 1, 3, 0, 2, 2, 0, 0, 0, 3, 2, 2, 0, 1, 3, 2, 3, 3, 2, 3, 3, 3, 2, 2, 2, 1, 0, 2, 0, 3, 0, 3, 0, 3, 3, 2, 1, 2, 0, 1, 2, 1, 0, 0, 2, 1, 0, 2, 3, 3, 0, 3, 0, 2, 0, 1, 2, 2, 0, 1, 2, 3, 3, 3, 2, 1, 1, 2, 0, 3, 0, 0, 3, 1, 3, 0, 3, 0, 2, 3, 1, 0, 1, 2, 1, 3, 3, 3, 2, 0, 2, 2, 1, 2, 0, 3, 1, 1, 2, 2, 1, 2, 3, 0, 2, 0, 1, 2, 3, 0, 2, 1, 0, 3, 2, 2, 2, 0, 2, 0, 0, 3, 0, 3, 3, 0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 1, 1, 2, 0, 3, 1, 3, 2, 1, 0, 3, 1, 0, 2, 2, 2, 1, 2, 0, 2, 0, 1, 1, 2, 3, 3, 2, 1, 3, 2, 1, 1, 0, 1, 3, 2, 2, 3, 2, 3, 0, 3, 2, 3, 1, 1, 3, 1, 0, 3, 3, 2, 3, 0, 2, 2, 0, 3, 3, 2, 0, 3, 3, 3, 2, 3, 3, 3, 2, 0, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 3, 0, 1, 3, 3, 1, 3, 3, 0, 0, 1, 2, 0, 3, 2, 2, 3, 3, 1, 3, 3, 1, 0, 3, 0, 3, 2, 0, 1, 1, 1, 2, 0, 3, 0, 3, 0, 2, 2, 1, 1, 0, 3, 0, 2, 1, 1, 1, 1, 1, 3, 1, 0, 0, 2, 1, 3, 3, 0, 2, 3, 1, 0, 1, 0, 3, 3, 3, 3, 0, 3, 3, 1, 0, 3, 2, 0, 3, 2, 2, 2, 3, 0, 2, 0, 3, 2, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3, 0, 0, 0, 2, 2, 3, 2, 0, 0, 0, 1, 2, 0, 0, 0, 1, 3, 2, 3, 3, 1, 2, 1, 2, 3, 3, 2, 1, 3, 2, 0, 3, 3, 2, 3, 3, 2, 1, 2, 1, 3, 0, 1, 2, 0, 1, 0, 2, 0, 3, 1, 0, 2, 3, 2, 3, 0, 2, 3, 3, 3, 0, 0, 1, 1, 0, 2, 2, 2, 3, 0, 2, 3, 1, 1, 3, 0, 3, 0, 1, 0, 0, 2, 2, 2, 3, 3, 1, 3, 0, 1, 2, 2, 0, 3, 1, 1, 0, 3, 3, 0, 1, 3, 0, 2, 3, 1, 2, 1, 0, 0, 2, 1, 1, 3, 0, 0, 3, 3, 2, 2, 2, 1, 3, 3, 0, 2, 3, 3, 2, 1, 2, 0, 2, 1, 2, 1, 0, 2, 2, 0, 0, 2, 2, 0, 2, 1, 3, 0, 0, 1, 0, 3, 1, 1, 3, 2, 1, 0, 3, 2, 2, 2, 1, 0, 3, 3, 1, 0, 0, 2, 3, 0, 3, 1, 0, 0, 1, 3, 0, 1, 3, 0, 0, 1, 0, 2, 3, 2, 0, 3, 2, 2, 3, 1, 1, 0, 2, 1, 2, 1, 3, 2, 0, 3, 0, 3, 2, 3, 1, 1, 0, 0, 3, 1, 3, 1, 3, 1, 2, 0, 1, 3, 0, 0, 1, 0, 2, 2, 0, 2, 0, 1, 1, 3, 2, 2, 3, 3, 3, 1, 1, 2, 0, 3, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 1, 2, 3, 0, 2, 3, 2, 3, 1, 0, 0, 3, 3, 2, 3, 3, 1, 3, 2, 2, 2, 3, 2, 0, 0, 0, 0, 2, 3, 0, 2, 0, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 1, 2, 3, 3, 3, 0, 3, 0, 3, 1, 2, 3, 0, 3, 0, 2, 3, 0, 1, 3, 2, 2, 0, 0, 2, 2, 3, 2, 2, 2, 1, 3, 2, 0, 1, 1, 0, 3, 2, 0, 2, 3, 2, 1, 3, 1, 1, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 1, 3, 0, 2, 1, 2, 2, 3, 2, 2, 3, 2, 1, 0, 3, 2, 1, 0, 0, 1, 3, 2, 0, 2, 2, 3, 2, 3, 1, 2, 3, 1, 1, 2, 1, 0, 3, 0, 2, 2, 0, 2, 1, 2, 2, 0, 2, 1, 1, 1, 3, 3, 1, 3, 3, 2, 2, 3, 1, 3, 3, 0, 2, 1, 0, 0, 2, 1, 3, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 0, 0, 1, 3, 3, 3, 1, 2, 3, 2, 1, 2, 0, 1, 0, 3, 1, 0, 1, 3, 1, 0, 3, 0, 3, 2, 1, 1, 2, 1, 3, 3, 3, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 0, 3, 1, 0, 0, 2, 2, 3, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 0, 1, 0, 3, 3, 0, 0, 0, 3, 3, 2, 1, 1, 0, 0, 1, 2, 1, 0, 2, 1, 2, 3, 2, 1, 3, 3, 3, 1, 3, 0, 3, 0, 2, 1, 0, 3, 0, 1, 3, 2, 2, 2, 2, 3, 2, 3, 3, 3, 0, 1, 1, 3, 1, 3, 2, 1, 2, 0, 1, 0, 1, 0, 0, 1, 3, 3, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 2, 0, 2, 2, 1, 0, 1, 0, 3, 2, 3, 3, 3, 2, 2, 0, 2, 0, 2, 0, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 2, 3, 2, 3, 3, 0, 0, 1, 0, 1, 3, 3, 0, 1, 0, 3, 0, 3, 2, 0, 2, 3, 1, 1, 1, 1, 3, 2, 2, 0, 3, 0, 3, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 2, 0, 0, 0, 2, 3, 1, 1, 2, 3, 3, 1, 3, 3, 1, 0, 3, 2, 2, 1, 0, 2, 0, 1, 3, 1, 2, 1, 3, 1, 1, 1, 3, 2, 2, 1, 0, 3, 2, 1, 0, 2, 0, 2, 2, 3, 1, 3, 0, 3, 3, 2, 2, 3, 2, 1]


✨ 6. Let's encrypt the query vector by calculating B and ciphertext c.
✨ c_query: (
Rows: 100
Cols: 1
Vector: [502, 35, 173, 693, 113, 827, 738, 776, 144, 776, 739, 214, 960, 894, 918, 467, 644, 688, 620, 737, 636, 307, 427, 555, 92, 768, 439, 654, 587, 817, 287, 39, 573, 685, 369, 2, 567, 695, 644, 640, 669, 831, 601, 955, 474, 130, 453, 381, 545, 57, 587, 878, 803, 704, 666, 359, 394, 15, 840, 307, 216, 873, 547, 801, 752, 541, 755, 846, 831, 723, 671, 437, 866, 355, 296, 253, 994, 530, 161, 900, 498, 45, 817, 340, 360, 610, 347, 303, 875, 22, 118, 793, 840, 268, 520, 530, 160, 709, 74, 182]
, 
Rows: 100
Cols: 10
Vector: [403, 829, 782, 833, 680, 783, 996, 781, 772, 668, 881, 517, 327, 713, 656, 188, 100, 650, 982, 663, 842, 128, 675, 753, 648, 786, 552, 482, 199, 791, 396, 371, 974, 39, 100, 556, 371, 51, 50, 186, 614, 540, 173, 780, 787, 723, 148, 548, 234, 131, 38, 405, 751, 952, 396, 331, 578, 698, 863, 119, 845, 982, 263, 919, 619, 405, 376, 133, 169, 4, 608, 3, 109, 393, 660, 710, 993, 484, 9, 770, 193, 5, 167, 335, 251, 733, 482, 556, 271, 769, 961, 618, 327, 429, 211, 97, 520, 15, 912, 677, 451, 135, 359, 439, 916, 340, 644, 165, 937, 435, 344, 349, 755, 505, 253, 244, 611, 979, 486, 192, 987, 183, 984, 56, 120, 50, 49, 901, 433, 764, 495, 773, 896, 922, 211, 67, 448, 853, 408, 69, 115, 283, 755, 232, 25, 744, 265, 370, 959, 579, 256, 646, 572, 715, 622, 700, 31, 904, 555, 185, 644, 325, 938, 76, 14, 46, 680, 946, 790, 433, 803, 358, 796, 430, 92, 543, 88, 531, 628, 567, 459, 764, 443, 695, 748, 742, 871, 527, 828, 535, 710, 692, 398, 230, 695, 303, 776, 303, 116, 7, 677, 428, 602, 818, 431, 620, 344, 528, 333, 579, 636, 458, 728, 959, 418, 993, 789, 538, 837, 506, 160, 144, 536, 651, 782, 992, 458, 338, 333, 789, 257, 137, 983, 251, 283, 55, 340, 476, 333, 430, 227, 420, 701, 151, 533, 772, 827, 630, 270, 102, 105, 435, 890, 355, 978, 732, 88, 593, 554, 794, 432, 470, 835, 920, 604, 824, 166, 273, 539, 568, 92, 991, 587, 886, 686, 97, 311, 485, 773, 132, 336, 177, 577, 199, 116, 215, 235, 995, 167, 143, 870, 752, 106, 957, 399, 31, 109, 571, 414, 393, 805, 70, 593, 851, 57, 115, 659, 90, 827, 296, 553, 171, 365, 734, 695, 61, 286, 831, 768, 953, 575, 990, 997, 71, 854, 138, 966, 695, 926, 957, 969, 456, 395, 861, 504, 230, 262, 908, 477, 609, 47, 543, 152, 595, 841, 324, 966, 724, 813, 81, 792, 184, 396, 26, 984, 877, 725, 108, 2, 870, 50, 227, 183, 721, 566, 746, 805, 896, 923, 272, 509, 188, 474, 796, 892, 510, 235, 789, 99, 516, 383, 372, 908, 479, 757, 409, 674, 429, 85, 496, 596, 288, 713, 714, 535, 61, 172, 70, 248, 610, 952, 672, 301, 280, 248, 386, 318, 949, 316, 306, 50, 842, 223, 40, 805, 690, 885, 146, 662, 353, 125, 268, 418, 81, 51, 486, 756, 24, 481, 713, 839, 96, 34, 415, 927, 860, 390, 882, 704, 224, 723, 843, 71, 389, 766, 587, 926, 121, 549, 123, 321, 246, 710, 542, 14, 159, 52, 707, 532, 353, 814, 217, 109, 56, 837, 484, 296, 698, 409, 733, 981, 612, 172, 374, 572, 991, 317, 678, 516, 504, 987, 782, 344, 472, 140, 385, 814, 306, 647, 278, 903, 411, 447, 28, 683, 806, 236, 981, 88, 378, 865, 993, 916, 221, 634, 548, 337, 394, 370, 717, 132, 521, 85, 802, 456, 571, 631, 579, 773, 402, 351, 974, 290, 121, 3, 317, 962, 2, 783, 826, 337, 981, 23, 570, 335, 1, 858, 41, 580, 451, 328, 926, 332, 675, 832, 589, 724, 918, 61, 603, 320, 380, 167, 668, 200, 733, 98, 231, 460, 3, 503, 428, 232, 632, 303, 58, 887, 633, 475, 66, 813, 898, 778, 360, 307, 899, 25, 21, 631, 565, 496, 404, 154, 826, 288, 609, 573, 445, 606, 74, 920, 803, 83, 619, 986, 602, 364, 415, 741, 403, 163, 110, 416, 603, 71, 259, 392, 584, 339, 57, 162, 851, 459, 686, 929, 415, 907, 645, 49, 718, 632, 88, 327, 698, 547, 211, 368, 937, 291, 186, 264, 878, 436, 669, 632, 98, 179, 328, 698, 319, 74, 840, 12, 638, 264, 335, 344, 790, 85, 426, 61, 79, 993, 329, 374, 543, 402, 680, 921, 692, 406, 636, 284, 851, 517, 359, 638, 38, 395, 385, 598, 642, 48, 999, 76, 621, 592, 33, 429, 471, 408, 108, 72, 28, 233, 440, 272, 848, 857, 462, 966, 122, 898, 58, 933, 598, 253, 335, 371, 494, 757, 621, 136, 576, 961, 824, 774, 609, 476, 461, 495, 864, 430, 776, 276, 984, 892, 638, 519, 853, 463, 958, 434, 931, 999, 906, 774, 946, 949, 204, 280, 330, 732, 848, 23, 354, 169, 932, 602, 497, 949, 157, 559, 85, 838, 967, 62, 192, 592, 489, 971, 856, 760, 64, 79, 417, 982, 749, 666, 751, 150, 3, 842, 406, 381, 312, 469, 462, 324, 219, 424, 104, 682, 548, 700, 545, 287, 849, 252, 743, 914, 540, 0, 267, 160, 279, 478, 881, 19, 186, 375, 388, 404, 90, 511, 201, 66, 639, 392, 726, 568, 861, 509, 808, 363, 670, 129, 701, 672, 333, 248, 841, 855, 694, 53, 662, 561, 231, 248, 777, 174, 690, 760, 656, 513, 886, 976, 651, 135, 151, 881, 66, 260, 19, 766, 303, 810, 611, 879, 313, 895, 344, 129, 534, 285, 511, 806, 568, 714, 377, 563, 516, 971, 176, 647, 712, 390, 499, 307, 231, 336, 848, 808, 756, 856, 96, 846, 769, 64, 940, 139, 629, 209, 87, 900, 236, 116, 213, 926, 896, 444, 467, 748, 739, 90, 986, 151, 697, 561, 521, 654, 207, 561, 486, 165, 331, 678, 481, 830, 508, 152, 750, 178, 882, 862, 144, 274, 29, 353, 958, 309, 428, 398, 418, 328, 455, 742, 361, 325, 360, 161, 720, 713, 359, 635, 921, 911, 338, 825, 8, 735, 4, 130, 654, 74, 400, 241, 756, 539, 249, 560, 499, 18, 638, 694, 289, 596, 235, 608, 390, 278, 323, 700, 619, 170, 959, 534, 448, 14, 806, 830, 300, 43, 852, 941, 730, 58, 530, 317, 841, 363, 22, 783, 199, 72, 338, 212, 585, 770, 900, 11, 785, 125, 372, 97, 962, 691, 768, 336, 486, 370, 688, 755, 461, 171, 131, 998, 100, 610, 49]
)

✨ 7. Let's compute the encrypted result by calculating the dot product of the encrypted query and the encrypted database.
✨ c_result: (
Rows: 100
Cols: 1
Vector: [722, 347, 757, 223, 727, 295, 422, 806, 206, 595, 654, 364, 778, 74, 812, 688, 947, 214, 482, 672, 348, 468, 360, 757, 566, 579, 370, 121, 404, 252, 813, 641, 707, 473, 592, 812, 359, 449, 2, 713, 533, 54, 221, 83, 619, 179, 162, 814, 587, 573, 548, 357, 866, 820, 309, 97, 451, 621, 152, 958, 493, 345, 310, 149, 871, 121, 388, 206, 7, 613, 184, 332, 285, 406, 814, 726, 850, 372, 775, 750, 709, 697, 928, 436, 188, 295, 54, 807, 207, 409, 927, 943, 107, 943, 730, 532, 260, 935, 248, 987]
, 
Rows: 100
Cols: 10
Vector: [195, 847, 936, 349, 968, 531, 207, 80, 163, 257, 367, 813, 926, 493, 817, 367, 57, 359, 710, 302, 839, 974, 134, 594, 279, 89, 117, 390, 473, 619, 259, 614, 551, 244, 290, 547, 164, 437, 402, 318, 615, 535, 58, 53, 142, 265, 746, 5, 40, 892, 286, 614, 544, 177, 230, 901, 526, 535, 712, 23, 181, 491, 805, 431, 847, 673, 15, 893, 726, 503, 634, 55, 879, 822, 881, 169, 105, 755, 525, 642, 232, 908, 832, 352, 623, 803, 531, 998, 110, 7, 279, 536, 983, 809, 763, 297, 816, 189, 200, 249, 935, 563, 128, 997, 716, 734, 534, 733, 644, 457, 269, 622, 943, 466, 29, 643, 439, 327, 73, 531, 143, 984, 714, 951, 75, 862, 573, 503, 678, 762, 176, 637, 864, 674, 328, 92, 770, 626, 134, 469, 203, 357, 848, 249, 494, 16, 847, 411, 783, 11, 80, 784, 396, 237, 298, 917, 78, 265, 821, 748, 27, 563, 547, 415, 937, 229, 62, 631, 593, 9, 802, 826, 424, 173, 895, 310, 419, 190, 480, 489, 360, 280, 794, 851, 865, 225, 636, 276, 520, 611, 402, 602, 386, 826, 882, 291, 147, 72, 769, 141, 398, 387, 561, 715, 462, 686, 18, 187, 798, 816, 789, 537, 146, 156, 737, 154, 833, 804, 756, 360, 499, 146, 191, 351, 117, 284, 500, 606, 409, 276, 594, 737, 683, 874, 423, 844, 6, 109, 741, 630, 799, 383, 752, 893, 575, 128, 672, 820, 950, 326, 386, 626, 690, 568, 208, 894, 646, 422, 70, 141, 598, 80, 326, 595, 447, 14, 518, 242, 301, 126, 919, 885, 529, 991, 579, 470, 176, 998, 920, 194, 308, 872, 785, 324, 821, 638, 387, 142, 482, 4, 443, 183, 478, 135, 847, 623, 43, 776, 202, 154, 5, 85, 223, 478, 393, 75, 20, 39, 99, 891, 148, 535, 325, 465, 940, 659, 244, 396, 490, 339, 82, 62, 281, 695, 115, 692, 701, 513, 615, 794, 978, 111, 702, 667, 690, 735, 627, 961, 539, 213, 336, 528, 568, 51, 283, 333, 132, 838, 113, 678, 13, 267, 619, 637, 7, 444, 210, 801, 785, 262, 926, 255, 675, 446, 774, 422, 486, 53, 280, 200, 935, 437, 192, 678, 886, 172, 285, 249, 80, 49, 610, 569, 884, 825, 290, 879, 802, 216, 316, 393, 372, 697, 901, 83, 367, 746, 446, 8, 578, 561, 810, 136, 340, 678, 768, 261, 211, 578, 401, 188, 136, 44, 318, 565, 764, 308, 296, 874, 740, 938, 833, 85, 106, 21, 898, 684, 996, 138, 345, 400, 982, 606, 103, 786, 415, 681, 791, 939, 489, 352, 352, 192, 262, 730, 135, 126, 633, 975, 813, 511, 776, 137, 732, 767, 726, 70, 628, 439, 22, 897, 950, 929, 595, 508, 563, 52, 416, 367, 725, 401, 85, 293, 93, 95, 972, 446, 577, 865, 908, 411, 406, 602, 702, 478, 305, 271, 838, 484, 335, 789, 424, 531, 850, 298, 290, 445, 294, 548, 167, 113, 70, 512, 89, 223, 269, 140, 985, 424, 498, 673, 999, 883, 98, 871, 493, 40, 317, 909, 475, 6, 268, 60, 438, 296, 245, 551, 795, 503, 684, 102, 261, 599, 760, 234, 176, 332, 510, 271, 751, 543, 197, 321, 674, 408, 791, 781, 199, 689, 515, 708, 711, 993, 718, 737, 706, 734, 166, 805, 1, 613, 285, 322, 127, 31, 969, 638, 120, 437, 532, 182, 347, 139, 128, 145, 304, 978, 212, 722, 864, 39, 965, 550, 303, 232, 414, 42, 321, 425, 137, 57, 660, 282, 71, 686, 351, 0, 670, 204, 693, 295, 174, 753, 239, 481, 458, 765, 595, 187, 275, 685, 662, 756, 578, 960, 543, 184, 60, 35, 856, 91, 356, 266, 524, 873, 807, 546, 820, 273, 211, 164, 537, 996, 701, 550, 574, 957, 172, 317, 479, 731, 546, 715, 826, 308, 917, 453, 958, 360, 280, 11, 125, 633, 530, 351, 2, 321, 938, 9, 808, 476, 209, 876, 312, 674, 879, 840, 991, 855, 67, 704, 400, 515, 137, 421, 71, 194, 716, 483, 791, 529, 723, 734, 319, 240, 389, 382, 557, 583, 953, 832, 439, 490, 744, 221, 955, 177, 564, 353, 884, 637, 526, 432, 550, 157, 721, 584, 7, 483, 179, 665, 161, 601, 780, 48, 915, 981, 299, 490, 113, 240, 8, 598, 766, 573, 859, 737, 412, 393, 828, 22, 951, 984, 726, 742, 922, 666, 164, 976, 299, 734, 179, 124, 799, 773, 366, 825, 273, 111, 424, 0, 586, 820, 576, 30, 280, 275, 126, 999, 897, 850, 115, 353, 579, 143, 926, 684, 177, 678, 750, 338, 864, 322, 702, 9, 12, 600, 726, 388, 843, 633, 928, 874, 324, 409, 920, 992, 998, 834, 615, 333, 233, 690, 887, 197, 650, 571, 94, 439, 281, 191, 991, 136, 63, 320, 765, 710, 521, 965, 489, 5, 561, 251, 406, 145, 346, 887, 403, 234, 572, 815, 34, 396, 117, 918, 451, 912, 369, 597, 667, 377, 722, 570, 416, 44, 599, 234, 832, 293, 680, 461, 744, 780, 509, 156, 829, 188, 956, 905, 551, 56, 811, 820, 705, 604, 743, 75, 752, 710, 931, 633, 201, 56, 581, 941, 864, 870, 364, 582, 760, 613, 611, 251, 274, 173, 709, 557, 168, 512, 36, 240, 203, 586, 601, 894, 328, 276, 643, 112, 523, 320, 653, 665, 249, 962, 40, 9, 478, 729, 698, 121, 494, 557, 260, 271, 7, 358, 152, 44, 671, 717, 815, 264, 644, 363, 779, 863, 281, 144, 475, 519, 860, 582, 435, 880, 286, 417, 743, 458, 767, 597, 351, 213, 686, 350, 725, 264, 45, 937, 192, 376, 574, 479, 707, 348, 40, 849, 907, 672, 127, 445, 641, 219, 608, 268, 134, 984, 79, 213, 201, 708, 843, 319, 890, 436, 49, 18, 837, 480, 776, 413, 147, 550, 588, 676, 222, 102, 82, 776, 213, 55, 865, 810, 455, 901, 967, 525, 158, 466, 996, 566, 493, 977, 50, 477, 783, 118, 38, 647, 921, 469]
)

✨ 8. Let's calculate the decryption of the ciphertext c_result
✨ m1: 
Rows: 100
Cols: 1
Vector: [247, 245, 13, 305, 513, 4, 484, 978, 21, 240, 747, 239, 489, 714, 197, 748, 999, 233, 751, 271, 502, 782, 460, 497, 28, 272, 248, 232, 11, 302, 231, 738, 978, 519, 772, 523, 999, 204, 746, 16, 245, 462, 991, 228, 48, 513, 223, 304, 234, 255, 752, 771, 290, 721, 739, 258, 217, 782, 235, 258, 248, 240, 262, 508, 469, 271, 989, 217, 773, 207, 777, 558, 507, 19, 244, 258, 251, 211, 728, 245, 220, 780, 22, 733, 289, 748, 3, 503, 465, 559, 749, 943, 51, 561, 989, 204, 565, 227, 762, 710]


✨ 9. Let's scale the result by p / mod.
✨ m1_scaled: 
Rows: 100
Cols: 1
Vector: [1, 1, 0, 1, 2, 0, 2, 0, 0, 1, 3, 1, 2, 3, 1, 3, 0, 1, 3, 1, 2, 3, 2, 2, 0, 1, 1, 1, 0, 1, 1, 3, 0, 2, 3, 2, 0, 1, 3, 0, 1, 2, 0, 1, 0, 2, 1, 1, 1, 1, 3, 3, 1, 3, 3, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 0, 1, 3, 1, 3, 2, 2, 0, 1, 1, 1, 1, 3, 1, 1, 3, 0, 3, 1, 3, 0, 2, 2, 2, 3, 0, 0, 2, 0, 1, 2, 1, 3, 3]


✨ 10. The message vector m1_scaled should be equal to the db at the query vector query_row, query_col, showing that PIR works.
✨ db.get_query_element(5, 5): 0
✨ m1_scaled.get_query_element(5, 0): 0

✨ Are they the same? Did we get a correct retrieval? True
```

<br>
<br>

----


### references


* **[private information retrieval and its applications, sajani vithana et al.](https://arxiv.org/pdf/2304.14397.pdf)**
* **[practical private information retrieval, femi george olumofin](https://uwspace.uwaterloo.ca/bitstream/handle/10012/6142/Olumofin_Femi.pdf?sequence=1&isAllowed=y)**
* **[how practical is single-server private information retrieval?, sophia artioli](https://ethz.ch/content/dam/ethz/special-interest/infk/inst-infsec/appliedcrypto/education/theses/How_practical_is_single_server_private_information_retrieval_corrected.pdf)**
* **[applying private information retrieval to lightweight bitcoin clients, kaihua oin et al.](https://www.computer.org/csdl/proceedings-article/cvcbt/2019/366900a060/1cdOwKCMqXK)**



