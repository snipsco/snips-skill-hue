Philips Hue skill for Snips
===========================

|Build Status| |PyPI| |MIT License|


Installation
------------

The skill is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install snipshue

Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    skills:
      - package_name: snipshue
        class_name: SnipsHue
        pip: snipshue=
        params:
          hostname: PHILIPS_HUE_IP
          username: PHILIPS_HUE_USERNAME
          light_ids: [1, 2, 3, 4, 5, 6]
        intents:
          - intent: DeactivateObject
            action: "turn_off"
          - intent: ActivateLightColor
            action: "turn_on"
      

Usage
-----

The skill allows you to control `Philips Hue`_ lights. In order to use it, you need the IP address of your Hue Bridge, as well as the username:

.. code-block:: python

    from snipshue.snipshue import SnipsHue

    hue = SnipsHue(hostname, username, light_ids) 
    hue.turn_on()

Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skill-hue.svg
   :target: https://travis-ci.org/snipsco/snips-skill-hue
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipsowm.svg
   :target: https://pypi.python.org/pypi/snipsowm
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/snipshue
.. _`pip`: http://www.pip-installer.org
.. _`Philips Hue`: http://www2.meethue.com/
.. _`Snips`: https://www.snips.ai
.. _`OpenWeatherMap website`: https://openweathermap.org/api
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt
