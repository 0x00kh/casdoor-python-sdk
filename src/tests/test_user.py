# Copyright 2023 The Casdoor Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import unittest

from src.casdoor import CasdoorSDK
from src.casdoor.user import User
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class UserTest(unittest.TestCase):
    def test_user(self):
        name = get_random_name("User")

        # Add a new object
        user = User.new(owner="admin", name=name, created_time=datetime.datetime.now().isoformat(), display_name=name)

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_user(user=user)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            users = sdk.get_users()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in users]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            user = sdk.get_user(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(user.name, name)

        # Update the object
        updated_display_name = "Updated Casdoor Website"
        user.displayName = updated_display_name
        try:
            sdk.update_user(user)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_user = sdk.get_user(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_user.displayName, updated_display_name)

        # Delete the object
        try:
            sdk.delete_user(user)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_user = sdk.get_user(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_user, "Failed to delete object, it's still retrievable")
