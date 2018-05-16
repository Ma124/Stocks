document.companyBy = stock ->
  $.getJSON('https://api.iextrading.com/1.0/stock/GOOG/earnings', data ->
    console.log(data)
  )