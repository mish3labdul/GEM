# Public privacy notice — draft with marked blanks

**Status: DRAFT, not published, not legal advice.** Prepared 23 October 2026 for gate L09. It replaces the preview notice only after the owner supplies the facts below, a privacy decision-maker approves the wording, and a native Arabic reviewer checks the Arabic. Nothing here has been wired into the site; the live preview notice is unchanged.

**Marker convention.** `[… — PENDING]` means a fact nobody has confirmed. Do not guess a value: leave the marker and the notice stays unpublishable. This matches `../refined-preview-20261022/LAUNCH-INPUTS.json`.

## What the draft relies on, and how it was checked

| Statement in the notice | Basis | Checked |
|---|---|---|
| The brief tool runs in the browser and sends nothing | `website/remake/app.js` form handlers; `form-action 'none'` policy in the page and in `hosting/cloudflare/_headers` | Code and regression tests (blocked-script, no network navigation on submit) |
| Nothing is saved to browser storage | No `localStorage`/`sessionStorage` use in `app.js` | Code search |
| No cookies, analytics or tracking scripts | No such code in the build; no cookie-setting header in `_headers` | Code, headers, and the live `/en/` response on 23 Oct 2026 (no `Set-Cookie`, no third-party URLs in the HTML). Cloudflare can add its own cookies under some security settings; the owner should confirm none are enabled before the cookie sentence is published |
| Fonts and logo are served from the site itself | `@font-face` URLs are `/assets/*.woff2` | Code |
| The site is hosted on Cloudflare Pages | `hosting/cloudflare/README.md`, deployment records | Records; **provider name still to be confirmed by the owner** |
| Hosting logs, their access and their retention | **Not known** | Pending |
| Operator, contact, law, rights, response time | **Not known** | Pending |

If an enquiry-receiving service is ever added (milestone M10), the "Sending an enquiry" section must be added and the "sends nothing" statements rewritten before that service goes live.

---

## English

**Privacy notice — GEM website**
Last updated: [DATE OF PUBLICATION — PENDING]

### Who runs this website
This website is operated by [PUBLIC OPERATOR NAME — PENDING], [REGISTERED ADDRESS OR JURISDICTION — PENDING]. You can contact us about privacy at [PRIVACY CONTACT EMAIL — PENDING].

### What this website does
The website describes GEM's guest amenity and packaging concepts. It also contains a project-brief tool. Everything shown is a concept presentation; it is not a catalogue of goods available to order.

### The project-brief tool
The tool helps you write a project brief. It runs in your browser. **It does not send your brief to GEM or to any other service.** It asks for your name, company or property, email address, project location, area of interest and a project description. The website does not store what you type in your browser's storage; reloading or clearing the page removes it. Your browser may separately offer to autofill fields.

You can copy the brief to your clipboard or download it as a text file. Both stay on your device, and you decide whether and with whom to share them. Clearing the form does not delete a downloaded file or empty your clipboard.

Please leave out payment details, identity-document numbers, health information, confidential guest information and other sensitive personal data.

### Cookies, analytics and third parties
The website does not set cookies, and it does not use analytics, advertising or tracking tools. Its fonts and logo are served from the website itself, not from a third party.

### Hosting and technical logs
The website is hosted by [HOSTING PROVIDER — PENDING CONFIRMATION; RECORDS INDICATE CLOUDFLARE PAGES]. When your browser loads a page, the hosting service receives the technical information needed to deliver it, such as your IP address, the page requested, the time, and your browser type.
- What the hosting service records: [LOGGING SERVICES — PENDING]
- Who can access those records: [AUTHORIZED ACCESS — PENDING]
- How long they are kept: [RETENTION PERIOD — PENDING]
- Why: [PURPOSE, FOR EXAMPLE SECURITY AND RELIABILITY — PENDING]

### Your choices and rights
[RIGHTS AND APPLICABLE-LAW WORDING — PENDING, TO BE PROVIDED BY THE PRIVACY DECISION-MAKER]. To ask a question or make a request about information we hold, write to [PRIVACY CONTACT EMAIL — PENDING]. We aim to reply within [RESPONSE TIME — PENDING].

### Changes to this notice
We will update this notice and its date if the website's handling of information changes, for example if a way of sending enquiries is added. [HOW CHANGES ARE ANNOUNCED — PENDING]

---

## العربية

