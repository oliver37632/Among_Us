from schematics.models import Model
from schematics.types import EmailType, StringType, IntType


class SingupValidator(Model):
    email = EmailType(serialized_name='email', required=True)
    password = StringType(serialized_name='passsword', required=True, min_length=8, max_length=15)
    nickname = StringType(serialized_name='nickname', required=True, min_length=3, max_length=10)


class LoginValidator(Model):
    nickname = StringType(serialized_name='nickname', required=True, min_length=3, max_length=10)
    password = StringType(serialized_name='password', required=True, min_length=8, max_length=15)


class CheckNickValidator(Model):
    nickname = StringType(serialized_name='nickname', required=True, min_length=3, max_length=10)


class SendEmailCodeValidator(Model):
    email = EmailType(serialized_name='email', required=True)


class CheckEmailCodeValidator(Model):
    email = EmailType(serialized_name='email')
    code = IntType(serialized_name='code', min_value=1111, max_value=9999)
