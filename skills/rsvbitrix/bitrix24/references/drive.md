# Drive and Disk

Use this file for storage, folder, file, and external-link operations.

## Core Methods

Storages:

- `disk.storage.getlist`
- `disk.storage.get`
- `disk.storage.getchildren`
- `disk.storage.addfolder`
- `disk.storage.uploadfile`

Folders:

- `disk.folder.get`
- `disk.folder.getchildren`
- `disk.folder.addsubfolder`
- `disk.folder.uploadfile`
- `disk.folder.getexternallink`
- `disk.folder.deletetree`

Files:

- `disk.file.get`
- `disk.file.copyto`
- `disk.file.moveto`
- `disk.file.delete`

Chat handoff:

- `im.disk.file.commit`

## Working Rules

- Find file IDs from `disk.storage.getchildren` or `disk.folder.getchildren`.
- Use `disk.file.get` to inspect metadata such as `DOWNLOAD_URL`, `DETAIL_URL`, and parent IDs.
- Upload to a storage root with `disk.storage.uploadfile`.
- Upload directly into a folder with `disk.folder.uploadfile`.
- Use `im.disk.file.commit` only after the file already exists on Disk.

## Minimal Examples

List storages:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}disk.storage.getlist.json"
```

List root children of a storage:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}disk.storage.getchildren.json" \
  -d 'id=1'
```

Get file metadata:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}disk.file.get.json" \
  -d 'id=9043'
```

Upload to a storage root:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}disk.storage.uploadfile.json" \
  -d 'id=1&data[NAME]=document.txt&fileContent[0]=document.txt&fileContent[1]=<base64_content>'
```

## Download Note

`DOWNLOAD_URL` is only useful if the caller also satisfies the authentication requirements for the file.

## Good MCP Queries

- `disk storage folder file upload download`
- `disk external link`
- `im disk file commit`
