EASY PETE BOT
=============

<p align="center">
  <a href="https://top.gg/bot/700307494580256768">
    <img src="https://top.gg/api/widget/700307494580256768.svg" alt="Easy Pete Bot" />
  </a>
</p>

A general-purpose bot for Discord with the following commands:

**.iam** (role name): Assign yourself a role. If the role doesn't exist, it may be created depending on settings.

**.iamnot** (role name): Remove a role from your user. If no users have the role anymore, the role may be removed depending on settings.

**.meme**: Send a random meme, straight from our repositories.

**.song**: Send a random song from our list of user-submitted songs.

**@someone**: Randomly mention someone on the server.

**.prune** (amount) or **.prune** (user) (amount): Requires _Manage Messages_ permission. Delete messages from a channel, starting by the latest. If a user precedes the amount, delete messages from that user only.
Example: _.prune @a user I don't like 100_

All features can be enabled, disabled or made to your preference with the help of _.enable,_ _.disable_ and _.set._ Additionally, the bot can welcome users and clean up unused roles, which may be coupled with the _.iam_ command for smoother role management.

A word filter may be enabled by means of _.set filter_profanity, .set filter_mass_mention and .set filter_invite_ followed by _1, 2_ or _3._ Please refer to the guide below to see what those mean.

The default dot prefix can be changed through _.set._

## More links

- [Add to Discord](https://discord.com/oauth2/authorize?client_id=700307494580256768&permissions=268561408&scope=bot)
- [See the guide](https://stamby.github.io/easy-pete-bot)
- [Join our community](https://discord.gg/VkvRqrv)

## How to host this bot

Create a file called `environment.sh` with the following variables defined in it:

- DB_NAME
- DB_PASSWORD
- DB_USER
- TOKEN
- TOKEN_BOTS_ON_DISCORD
- TOKEN_DISCORD_BOTS
- TOKEN_TOP_GG
