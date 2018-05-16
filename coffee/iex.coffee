document.companyBy = (stock) ->
  $.getJSON('https://api.iextrading.com/1.0/stock/' + stock + '/earnings', (data) ->
    console.log(data)
  )
