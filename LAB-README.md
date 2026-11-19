# Serverless-for-Iran Lab

این شاخه برای آزمایش‌های جدا از نسخه پایدار است.

## Subscription آزمایشی PattNG

`https://raw.githubusercontent.com/abolfazlkakavand121-a11y/Serverless-for-Iran/lab/profiles-v1/Subscription/Serverless-Lab.json`

این subscription سه پروفایل اصلی v64 را بدون تغییر نگه می‌دارد و دو پروفایل آزمایشی نیز اضافه می‌کند:
- `Serverless-v64-fragA-lab-oob-fragA`
- `Serverless-v64-fragB-lab-oob-fragB`

در دو پروفایل آزمایشی فقط `dialMode: oob.0,0` به سه outbound مبتنی بر TLS Fragment اضافه شده است: `tcp-fragment-tls`, `tcp-fragment-tls-cloudflare`, `tcp-fragment-tls-x`.

DNS bootstrap و `tls-repack-dns` عمداً OOB نشده‌اند. این تغییر صرفاً آزمایشی است و هنوز روی شبکه واقعی/گوشی تأیید نشده؛ در صورت بروز مشکل از سه پروفایل اصلی استفاده کنید.

## اعتبارسنجی

Workflow در هر push یا pull request، JSON subscription را parse می‌کند و ارجاع outboundها را بررسی می‌کند. این بررسی جایگزین اعتبارسنجی runtime توسط Xray-core یا تست شبکه نیست.
