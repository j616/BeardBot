![BeardBot Logo](http://github.com/mossblaser/BeardBot/raw/master/logo.png "BeardBot")

A modular Python IRC bot with an assortment of amusing and useful functions.
Currently at a rather early stage in development.


Usage
-----
    $ python bot.py -s "server.example.com" -r "#channel" [[options] ...]
The bot will join the specified room with the name "BeardBot".

### Arguments
*   *-r --room*
	*   Channel to join
*   *-s --server*
	*   Server hostname
*   *-p --port*
	*   Port on server
*   *-P --password*
	*   Server password
*   *-n --name*
	*   Name to join with ("_" will be appended if name unavailable)
*   *-a --noadmin*
	*   No administrators. All users can access all features

Note:
The bot remembers settings etc. on a per-channel basis, this includes the
selection of loaded modules so don't forget to load them!

### First Start
On first start with admins, you will be prompted in the command line to provide
a username and password. These will then be used to identify you to the admin
module to enable admin features.


### Killing the bot
Send "die" in a PM to the bot. (Note: No security for this at present!)


### Loading/Unloading/Listing Modules
Module management must be done via private messages to the bot. The following
commands are available to facilitate this and are only available to
administrators when they are enabled:

*   Load specified module(s).

        modprobe modulename [[modulename] ...]

*   Unload the specified modules   

        rmmod modulename [[modulename] ...]

*   List available modules.

        lsmod

The loaded modules will be remembered on a per-channel basis and the server will
attempt to restart them on subsequent runs.


### Current Modules
The following modules are shipped with BeardBot (hopefully) ready for use.

#### admin
The module that provides an interface to load/unload modules (See the
section on loading/unloading/listing modules above for usage). It also provides
the following commands in private messages for managing administrators:

*   Identify self as an administrator.

        identify username password

*   Add an administrator.

        addadmin username password

*   Remove an administrator.

        rmadmin username
        
*   List administrators.

        lsadmin
        
*   Change administrators password.
        
        passwd username newpassword

As well as the following private message commands to make the bot ignore/listen
to given nicks:

*   Ignore a nick.
        
        addignore nick
        
*   Stop ignoring a nick.

        rmignore nick
        
*   List ignored nicks.

        lsignore


#### astersed
Applies corrections made by clients like:
    *correction
Using the most likely word they intended to correct. Only applies
corrections if it is 60% certain of the word to be corrected.

#### ball
Plays ball using actions. Throw Beardbot a ball with commands like the following (where beardbot is the name of the bot in the channel):

        /me bounces ball at beardbot

#### beardy
Jonathan Heathcote's `beardy' Markov chain generator. It collects messages
written by users (and will use logs made by the log module if it is loaded)
and produces markov chains which can then be used to generate sentences in
the style of the specified user using either 1st order or 2nd order chains.
Due to the fact most IM messages are short, 1st order messages are
preferable for variety and humour while 2nd order ones tend to be direct
quotations disappointingly often. Usage is as follows (where beardbot is the
name of the bot in the channel):

*   generate a sentence based on the your own messages

        beardbot: what do I sound like?

*   generate a sentence based on someone else's messages

        beardbot: what does username sound like?

*   switch to a 2nd order model

        beardbot: grow your beard

*   switch to a 1st order model

        beardbot: shave your beard

#### bucket
A simple game by Tom Nixon. Put something in, get something out.

*   put an item 'this item' into the bucket

        I put in this item

* find out who put in the last item

        Who put that in

#### cake
Did somebody mention cake? Well if they did, this module will print one of a
number of quotes if they did...

#### dominos
A dominos pizza (UK) delivery tracker. Use as follows where <Pizza ID> is the sequence of characters after ?=id in the pizza tracking url:

*   Track a dominos order
        
        Track pizza <Pizza ID>

#### german
Replaces letters in the supplied phrase to make it sound stereotypically german
when pronounced phonetically. Use as follows:

*   Translate phrase in a stereotypical german accent

        in german: This is very german phrase I have created
        
#### help
Currently experimental help function which uses docstrings. Awaiting further
work.

#### highscore
Keeps track of the daily high-score of the number of :D emoticons in one
message. Will announce high scores as they occur.
Other commands:
  
*   Reset the highscores

        beardbot: we are all sad

*   Print the leaderboard

        beardbot: who is the happiest of them all?
    
#### hyphen
Simply corrects users who forget to apply Randal Munroe's translation of
[hyphen](http://xkcd.com/37/)s one-word forwards when used in the form adjective-ass noun.

#### log
A logging feature. Keeps a log of the channel in an sqlite database and
provides access to data to other modules. Also features some querying
features:

*   Report whether a user said anything matching the regular expression
    provided. This function automatically appends .* to the start and end of
    the expression unless you start the regex with a /

        did username say regex.*search

*   As above but not limited to a particular user.

        who said regex.*search

*   Prints out the most recently said things on the channel.

        [in a pm] recent messages

#### metrolink
Tells you information about Manchester Metrolink:

* Get next trams at specified station
        Tram <station name>

* Get network status
        Tram

#### ping
A ping module. Ping a nick and time their reply.

*   Ping a person

        <nick>: ping

*   Ping a person with a custom timeout

        <nick>: ping <timeout>

*   Reply to a ping

        pong

#### reply
Reads a list of tab seperated regexes and replies from data/replyFile. When the
regex is matched in a channel message, the bot will say the reply. Note that
this module has replaced both the hokay and medibot modules previously supplied
with the bot. Running this module with hokay or medibot will result in duplicate
replies on regexes present in both.

#### sed
Provides sed-like regex substitution functionality for messages. Simply
write a sed-like substitution command in a message and beardbot will apply
it to the first of the last five messages that matches the expression. Eg:

    s/some(.*)/all \1/

Add the 'g' flag at the end to replace all occurrences.
Add the 'o' flag at the end to search in original messages only 
(ie, ones not generated by beardbot).

#### sms
Uses [tropo](http://tropo.com) to send a free text. Documentation to come.

#### spellingnazi
A spelling-nazi function. It will shout at users who misspell words. Note of
warning, this module is bloody annoying. If the spellcheck doesn't know a
word that it should you can correct it when it complains by saying:

    beardbot: yes I [your choice of expletives here] do

#### urltitle
Attempts to find urls in channel messages and then attempts to retrieve the
pagetitle before hopefully posting it on the channel

#### upstrack
An interface for the UPS package tracking system. 
*   To add a package to be tracked, send the bot a private message in the following form:

        Track package <tracking number>

*   To check the status of your package, send the following private message:

        Where's my package.

#### whatthehellguys
Keeps track of the tone of conversation in the channel and complains when it
gets worryingly bad. The module can be manipulated with the following commands
(where beardbot is the name of the bot in the channel):

*   Dissable automatic commenting on conversation tone
        
        beardbot: don't judge me!
        
*   Enable automatic commenting on conversation tone

        beardbot: tell us if this gets too bad
        
*   Print the current level of conversation cleanness
        
        beardbot: what the hell guys?

#### winning
Keeps track of who has claimed to have won and has been claimed to have won the
most in the channel. The following commandscan be used to control this module
(where beardbot is the name of the bot in your channel):

*   Reset the scores

        beardbot: none of us are winning
        
*   Turn on automatic reporting of scores
        
        beardbot: tell us if we win
        
*   Turn off automatic reporting of scores
        
        beardbot: we've won enough
        
*   Print the current winner

        beardbot: who is winning?

#### wtf
An acronym decryption module. For occasions when someone uses an obscure
acronym which you do not know simply say

    wtf is wtf

where the second wtf is your chosen acronym and the module will try to
answer your question. This uses the files found in data/ that can be modified by
the user as well as online sources. If you're unhappy with the first definition,
try the following:

    wtf else is wtf

#### xkcdhighscore
Keeps track of the number of times users post xkcd links. Will print out a
leaderboard on request:

    beardbot: xkcd leader board

Prints out the leaderboard of the number of times users have used xkcd
refrences and provided links.

Dependencies
------------
### Required
*   [irc](https://pypi.python.org/pypi/irc/)
*   [bcrypt](https://pypi.python.org/pypi/bcrypt/)

### Package Specific
#### upstrack
*   [packagetrack](https://pypi.python.org/pypi/packagetrack/)

#### urltitle
*   [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/)

#### spellingnazi
*   [pyenchant](https://pypi.python.org/pypi/pyenchant/)


About
-----
Developed By [Jonathan Heathcote](http://github.com/mossblaser) with significant
architecture contributions and some modules by [Tom Nixon](http://github.com/tomjnixon)
and various archetecture contributions, modules and some other disturbing
contributions by [James Sandford](http://github.com/j616)

All code GNU GPLv2, no warranties etc. etc.

### The Name
BeardBot is named after the `Beardy' Markov chain generator which inspired it.
Beardy was in turn named in honour of Markov's epic beard.
