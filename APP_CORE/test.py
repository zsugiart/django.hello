from __future__ import unicode_literals

from django.test import TestCase
from SAN import *
from APP_CORE import urls

class SANTest(TestCase):

    def setUp(self):
        pass

    def test_01_AESCipher(self):
        key = "erebor"
        ac  = AESCipher(key)
        encoded = ac.encrypt("Far over the misty mountain cold. In dungeons deep, and caverns old")
        print "encoded = "+encoded
        raw = ac.decrypt(encoded)
        print "raw = "+raw

    def test_02_Reflection(self):
        members = Reflection.getMembers(urls)
        print "members: "
        print members
