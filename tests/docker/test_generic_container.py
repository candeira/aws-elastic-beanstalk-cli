# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License'). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the 'license' file accompanying this file. This file is
# distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from ebcli.docker.generic_container import GenericContainer
from ebcli.objects.exceptions import NotFoundError, ValidationError
from mock import patch, Mock
from unittest import TestCase


MOCK_DESTINATION_DOCKERFILE = '/foo'


class TestGenericContainer(TestCase):
    def setUp(self):
        self.fs_handler = Mock()
        self.fs_handler.make_dockerfile = Mock()
        self.fs_handler.dockerrun = None
        self.container = GenericContainer(self.fs_handler, None, None, None)

    def test_constructor_no_dockerfile_or_dockerrun(self):
        self.fs_handler.dockerfile_exists = False
        self.fs_handler.dockerrun_exists = False

        self.assertRaises(NotFoundError, self.container.validate)

    @patch('ebcli.docker.generic_container.dockerrun.validate_dockerrun_v1')
    def test_constructor_dockerrun_validation_fail(self, validate_dockerrun_v1):
        self.fs_handler.dockerfile_exists = True
        validate_dockerrun_v1.side_effect = ValidationError

        self.assertRaises(ValidationError,self.container.validate)

    def test_containerize(self):
        self.fs_handler.dockerfile_exists = True
        container = GenericContainer(self.fs_handler, None, None)
        container._containerize()
        self.fs_handler.make_dockerfile.assert_called_once_with()
