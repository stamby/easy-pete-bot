import discord

async def run(message, db):
    c = db.cursor()

    permissions = message.channel.permissions_for(
            message.author)

    if not permissions.manage_channels \
            and not permissions.manage_messages \
            and not permissions.manage_guild:
        await message.channel.send(
                '''
The _.admin_ message is directed towards people who have _Manage Channels, Manage Messages_ or _Manage Server_ permission.
                ''')
        return

    await message.channel.send(
            embed=discord.Embed(
                title='MODERATION',
                colour=discord.Colour.gold(),
                description='''
**.prune** (amount) or **.prune** (user) (amount): Requires _Manage Messages_ permission. Delete messages from a channel, starting by the latest. If a user precedes the amount, delete messages from that user only.
Example: _.prune @a user I don't like 100_
            '''))

    await message.channel.send(
            embed=discord.Embed(
                title='ENABLING AND DISABLING FEATURES',
                colour=discord.Colour.gold(),
                description='''
**.enable** or **.disable** (commands): Requires _Manage Channels_ permission. Enable or disable one or more features for the current channel. Valid features:
**greeting**: To send greeting messages to this channel.
**iam**: To reply to _.iam_ and _.iamnot_ on this channel.
**song**: Likewise for _.song._
**meme**: " for _.meme._
**updates**: Updates about the bot.
All of them are disabled by default. Note that this means that they will not work, unless enabled.
Example: _.enable greeting iam_
            '''))

    await message.channel.send(
            embed=discord.Embed(
                title='CHANGING THE WAY COMMANDS WORK',
                colour=discord.Colour.gold(),
                description='''
**.set** (property) (value) or **.set**: Requires _Manage Server_ permission. Define properties that change the way the bot behaves. If no property is given, show current values. Valid properties:
**welcome**: A greeting for when a user joins. Writing _@@USER@@_ in it will mention the user in question.
Example: _.set welcome Welcome, @@USER@@!_ (default)
**farewell**: Likewise when someone leaves.
Example: _.set farewell @@USER@@ has left the server._ (default)
**max\_deletions**: The maximum amount of messages that _.prune_ may delete. The default value is 10.
Example: _.set max\_deletions 100_
**role\_create**: Whether _.iam_ should create a non-existing role. If disabled, it has no effect. Value should be _true_ or _false._ Default value: _false._
Example: _.set role\_create false_
**role\_cleanup**: Whether the bot should remove any unused roles. _True_ or _false._ Default value: _false._
**someone**: Whether _@someone_ is allowed. _True_ or _false._ Default: _true._
**meme\_filter**: Filter memes sent by _.meme._ _True_ or _false._ Default: _true._
**filter\_profanity**: Filter swearing. _True_ or _false._ Default: _false._
Example: _.set filter\_profanity true_
**filter\_invite**: Filter server invites. _True_ or _false._ Default: _false._
**filter\_mass\_mention**: Filter mass mentions. _True_ or _false._ Default: _false._
**filter\_action**: Choose an action for when the filter is activated. Valid values:
0: Take no action, 1: Drop a warning, 2: Warn, then delete message, 3: Delete message. Default value: _0._
Example: _.set filter\_action 3_

For more information, please write _.about._
            '''))