**إشعار الخصوصية — موقع GEM**
آخر تحديث: [تاريخ النشر — قيد التحديد]

### من يشغّل هذا الموقع
يشغّل هذا الموقع [اسم الجهة المشغّلة — قيد التحديد]، [العنوان المسجّل أو الاختصاص القضائي — قيد التحديد]. يمكنك التواصل معنا بشأن الخصوصية عبر [البريد الإلكتروني للخصوصية — قيد التحديد].

### ما الذي يقدّمه هذا الموقع
يعرض الموقع تصوّرات GEM لمستلزمات الضيوف والتغليف، ويتضمن أداة لإعداد موجز المشروع. كل ما يُعرض هو تصوّرات للعرض، وليس قائمة منتجات متاحة للطلب.

### أداة موجز المشروع
تساعدك الأداة على كتابة موجز لمشروعك، وتعمل داخل المتصفح. **لا ترسل الأداة موجزك إلى GEM ولا إلى أي خدمة أخرى.** تطلب الأداة الاسم، والشركة أو المنشأة، والبريد الإلكتروني، وموقع المشروع، ومجال الاهتمام، ووصف المشروع. لا يحفظ الموقع ما تكتبه في تخزين المتصفح؛ وتؤدي إعادة تحميل الصفحة أو مسحها إلى إزالته. وقد يقترح المتصفح تعبئة الحقول تلقائيًا بشكل مستقل.

يمكنك نسخ الموجز إلى حافظة جهازك أو تنزيله ملفًا نصيًا. يبقى كلاهما على جهازك، وأنت من يقرر مشاركتهما ومع من. لا يؤدي مسح النموذج إلى حذف الملف المنزّل ولا إلى إفراغ الحافظة.

نرجو عدم إدخال بيانات الدفع، أو أرقام وثائق الهوية، أو المعلومات الصحية، أو معلومات الضيوف السرية، أو غيرها من البيانات الشخصية الحساسة.

### ملفات الارتباط والتحليلات والأطراف الثالثة
لا يضع الموقع ملفات ارتباط، ولا يستخدم أدوات تحليل أو إعلان أو تتبّع. تُقدَّم الخطوط والشعار من الموقع نفسه وليس من طرف ثالث.

### الاستضافة والسجلات التقنية
يستضيف الموقع [مزوّد الاستضافة — قيد التأكيد؛ تشير السجلات إلى Cloudflare Pages]. عندما يحمّل متصفحك صفحة، تستلم خدمة الاستضافة المعلومات التقنية اللازمة لتقديمها، مثل عنوان IP، والصفحة المطلوبة، ووقت الطلب، ونوع المتصفح.
- ما تسجّله خدمة الاستضافة: [خدمات التسجيل — قيد التحديد]
- من يمكنه الوصول إلى هذه السجلات: [صلاحيات الوصول — قيد التحديد]
- مدة الاحتفاظ بها: [مدة الاحتفاظ — قيد التحديد]
- الغرض: [الغرض، مثل الأمان والموثوقية — قيد التحديد]

### خياراتك وحقوقك
[صياغة الحقوق والنظام المعمول به — قيد التحديد، يقدّمها المسؤول عن قرار الخصوصية]. للاستفسار أو لتقديم طلب بشأن معلومات نحتفظ بها، راسلنا على [البريد الإلكتروني للخصوصية — قيد التحديد]. نسعى إلى الرد خلال [مدة الرد — قيد التحديد].

### تغييرات هذا الإشعار
سنحدّث هذا الإشعار وتاريخه إذا تغيّرت طريقة تعامل الموقع مع المعلومات، كإضافة وسيلة لإرسال الاستفسارات. [كيفية الإعلان عن التغييرات — قيد التحديد]

---

## Review checklist before publication

1. Every `[… — PENDING]` / `[… — قيد التحديد]` marker replaced by a confirmed fact, or its sentence removed by the decision-maker.
2. Hosting provider named correctly and the logging facts match the provider's actual configuration.
3. Applicable-law and rights wording supplied by the privacy decision-maker; not drafted here.
4. Native Arabic review of the Arabic text, including that Latin terms (Cloudflare Pages, IP) read correctly in right-to-left layout.
5. Notice date set; page title changed from "Website Preview" to the public wording; the sentence about the preview removed.
6. Site build and `check.py` re-run with the new copy; Chromium and Firefox suites pass; privacy page reviewed in both languages at phone and desktop widths.
