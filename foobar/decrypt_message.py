import base64

MESSAGE = '''
DEgSGRAHCxcESEFWU0MJFhIOFUtfREkHGAMNCRIDGwFQT1tMVAEdEBIKDAkXQ0JEUAoHChwWGhdQ T1tMVA0ABwUKBQURCAtDW09GDRAMBwEBCgwJHRBJRE1PRhkdCAEHHAoFS19ESRYWDQMFBxdJRE1P Rh8SAgtDW09GChwLSURNT0YbGgpPQwo=
'''

KEY = 'woalsdnd'

result = []
for i, c in enumerate(base64.b64decode(MESSAGE)):
    result.append(chr(ord(c) ^ ord(KEY[i % len(KEY)])))

print ''.join(result)