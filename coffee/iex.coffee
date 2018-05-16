document.add = () ->
  e = document.getElementById('iSymbol')
  $.getJSON('https://api.iextrading.com/1.0/stock/' + e.value + '/earnings', (data) ->
    e.value = ''
    document.getElementById('titems')
  )
