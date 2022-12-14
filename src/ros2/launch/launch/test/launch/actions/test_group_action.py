# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the GroupAction action class."""

from launch import Action
from launch import LaunchContext
from launch.actions import GroupAction
from launch.actions import PopEnvironment
from launch.actions import PopLaunchConfigurations
from launch.actions import PushEnvironment
from launch.actions import PushLaunchConfigurations
from launch.actions import SetLaunchConfiguration

from temporary_environment import sandbox_environment_variables


def test_group_action_constructors():
    """Test the constructors for the GroupAction class."""
    GroupAction([])
    GroupAction([Action()])
    GroupAction([Action()], scoped=False)
    GroupAction([Action()], scoped=False, launch_configurations={'foo': 'FOO'})


@sandbox_environment_variables
def test_group_action_execute():
    """Test the execute() of the the GroupAction class."""
    lc1 = LaunchContext()

    assert len(lc1.launch_configurations) == 0
    assert len(GroupAction([], scoped=False).visit(lc1)) == 0
    assert len(lc1.launch_configurations) == 0

    assert len(lc1.launch_configurations) == 0
    result = GroupAction([]).visit(lc1)
    assert len(result) == 4  # push and pop actions, due to scope=True
    assert isinstance(result[0], PushLaunchConfigurations)
    assert isinstance(result[1], PushEnvironment)
    assert isinstance(result[2], PopEnvironment)
    assert isinstance(result[3], PopLaunchConfigurations)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 0

    assert len(lc1.launch_configurations) == 0
    result = GroupAction([], launch_configurations={'foo': 'FOO'}).visit(lc1)
    assert len(result) == 5  # push, set 1 launch_configurations, and pop actions
    assert isinstance(result[0], PushLaunchConfigurations)
    assert isinstance(result[1], PushEnvironment)
    assert isinstance(result[2], SetLaunchConfiguration)
    assert isinstance(result[3], PopEnvironment)
    assert isinstance(result[4], PopLaunchConfigurations)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 0

    assert len(lc1.launch_configurations) == 0
    result = GroupAction([], launch_configurations={'foo': 'FOO', 'bar': 'BAR'}).visit(lc1)
    assert len(result) == 6  # push, set 2 launch_configurations, and pop actions
    assert isinstance(result[0], PushLaunchConfigurations)
    assert isinstance(result[1], PushEnvironment)
    assert isinstance(result[2], SetLaunchConfiguration)
    assert isinstance(result[3], SetLaunchConfiguration)
    assert isinstance(result[4], PopEnvironment)
    assert isinstance(result[5], PopLaunchConfigurations)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 0

    assert len(lc1.launch_configurations) == 0
    PushLaunchConfigurations().visit(lc1)
    PushEnvironment().visit(lc1)
    lc1.environment['foo_to_test_launch_group'] = 'FOO'
    result = GroupAction([], scoped=False, launch_configurations={'foo': 'FOO'}).visit(lc1)
    assert len(result) == 1  # set 1 launch_configurations
    assert 'foo_to_test_launch_group' in lc1.environment
    assert isinstance(result[0], SetLaunchConfiguration)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 1  # still set after group was included
    assert 'foo_to_test_launch_group' in lc1.environment
    PopEnvironment().visit(lc1)
    PopLaunchConfigurations().visit(lc1)
    assert len(lc1.launch_configurations) == 0
    assert 'foo_to_test_launch_group' not in lc1.environment

    assert len(lc1.launch_configurations) == 0
    PushLaunchConfigurations().visit(lc1)
    result = GroupAction([Action()], scoped=False, launch_configurations={'foo': 'FOO'}).visit(lc1)
    assert len(result) == 2  # set 1 launch_configurations, then the 1 included actions
    assert isinstance(result[0], SetLaunchConfiguration)
    assert isinstance(result[1], Action)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 1  # still set after group was included
    PopLaunchConfigurations().visit(lc1)
    assert len(lc1.launch_configurations) == 0

    assert len(lc1.launch_configurations) == 0
    result = GroupAction([Action()], launch_configurations={'foo': 'FOO'}).visit(lc1)
    assert len(result) == 6  # push, set 1 launch_configurations, the 1 action, and pop actions
    assert isinstance(result[0], PushLaunchConfigurations)
    assert isinstance(result[1], PushEnvironment)
    assert isinstance(result[2], SetLaunchConfiguration)
    assert isinstance(result[3], Action)
    assert isinstance(result[4], PopEnvironment)
    assert isinstance(result[5], PopLaunchConfigurations)
    for a in result:
        a.visit(lc1)
    assert len(lc1.launch_configurations) == 0
