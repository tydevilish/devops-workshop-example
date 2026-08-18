import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the escaped quotes inside class="user-replace" for the entire file
content = content.replace('class=\\"user-replace\\"', 'class="user-replace"')

data = """1    68319010001    นายกิตติคุณ  ชูบุญ
2    68319010002    นายไกรวิชญ์  อ้นเกษ
3    68319010005    นายจิรภัทร  ป่าไพร
4    68319010007    นายชลสิทธิ์  แสงปินตา
5    68319010008    นายชวนากร  ไชยวงค์
6    68319010009    นายชินดนัย  พรมแดง
7    68319010011    นายณัฏฐณวัฒน์  มานะกิจ
8    68319010012    นายตุลธร  เลาว้าง
9    68319010013    นายทวีศักดิ์  นำมา
10    68319010014    นายธนกร  มีทรัพย์
11    68319010015    นายธนกฤต  กุณะแสงคำ
12    68319010016    นายธนากร  สุนโท
13    68319010017    นายธีรภัทร  คำชุม
14    68319010019    นายนราวิชญ์  พิชัย
15    68319010020    นายบวรทัต  ไชยวงค์
16    68319010021    นายปี  สุขใจ
17    68319010022    นายพสิษฐ์  จงงามวิไล
18    68319010023    นายพัทธดนย์  กาชัย
19    68319010024    นางสาวภักจิรา  พากเพียร
20    68319010025    นายวรากร  ไชยยา
21    68319010026    นายสราวุฒิ  ชัยวงค์
22    68319010028    นายเสฎฐวุฒิ  ขาวสะอาด
23    68319010029    นายอดิชาติ  ใจสวน
24    68319010030    นายอนุวัฒน์  สมเดช
25    68319010031    นายนนทพัทธ์  เนตรผาบ
26    68319010032    นายธนกฤต  สุปัญญา
27    68319010033    นายกรวิชญ์  กองเงิน
28    68319010034    นายธีรเมธ  คำจา
29    68319010035    นายธนพรพรรณ  อภิชนภูริ
30    68319010036    นายผไทภักดิ์  อาจวิจิตร
31    68319010037    นายภัทรศัย  ใจพงค์
32    68319010038    นายศุภฤกษ์  อุดมกสพ
33    68319010062    นายจิตติพัฒน์  จันทะกี
34    68319010063    นายชลธี  เลี้ยงบุตร
35    68319010065    นายโชติกร  สุวรรณสาร
36    68319010066    นายคณาธิป  ฐานดี"""

table_rows = ""
for line in data.split('\n'):
    if not line.strip(): continue
    parts = line.split()
    seq = parts[0]
    id_str = parts[1]
    name = " ".join(parts[2:])
    port = "99" + id_str[-2:]
    table_rows += f"""            <tr>
              <td>{seq}</td>
              <td>{id_str}</td>
              <td>{name}</td>
              <td><code class="val">{port}</code></td>
            </tr>\n"""

replacement = """        <div class="callout warn">
          <span class="callout-icon">⚠️</span>
          <div>อย่าลืมเปลี่ยน <code><span class="user-replace">username</span></code> เป็น GitLab username ของคุณ (<strong>ต้องเป็นตัวพิมพ์เล็กทั้งหมด</strong> หากมีตัวพิมพ์ใหญ่ให้แก้เป็นตัวพิมพ์เล็กให้หมด) และ <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมายตามตารางด้านล่าง มิฉะนั้น Deploy จะ Error</div>
        </div>

        <div style="margin: 14px 0 0 46px; max-height: 400px; overflow-y: auto; border: 1px solid var(--border); border-radius: var(--radius);">
          <table class="var-table" style="margin: 0; width: 100%;">
            <thead style="position: sticky; top: 0; z-index: 1; background: var(--bg-code);">
              <tr>
                <th style="padding: 10px 16px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 1px solid var(--border);">ลำดับ</th>
                <th style="padding: 10px 16px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 1px solid var(--border);">รหัสนักศึกษา</th>
                <th style="padding: 10px 16px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 1px solid var(--border);">ชื่อ-นามสกุล</th>
                <th style="padding: 10px 16px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 1px solid var(--border);">Port (99xx)</th>
              </tr>
            </thead>
            <tbody>
""" + table_rows + """            </tbody>
          </table>
        </div>"""

target = """        <div class="callout warn">
          <span class="callout-icon">⚠️</span>
          <div>อย่าลืมเปลี่ยน <code><span class="user-replace">username</span></code> เป็น GitLab username ของคุณ และ <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมาย มิฉะนั้น Deploy จะ Error</div>
        </div>"""

content = content.replace(target, replacement)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
