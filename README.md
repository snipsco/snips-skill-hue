# Philips Hue skill for Snips

[![Build Status](https://travis-ci.org/snipsco/snips-skill-hue.svg)](https://travis-ci.org/snipsco/snips-skill-hue)
[![PyPi](https://img.shields.io/pypi/v/snipshue.svg)](https://img.shields.io/pypi/v/snipshue.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt)

## Installation

The skill is on [PyPI](https://pypi.python.org/pypi/snipshue), so you can just install it with [pip](http://www.pip-installer.org):

```sh
$ pip install snipshue
```

## Usage

### Snips Skills Manager

It is recommended that you use this skill with the [Snips Skills Manager](https://github.com/snipsco/snipsskills). Simply add the following section to your [Snipsfile](https://github.com/snipsco/snipsskills/wiki/The-Snipsfile):

```yaml
skills:
  - package_name: snipshue
    class_name: SnipsHue
    pip: snipshue=
    params:
      hostname: PHILIPS_HUE_IP
      username: PHILIPS_HUE_USERNAME
    intents:
      - intent: DeactivateObject
        action: "turn_off"
      - intent: ActivateLightColor
        action: "turn_on"
```      

### Standalone

The skill allows you to control [Philips Hue](http://www2.meethue.com/) lights. In order to use it, you need the IP address of your Hue Bridge, as well as the username:

```python
from snipshue.snipshue import SnipsHue

hue = SnipsHue() 
hue.turn_on()
```

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-skill-hue/blob/master/CONTRIBUTING.rst).

## Copyright

This skill is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE.txt](https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt) for more information.
