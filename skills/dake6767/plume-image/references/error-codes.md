# Error Code Reference

## API Response Codes

| code | Type | Description | Suggested action |
|------|------|-------------|-----------------|
| `SUCCESS` | success | Operation succeeded | — |
| `CREATED` | success | Resource created | — |
| `VALIDATION_ERROR` | client error | Parameter validation failed | Check required parameters |
| `UNAUTHORIZED` | auth error | API Key invalid or missing | Check PLUME_API_KEY |
| `FORBIDDEN` | permission error | API Key disabled | Contact admin to enable Key |
| `NOT_FOUND` | client error | Resource not found | Verify task_id is correct |
| `INSUFFICIENT_CREDITS` | business error | Insufficient credits | Prompt user to top up |
| `CREDITS_ACCOUNT_NOT_FOUND` | business error | Credits account does not exist | Contact admin to create account |
| `CONCURRENT_MODIFICATION` | concurrency conflict | Optimistic lock conflict | Auto-retry |
| `UPLOAD_FAILED` | server error | R2 upload failed | Retry |
| `INTERNAL_ERROR` | server error | Internal error | Retry or contact admin |

## Task Status Codes

| status | Name | Description | Terminal |
|--------|------|-------------|---------|
| 1 | initialized | Task created, waiting to be processed | no |
| 2 | processing | Executor picked up, in progress | no |
| 3 | success | Task completed, result in `result` field | yes |
| 4 | failed | Task execution failed | yes |
| 5 | timeout | Task processing timed out (default 1 hour) | yes |
| 6 | cancelled | Task was cancelled | yes |

## Polling Recommendations

- Poll interval: 3 seconds
- Max poll attempts: 60 (3 minutes total)
- Terminal check: `status >= 3` means task has ended
- Success check: `status == 3`, result is in `data.result`
- Failure check: `status >= 4`, explain reason to user

## Common Error Scenarios

### 1. API Key not configured
```
Error: PLUME_API_KEY environment variable not set
Action: Remind user to set PLUME_API_KEY in OpenClaw configuration
```

### 2. Insufficient credits
```json
{ "success": false, "code": "INSUFFICIENT_CREDITS" }
Action: Inform user of insufficient credits, suggest topping up on the Portal
```

### 3. Image upload failed
```json
{ "success": false, "code": "VALIDATION_ERROR", "error": { "details": { "file": "..." } } }
Possible causes: file too large (>20MB), unsupported format, corrupted file
```

### 4. Task timeout
```
Still not complete after polling for 3 minutes
Action: Inform user that the task is taking longer than expected, suggest querying again later
```
