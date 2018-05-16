document.add = () ->
  e = document.getElementById('iSymbol')
  $.getJSON('https://api.iextrading.com/1.0/stock/' + e.value + '/earnings', (data) ->
    e.value = ''
    tr = document.createElement('tr')
    addToTR(data.symbol)
    document.getElementById('titems').appendChild(tr)
  )

tagsToReplace = {
    '&': '&amp;'
    '<': '&lt;'
    '>': '&rt;'
}

replaceTag = (tag) ->
  return tagsToReplace[tag] || tag

escapeHtml = (s) ->
  return s.replace(/[&<>]/g, replaceTag)

addToTR = (tr, cont) ->
  td = document.createElement('td')
  td.innerHTML = escapeHtml(cont)
  tr.appendChild(td)
