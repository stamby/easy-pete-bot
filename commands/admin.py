import discord
import re

regex = re.compile(
        '.[Aa][Dd][Mm][Ii][Nn]( |$)')

async def run(prefix_, message, db):
    c = db.cursor()

    permissions = message.channel.permissions_for(
            message.author)

    if not permissions.manage_channels \
            and not permissions.manage_messages \
            and not permissions.manage_guild:
        await message.channel.send(
                '''
The _%sadmin_ message is directed towards people who have _Manage Channels, Manage Messages_ or _Manage Server_ permission.
                ''' % prefix_)
        return

    await message.channel.send(
            embed=discord.Embed(
                title='MODERATION',
                colour=discord.Colour.gold(),
                description='''
**%sprune** (amount) or **%sprune** (user) (amount): Requires _Manage Messages_ permission. Delete messages from a channel, starting by the latest. If a user precedes the amount, delete messages from that user only.
Example: _%sprune @a user I don't like 100_
            ''' % (prefix_, prefix_, prefix_)))

    await message.channel.send(
            embed=discord.Embed(
                title='ENABLING AND DISABLING FEATURES',
                colour=discord.Colour.gold(),
                description='''
**%senable** or **%sdisable** (commands): Requires _Manage Channels_ permission. Enable or disable one or more features for the current channel. Valid features:
**greeting**: To send greeting messages to this channel.
**iam**: To reply to _%siam_ and _%siamnot_ on this channel.
**song**: Likewise for _%ssong._
**meme**: " for _%smeme._
**updates**: Updates about the bot.
All of them are disabled by default. Note that this means that they will not work, unless enabled.
Example: _%senable greeting iam_
            ''' % (
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_
                )))

    await message.channel.send(
            embed=discord.Embed(
                title='CHANGING THE WAY COMMANDS WORK',
                colour=discord.Colour.gold(),
                description='''
**%sset** (property) (value) or **%sset**: Requires _Manage Server_ permission. Define properties that change the way the bot behaves. If no property is given, show current values. Valid properties:
**welcome**: A greeting for when a user joins. Writing _@@USER@@_ in it will mention the user. @@TAG@@ will print the user's tag.
Example: _%sset welcome Welcome, @@USER@@!_ (default)
**farewell**: Likewise when someone leaves.
Example: _%sset farewell \*\*@@TAG@@\*\* has left the server._ (default)
**max\_deletions**: The maximum amount of messages that _%sprune_ may delete. The default value is 10.
Example: _%sset max\_deletions 100_
**role\_create**: Whether _%siam_ should create a non-existing role. If disabled, it has no effect. Value should be _true_ or _false._ Default value: _false._
Example: _%sset role\_create false_
**role\_cleanup**: Whether the bot should remove any unused roles. _True_ or _false._ Default value: _false._
**someone**: Whether _@someone_ is allowed. _True_ or _false._ Default: _true._
**meme\_filter**: Filter memes sent by _%smeme._ _True_ or _false._ Default: _true._
**filter\_profanity**: Filter swearing. _True_ or _false._ Default: _false._
Example: _%sset filter\_profanity true_
**filter\_invite**: Filter server invites. _True_ or _false._ Default: _false._
**filter\_mass\_mention**: Filter mass mentions. _True_ or _false._ Default: _false._
**filter\_action**: Choose an action for when the filter is activated. Valid values:
0: Take no action, 1: Drop a warning, 2: Warn, then delete message, 3: Delete message. Default value: _0._
Example: _%sset filter\_action 3_

For more information, please write _%sabout._
            ''' % (
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_,
                    prefix_
                )))

