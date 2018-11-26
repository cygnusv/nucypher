"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""
import contextlib
import shutil

import pytest
from click.testing import CliRunner

from nucypher.config.characters import UrsulaConfiguration
from nucypher.utilities.sandbox.constants import MOCK_CUSTOM_INSTALLATION_PATH


@pytest.fixture(scope='module')
def click_runner():
    runner = CliRunner()
    yield runner


@pytest.fixture(scope='module')
def nominal_configuration_fields():
    config = UrsulaConfiguration(dev_mode=True)
    config_fields = config.static_payload
    del config_fields['is_me']
    yield tuple(config_fields.keys())
    del config


@pytest.fixture(scope='module')
def custom_filepath():
    _custom_filepath = MOCK_CUSTOM_INSTALLATION_PATH
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(_custom_filepath, ignore_errors=True)
    yield _custom_filepath
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(_custom_filepath, ignore_errors=True)
