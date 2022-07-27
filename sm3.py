import sys
import math
import time
import socket
import random
import base64
import binascii
from gmpy2 import invert
from random import randint
from os.path import commonprefix

index=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
iv = "7380166F4914B2B9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E"
T = (0x79cc4519, 0x7a879d8a)
index = "0123456789ABCDEF"
W68 = []
W64 = []

def ls(num, left):
    return (((num << left)&((1<<32)-1)) | (num >> (32 - left)))


def _T(x):
    return (T[1]) if x > 15 else (T[0])


def FF(x, y, z, n):
    return ((x & y) | (y & z) | (x & z)) if n > 15 else (x ^ y ^ z)


def GG(x, y, z, n):
    return ((x & y) | ((~x) & z)) if n > 15 else (x ^ y ^ z)


def P0(x):
    return (x ^ ls(x, 9) ^ ls(x, 17))


def P1(x):
    return (x ^ ls(x, 15) ^ ls(x, 23))


def padding(n, size,s):
    s=list(s)
    s.append('8')
    for i in range(0, n // 4):
        s.append("0")
    s=''.join(s)
    s+=hex(size)[2:].zfill(16).upper()
    return n,s

def message_extension(B):
    for i in range(0, 16):
        W68.append(int(B[(8 * i):(8 * i) + 8],16)%((1<<32)))

    for i in range(16, 68):
        W68.append(int(hex((P1(W68[i - 16] ^ W68[i - 9] ^ ls(W68[i - 3], 15))) ^ (ls(W68[i - 13], 7) ^ W68[i - 6])),16)%((1<<32)))

    for i in range(0, 64):
        W64.append(int(hex(W68[i] ^ W68[i + 4]),16)%((1<<32)))


def uint_to_str(num,k = 8) :
    s=""
    for i in range(0,k):
        s+=index[num % 16]
        num//=16
    return  s[::-1]

def iteration(V, Bi):
    irea = []
    irea1 = []
    for i in range(0, 8):
        t="0x"+V[8 * i: (8 * i) + 8]
        irea.append(int(t,16))
        irea1.append(irea[i])
    for i in range(0, 64):
        SS1 = ls((ls(irea[0], 12) + irea[4] + ls(_T(i), i % 32))%(1<<32), 7)
        SS2 = (SS1 ^ ls(irea[0], 12))
        t=(FF(irea[0], irea[1], irea[2], i)+irea[3])%((1<<32))
        TT1 = (FF(irea[0], irea[1], irea[2], i) + irea[3] + SS2 + W64[i])%(1<<32)
        TT2 = (GG(irea[4], irea[5], irea[6], i) + irea[7] + SS1 + W68[i])%(1<<32)
        irea[3] = irea[2]
        irea[2] = (ls(irea[1], 9))
        irea[1] = irea[0]
        irea[0] = TT1
        irea[7] = irea[6]
        irea[6] = ls(irea[5], 19)
        irea[5] = irea[4]
        irea[4] = P0(TT2)
    result = ""
    for i in range(0, 8):
        result += uint_to_str(irea1[i] ^ irea[i])
    return result.upper()


def SM3(m):
    size = len(m) * 4
    num = (size + 1) % 512
    t = 448 - num if num < 448 else 960 - num
    k ,m= padding(t,size,m)
    t=len(m)
    group_number = (size + 65 + k) // 512
    B = []
    IV = []
    IV.append(iv)
    for i in range(0, group_number):
        B.append(m[128 * i:128 * i + 128])
        message_extension(B[i])
        IV.append(iteration(IV[i], B[i]))
        W68.clear()
        W64.clear()
    digest = IV[group_number]
    return digest
