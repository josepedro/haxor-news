# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import print_function
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


class KeyManager(object):
    """Creates a Key Manager.

    Attributes:
        * manager: An instance of a prompt_toolkit's KeyBindingManager.
    """

    def __init__(self, set_color, get_color,
                 refresh_resources_and_options):
        """Initializes KeyManager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.

        Returns:
            None.
        """
        self.manager = None
        self._create_key_manager(set_color, get_color,
                                 refresh_resources_and_options)

    def _create_key_manager(self, set_color, get_color,
                            refresh_resources_and_options):
        """Creates and initializes the keybinding manager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.

        Returns:
            A KeyBindingManager.
        """
        assert callable(set_color)
        assert callable(get_color)
        assert callable(refresh_resources_and_options)
        self.manager = KeyBindingManager(
            enable_search=True,
            enable_abort_and_exit_bindings=True,
            enable_system_bindings=True,
            enable_auto_suggest_bindings=True)

        @self.manager.registry.add_binding(Keys.F2)
        def handle_f2(_):
            """Enables/Disables color output.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_color(not get_color())

        @self.manager.registry.add_binding(Keys.F5)
        def handle_f5(event):
            """Refreshes AWS resources.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            event.cli.run_in_terminal(refresh_resources_and_options)

        @self.manager.registry.add_binding(Keys.F10)
        def handle_f10(_):
            """Quits when the `F10` key is pressed.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            raise EOFError

        @self.manager.registry.add_binding(Keys.ControlSpace)
        def handle_ctrl_space(event):
            """Initializes autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            b = event.cli.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                event.cli.start_completion(select_first=False)
