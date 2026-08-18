// Klinika tizimi uchun kichik JS yordamchilar
document.addEventListener('DOMContentLoaded', function () {
  // Xabarlarni (messages) 4 soniyadan keyin avtomatik yopish
  document.querySelectorAll('.alert-auto-dismiss').forEach(function (el) {
    setTimeout(function () {
      const alert = bootstrap.Alert.getOrCreateInstance(el);
      alert.close();
    }, 4000);
  });

  // Reyting yulduzchalarini tanlashda vizual effekt (agar mavjud bo'lsa)
  document.querySelectorAll('select[name="rating"]').forEach(function (select) {
    select.addEventListener('change', function () {
      console.log('Baho tanlandi:', select.value);
    });
  });
});
