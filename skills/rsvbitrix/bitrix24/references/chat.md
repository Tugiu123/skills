# Chat and Notifications

Use this file for messenger dialogs, chats, history, notifications, and file delivery into chats.

## Separate `im.*` From `imbot.*`

Use `im.*` when the integration acts through normal IM REST methods:

- `im.message.add`
- `im.message.update`
- `im.message.delete`
- `im.chat.add`
- `im.chat.get`
- `im.chat.update`
- `im.chat.user.add`
- `im.chat.user.delete`
- `im.chat.user.list`
- `im.chat.leave`
- `im.dialog.get`
- `im.dialog.messages.get`
- `im.recent.list`
- `im.recent.get`
- `im.recent.unread`

Use `imbot.*` for bot/plugin scenarios. The previous OpenClaw channel plugin used:

- `imbot.message.add`
- `imbot.dialog.get`

Critical rule for `imbot.*`:

- bot registration must include `CLIENT_ID`
- persist that exact `CLIENT_ID`
- pass the same `CLIENT_ID` in every subsequent `imbot.*` call
- treat `CLIENT_ID` as a secret capability, not as a public identifier

Reason: Bitrix24 uses `CLIENT_ID` to ensure that arbitrary callers cannot control arbitrary bots. Only the bot creator should know it.

Historical integration note from the earlier Claw implementation:

- a stable `CLIENT_ID` derived from `md5(webhook)` was used
- that is a valid pattern if the value stays stable per bot and is not exposed

Do not mix `im.*` and `imbot.*` casually. Pick the family that matches the integration model.

## Bot Registration Note

If the workflow includes `imbot.register`:

- choose a deterministic `CLIENT_ID`
- save it next to the bot configuration
- reuse it for `imbot.message.add`, `imbot.message.update`, `imbot.message.delete`, `imbot.chat.sendTyping`, and other `imbot.*` methods

If the stored `CLIENT_ID` is lost, assume the bot control path is broken until the integration restores the same value or re-registers the bot correctly.

## Notifications

Confirmed notification methods:

- `im.notify.system.add`
- `im.notify.personal.add`
- `im.notify.read`

Important caveat from current MCP docs: both `im.notify.system.add` and `im.notify.personal.add` are documented as available only when called through an application. If a plain webhook flow fails with an auth-type error, re-check the access model and do not keep retrying blindly.

## Files Into Chat

Confirmed chat file method:

- `im.disk.file.commit`

It accepts either:

- `FILE_ID`
- `UPLOAD_ID`

and one of:

- `CHAT_ID`
- `DIALOG_ID`

Use this after a file already exists on Disk.

## Dialog Addressing

Common dialog formats:

- `123` for a direct dialog with user `123`
- `chat456` for group chat `456`
- `sg789` for a group or project chat

## Minimal Examples

Send a message:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}im.message.add.json" \
  -d 'DIALOG_ID=chat42&MESSAGE=Hello team'
```

Read dialog history:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}im.dialog.messages.get.json" \
  -d 'DIALOG_ID=chat42&LIMIT=20'
```

Send an existing Disk file to chat:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}im.disk.file.commit.json" \
  -d 'CHAT_ID=42&FILE_ID[]=5249&MESSAGE=Project files'
```

## Formatting Note

Bitrix24 chat rendering still relies heavily on BB-code conventions. If the surrounding integration already converts Markdown to BB-code, do not double-convert.

## Good MCP Queries

- `im message chat notify dialog recent`
- `imbot message`
- `im disk file commit`
