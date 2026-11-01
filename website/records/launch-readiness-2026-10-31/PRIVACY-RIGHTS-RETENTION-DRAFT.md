# Privacy notice: rights and retention wording — DRAFT FOR ADVISER REVIEW

**Status: draft written by Claude Code on 31 Oct 2026. Not legal advice. Not on the site. Not approved.** It exists so the owner's adviser can edit and approve it; the site still shows the pending retention marker and a "Still being finalised" section. Evidence: the rights list follows the owner's 26 Oct draft paragraphs (`docs/GEM-Launch-Owner-Answers-2026-10-26.md`, A9), which cite the Saudi PDPL implementing regulation; the scope sentence is the owner's pasted law text (31 Oct, cut off mid-sentence). Nothing here was checked against the current law text by Claude; the adviser must verify every legal statement, the competent authority's name, and any article references.

## 1. Rights paragraph (replaces the "Still being finalised" rights sentence; new section "Your rights")

**English.** This notice applies to personal data processed in connection with this website. Under the Personal Data Protection Law of the Kingdom of Saudi Arabia and its implementing regulations, you may have the right to be informed about how your personal data is processed, to access it and obtain a readable copy, to request its correction or completion, and to request its destruction where the legal conditions are met. Where processing relies on your consent, you may withdraw that consent. You may also complain to the competent authority. To make a request, write to <contact@mish3l.com>. We may ask for proportionate information to verify your identity. We acknowledge requests within 5 working days and handle applicable requests without undue delay and within 30 calendar days, subject only to a lawful extension notified with reasons. Nothing in this notice limits any right that applicable law gives you.

**العربية.** يسري هذا الإشعار على البيانات الشخصية التي تُعالَج فيما يتعلق بهذا الموقع. بموجب نظام حماية البيانات الشخصية في المملكة العربية السعودية ولوائحه التنفيذية، قد يكون لك الحق في العلم بكيفية معالجة بياناتك الشخصية، والوصول إليها والحصول على نسخة مقروءة منها، وطلب تصحيحها أو إكمالها، وطلب إتلافها عند تحقق الشروط النظامية. وإذا استندت المعالجة إلى موافقتك، فيجوز لك العدول عنها. ولك أيضًا الحق في تقديم شكوى إلى الجهة المختصة. لتقديم طلب، يُرجى مراسلتنا على contact@mish3l.com. وقد نطلب معلومات متناسبة للتحقق من هويتك. نؤكد استلام الطلبات خلال خمسة أيام عمل، ونعالج الطلبات المنطبقة دون تأخر غير مبرر وخلال ثلاثين يومًا تقويميًا، مع مراعاة أي تمديد نظامي يُبلَّغ به مع بيان أسبابه. ولا يحدّ هذا الإشعار من أي حق يقرّره لك النظام المنطبق.

## 2. Retention paragraph (replaces `[RETENTION PERIOD — PENDING]` in "Hosting and logs")

Two versions. Use A if the owner and adviser accept principle-based wording; use B once the Cloudflare dashboard periods are confirmed (Claude's connector cannot read them).

**A, principle-based (English).** We keep personal data only for as long as needed for the purposes described in this notice and as the law requires. The enquiry tool on this site does not send your brief to us or store it, so we hold no copy of what you type into it. Technical request records are kept by our hosting and network provider for the periods that provider applies to each type of record, and we do not control those periods individually.

**A (العربية).** نحتفظ بالبيانات الشخصية بالقدر الزمني اللازم للأغراض الموضّحة في هذا الإشعار ووفق ما يتطلبه النظام. ولا ترسل أداة الاستفسار في هذا الموقع موجزك إلينا ولا تخزّنه، ولذلك لا نحتفظ بنسخة مما تكتبه فيها. وتحتفظ جهة الاستضافة والشبكة لدينا بسجلات الطلبات التقنية للمدد التي تطبّقها على كل نوع من السجلات، ولا نتحكم في هذه المدد على نحو منفرد.

**B, with periods (English; fill the brackets from the dashboard).** We keep personal data only for as long as needed for the purposes described in this notice and as the law requires. The enquiry tool does not send your brief to us or store it. Technical request records held by our hosting and network provider are kept for these periods: requests and visitors [__ days]; performance [__ days]; security events [__ days]; cache and origin records [__ days]; DNS queries [__ days]. Copies we export ourselves, if any: [none / __ days].

**B (العربية).** نحتفظ بالبيانات الشخصية بالقدر الزمني اللازم للأغراض الموضّحة في هذا الإشعار ووفق ما يتطلبه النظام. ولا ترسل أداة الاستفسار موجزك إلينا ولا تخزّنه. وتُحفظ سجلات الطلبات التقنية لدى جهة الاستضافة والشبكة لدينا للمدد الآتية: الطلبات والزوار [__ يومًا]؛ الأداء [__ يومًا]؛ الأحداث الأمنية [__ يومًا]؛ سجلات التخزين المؤقت والخادم الأصلي [__ يومًا]؛ استعلامات DNS [__ يومًا]. النسخ التي نصدّرها بأنفسنا، إن وُجدت: [لا توجد / __ يومًا].

## 3. Questions the adviser needs to settle
1. Is "Personal Data Protection Law ... and its implementing regulations" the right citation, and is the competent authority to be named in the notice (and if so, its exact name and contact)?
2. Are the rights listed complete and correctly worded for this processing, and should the notice say anything about transfers outside the Kingdom (provider processing locations)? The owner kept "our hosting and network provider" unnamed pending this.
3. Is principle-based retention wording (A) acceptable, or are stated periods (B) required?
4. Does the informational cookie strip (owner's option b) satisfy any consent requirement for `cf_clearance`, or is a different approach needed (for example, turning the Cloudflare feature off)?
5. Is a legal entity name, registration number or address required in the notice beyond "GEM, Riyadh, Saudi Arabia"?
6. Review the Arabic: it was written by Claude Code and has had no native review (D1).

## 4. How it goes on the site once approved
Edit `website/remake/content.mjs` (English and Arabic `privacySections`): add a "Your rights" / "حقوقك" section with paragraph 1; replace the retention marker in "Hosting and logs" with paragraph 2 (A or B); remove the "Still being finalised" section; set the publication date at launch. Then rebuild, run the validator and both browser suites, and confirm no bracketed `PENDING` or `قيد التحديد` markers remain in the built pages.
