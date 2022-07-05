# PyCharm Tips
These tips are meant to help get PyCharm setup with additional dev tools to speed up development.

## Setup Save Actions
**Note:** `pre-commit` already does all of this format checking. Adding it to PyCharm just lets you see the updates automatically as you work.

An example of all File Watchers setup:
![File Watchers list with black and isort](/docs/assets/file_watcher_list.png)

For **Actions on Save**, you can have both `black` and `isort` set to **Any save**.

An example of **Actions on Save** configured with `black` and `isort`:
![Actions on Save with black and isort](/docs/assets/actions_on_save.png)

### Add `black`
1. Setup `black` by adding a new custom File Watcher and putting `black` as the program.
2. Use `$FilePath$` as both **Arguments** and **Output paths to refresh**.
3. Use `$ProjectFileDir$` as the **Working directory**.
4. Uncheck all the advanced options, because options like **Trigger the watcher regardless of syntax errors** will cause annoying error output windows from having run `black` while there are incomplete lines.

An example of the fully configured `black` File Watcher:
![Black File Watcher fully configured](/docs/assets/file_watcher_black.png)

### Add `isort`
1. Setup `isort` by adding a new custom File Watcher and putting `isort` as the program.
2. Use `$FilePath$` as both **Arguments** and **Output paths to refresh**.
3. Use `$ProjectFileDir$` as the **Working directory**.
4. Uncheck all the advanced options, because options like **Trigger the watcher regardless of syntax errors** will cause annoying error output windows from having run `isort` while there are incomplete lines.

An example of the fully configured `isort` File Watcher:
![Isort File Watcher fully configured](/docs/assets/file_watcher_isort.png)

## Setup Configurations
In PyCharm, configurations are how you can run and debug code within the IDE. As this is a Django project which has tests, 2 configurations are recommended. Reminder that a single configuration can be used for any of the modes, like _run_, _debug_, and _coverage_.

### Setup Django configuration
If you properly setup your `pyenv` virtualenv and installed the dependencies before ever opening the project in PyCharm, this configuration may already have been created.

1. In `/dionysus_service` create a `local_settings.py` file to live alongside `settings.py`. Have it import all of `settings.py` with
   1. ```python
      from dionysus_service.settings import *
      ```
   2. Include any settings you need to change for your local environment.
   3. **Note**: This file is already in the project `.gitignore` so it will not be committed.
2. In the configurations, hit the plus and select the **Django Server** configuration.
3. Ensure it is using the virtualenv from `pyenv` as the Python Interpreter.
4. Set an environment variable to point Django to use your `local_settings.py` like
   1. ```bash
      DJANGO_SETTINGS_MODULE=dionysus_service.local_settings
      ```
5. Save the configuration.

## Setup pytest configuration
This setup is important to being table to assure tests run before making your commits. GitHub Actions will run the tests as well, but running them locally just makes everything easier. It will also let you use the debugger to step through the code if something is not working as you expected.

1. In the configurations, hit the plus and select the **pytest** configuration.
2. Ensure it is using the virtualenv from `pyenv` as the Python Interpreter.
3. Set the **Script path** to point at the `/tests` folder.
4. Save the configuration.
