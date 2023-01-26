<%
    import locale
    locale.setlocale(locale.LC_MONETARY, 'ru_RU.utf8')
    c = locale.currency
%>

🏪<b>${shop}</b>
🍪<b>${title}</b>

<b>Цена раньше:</b> \
% if had_discount:
${c(price_before)} <s>(${c(price_old_before)})</s>
% else:
${c(price_before)}
% endif
\
<b>Цена сейчас:</b> \
% if discount:
${c(price_after)} <s>(${c(price_old_after)})</s>
% else:
${c(price_after)}
% endif
\
% if available:
<b>В наличии</b>
% else:
<b>Нет в наличии</b>
% endif

<i>Обновлено: ${timestamp} UTC</i>