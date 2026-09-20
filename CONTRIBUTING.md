# Contributing / المساهمة

Thank you for improving Download Organizer. Keep changes focused, local-first, and safe for user files.

1. Create a branch from `main`.
2. Install development tools with `python -m pip install -e ".[dev]"`.
3. Run `ruff check src tests` and `pytest -q`.
4. Add tests for behavior changes, especially filesystem safety cases.
5. Open a pull request explaining the user-visible behavior and risks.

Never add telemetry, destructive defaults, credentials, or code that silently overwrites user files.

شكرًا للمساهمة. اجعل التغييرات محددة وآمنة ومحلية، وأضف اختبارات لأي تغيير يمس الملفات. لا تضف تتبعًا أو أسرارًا أو سلوكًا افتراضيًا يحذف أو يستبدل ملفات المستخدم.

Author / المؤلف: Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2
