# Online-School-Homework-Server
*Client part:* https://github.com/solja484/Online-School-Homeworks

**Запити в БД (їх методи, список аргументів які вони повертають і які дані треба передати в main.py):**
* */getteacherinfo* - для особистого кабінету вчителя
* */getpupilinfo* - для особистого кабінету вчителя

-- вертаю назву школи і id щоб в особистих кабінетах було посилання на сторінку школи (0nclick - запит на сервер з id коли)
* */getschoolinfo* - для сторінки школи
* */getadmininfo* - для сторінки адміністраторів
* */editadmininfo*
* */editteacherinfo*
* */editpupilinfo*

**Помилки повертаються як параметр не err, а error**
---

**TODO:**
- [ ] Розбратись з фотографіями шкіл і як і де їх зберігати
- [ ] Повертати правильні помилки якщо вчитель чи учень намагаються змінити email на існуючий у іншого
- [x] Вертати порахований remaining time  в get_subjects_hometasks
- [x] зробити підрахунок "remain_time": '0' //TODO remaining time