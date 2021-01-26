from django.test import TestCase

# Create your tests here.
import uuid

ss = str(uuid.uuid4())
sss = ss.split('-', -1)[-1]
print(ss)
print(sss)
