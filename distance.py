#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
import requests
import itertools
import gzip

# 返回最长公共字符串的长度，和集合
def lcs(s1, s2):
    m = len(s1)
    n = len(s2)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s1[i-1] == s2[j-1]:
                c = counter[i-1][j-1] + 1
                counter[i][j] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(s1[i-c:i])
                elif c == longest:
                    lcs_set.add(s1[i-c:i])

    return longest, list(lcs_set)

def ucfirst(s):
	return s[0].upper() + s[1:]

def uclast(s):
	return s[0:len(s) - 1] + s[len(s) - 1].upper()

def ucfirst_alpha(s):
	match = re.match(r'([0-9]+)([a-z]{1})(.*)', s);
	if match:
		return match.group(1) + match.group(2).upper() + match.group(3)

	return None

def inc_last(s):
	match = re.match(r'^(.*)([0-9]+)$', s);
	if match:
		number = int(match.group(2)) + 1
		return match.group(1) + str(number)

	return None

def relocate_alpha(s):
	alpha  = None
	number = None

	match = re.match(r'^([0-9]+)([a-z]+)$', s)
	if match:
		return match.group(2) + match.group(1)
	
	match = re.match(r'^([a-z]+)([0-9]+)$', s)
	if match:
		return match.group(2) + match.group(1)

	return None

def show_reason(s1, s2, lcs_list):
	# Winnie1 -> winnie1
	if ucfirst(s1) == s2 or ucfirst(s2) == s1:
		return 'ucfirst'

	# 12345y -> 12345Y
	if uclast(s1) == s2 or uclast(s2) == s1:
		return 'ucfirst'

	# crazymom -> crazymom1
	if s1.startswith(s2):
		return 'suffix: ' + s1[len(s2)]
	elif s2.startswith(s1):
		return 'suffix: ' + s2[len(s1):]

	# spiderman -> 1spiderman
	if s1.endswith(s2):
		return 'prefix: ' + s1[0:len(s1) - len(s2)]
	elif s2.endswith(s1):
		return 'prefix: ' + s2[0:len(s2) - len(s1)]

	# 1997narek1997 -> 1997Narek1997
	if ucfirst_alpha(s1) == s2 or ucfirst_alpha(s2) == s1:
		return 'ucfirst_alpha'

	# m12345 -> 12345m
	if relocate_alpha(s1) == s2 or relocate_alpha(s2) == s1:
		return 'relocate_alpha'

	# xaiver4 -> xaiver5 
	if inc_last(s1) == s2 or inc_last(s2) == s1:
		return 'inc_last'

	return ''

def is_ascii(s):
    return all(ord(c) < 128 for c in s)   

def run(filename):
	with gzip.open(filename, 'rb') as f:
		data = json.loads(f.read())

		for key, rows in data.iteritems():
			for row in rows:
				distances = row['edit_distance']
				password  = row['password']

				for i in range(1, len(distances)):
					# 密码长度至少5个字符，且编辑举例小于等于2
					if distances[i] == 0 or distances[i] > 2 or len(password[i]) < 5:
						continue

					# 忽略 UNICODE
					if not is_ascii(password[i - 1]) or not is_ascii(password[i]):
						continue

					# 相同字符串至少占 60% 比例
					max_lcs, lcs_set = lcs(password[i - 1].lower(), password[i].lower())
					if max_lcs < len(password[i - 1]) * 0.6:
						continue

					reason = show_reason(password[i - 1], password[i], lcs_set)

					# print password[i-1], "\n", password[i], "\n"
					print '{0:<5} {1:<40} {2:<40} {3:<10}'.format(max_lcs, password[i - 1], password[i], reason)

if __name__ == '__main__':
	for arg in sys.argv[1:]:
		run(arg)


