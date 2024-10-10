import pytest

from tools.configuring import ConfigKeys


def test_configuring_validators():
    admin_key = ConfigKeys.ADMIN_ROLE
    assert admin_key.value[1]('<@&12345678>')
    assert not admin_key.value[1]('@everyone')

