import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Edit 1: update instruction to 3 points
old_desc = 'วางโค้ดด้านล่าง — ต้องแก้ 2 จุด: เปลี่ยน <code><span class="user-replace">username</span></code> เป็นชื่อ GitLab ของคุณ และเปลี่ยน <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมาย'
new_desc = 'วางโค้ดด้านล่าง — ต้องแก้ 3 จุด: เปลี่ยน <code><span class="user-replace">username</span></code> เป็นชื่อ GitLab ของคุณ, เปลี่ยน <code><span class="user-replace">my_website</span></code> เป็นชื่อ Container ของคุณ, และเปลี่ยน <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมาย'
content = content.replace(old_desc, new_desc)

# Edit 2: add user-replace span to my_website
old_container = '<span class="nm">container_name</span>: <span class="st">my_website</span>'
new_container = '<span class="nm">container_name</span>: <span class="st">"<span class="user-replace">my_website</span>"</span>'
content = content.replace(old_container, new_container)

# Edit 3: update callout warning
old_warn = '<div>อย่าลืมเปลี่ยน <code><span class="user-replace">username</span></code> เป็น GitLab username ของคุณ (<strong>ต้องเป็นตัวพิมพ์เล็กทั้งหมด</strong> หากมีตัวพิมพ์ใหญ่ให้แก้เป็นตัวพิมพ์เล็กให้หมด) และ <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมายตามตารางด้านล่าง มิฉะนั้น Deploy จะ Error</div>'
new_warn = '<div>อย่าลืมเปลี่ยน <code><span class="user-replace">username</span></code> เป็น GitLab username ของคุณ (<strong>ต้องเป็นตัวพิมพ์เล็กทั้งหมด</strong> หากมีตัวพิมพ์ใหญ่ให้แก้เป็นตัวพิมพ์เล็กให้หมด), เปลี่ยน <code><span class="user-replace">my_website</span></code> เป็น <strong>เลข 3 ตัวท้ายของรหัสนักศึกษา (ตัวอย่าง 683... คือเลขท้าย 3 ตัว) และตามด้วยชื่อภาษาอังกฤษของคุณ</strong> (เช่น <code>001kittikun</code>), และเปลี่ยน <code><span class="user-replace">99xx</span></code> เป็น Port ที่ได้รับมอบหมายตามตารางด้านล่าง มิฉะนั้น Deploy จะ Error</div>'
content = content.replace(old_warn, new_warn)

# Edit 4: step 14 header
old_step14_title = '<div class="step-title">ตรวจสอบ GitLab Username และ Port ให้ถูกต้อง</div>'
new_step14_title = '<div class="step-title">ตรวจสอบ GitLab Username, Container Name และ Port ให้ถูกต้อง</div>'
content = content.replace(old_step14_title, new_step14_title)

old_step14_desc = 'ก่อนไปขั้นต่อไป ตรวจสอบ 2 จุดในไฟล์ <code>docker-compose.yml</code> ให้แน่ใจ:'
new_step14_desc = 'ก่อนไปขั้นต่อไป ตรวจสอบ 3 จุดในไฟล์ <code>docker-compose.yml</code> ให้แน่ใจ:'
content = content.replace(old_step14_desc, new_step14_desc)

# Edit 5: table rows
old_table_row = """            <tr>
              <td>Port Number</td>
              <td><code><span class="user-replace">99xx</span>:80</code></td>
              <td><code class="val">9901:80</code> (ใส่เลขที่คุณได้)</td>
            </tr>"""
new_table_row = """            <tr>
              <td>Container Name</td>
              <td><code><span class="user-replace">my_website</span></code></td>
              <td><code class="val">001kittikun</code> (เลขท้าย 3 ตัว+ชื่ออิ้ง)</td>
            </tr>
            <tr>
              <td>Port Number</td>
              <td><code><span class="user-replace">99xx</span>:80</code></td>
              <td><code class="val">9901:80</code> (ใส่เลขที่คุณได้)</td>
            </tr>"""
content = content.replace(old_table_row, new_table_row)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
