# Security Policy

## Scope
Download Organizer moves local files. Data-loss prevention therefore has priority over convenience.

## Safe defaults
- Preview only unless `--apply` is explicitly supplied.
- No deletion, networking, telemetry, or execution of downloaded files.
- Symbolic links are ignored.
- Existing destinations are never overwritten.
- SHA-256 detects source changes between planning and application.
- Undo refuses changed destinations and occupied original paths.

## Reporting
Please report security problems privately to the repository owner through GitHub-supported private reporting channels when available. Do not publish sensitive proof-of-concept data or credentials in a public issue.

## Security note / ملاحظة أمنية
الأداة لا تُعد برنامج مكافحة فيروسات، ولا تعني بصمة SHA-256 أن الملف آمن؛ وظيفتها هنا هي التحقق من عدم تغير الملف أثناء عملية التنظيم.
