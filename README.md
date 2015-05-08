# b3-risc
risc is an IRC bot providing interaction with the UrbanTerror (ioq3) game through
the [BigBrotherBot](http://www.bigbrotherbot.net/) (b3) API.

## Required dependencies
The whole software requires some python libs before you can run it, you can install these using pip2 or easy_install:

* `tld`
* `requests`
* `lxml`
* `mechanize`

## Installation - risc standalone
Clone (master) into your home directory. You'll find two main folders
in b3-risc/src: `extplugins` and `risc`. The first one is used for b3
interaction, while the second is the main IRC bot. Both will interact.

This interaction requires some config obviously, like the servers addresses
you want risc to manage, their respective databases, a mysql user etc. This config
is located in the `b3-risc/src/risc/risc.ini` file. Keep an
original copy of it, and remove the comments.
It's quite easy to set it up if you follow the comments.

## Installation - riscb3 plugin
Follow these instructions if you want to install the riscb3 plugin on
some of your servers, since you can run risc without riscb3, with less
features obviously. This is basically the same setup as above.

Follow these instructions for each server you want riscb3 to run:

* Set up the `b3-risc/src/extplugins/conf/riscb3.ini` and remove the comments
* Copy `b3-risc/src/extplugins/riscb3.py` to `@b3/extplugins`
* Copy `b3-risc/src/extplugins/conf/riscb3.ini` to `@b3/extplugins/conf`
* Add `<plugin name="riscb3" config="@b3/extplugins/conf/riscb3.ini" />` to your `@b3/conf/b3.xml`

## Support
Simply mail me at Pr3acher777h@gmail.com for anything related to this project.
