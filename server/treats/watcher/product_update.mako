<%
    import locale
    locale.setlocale(locale.LC_MONETARY, 'ru_RU.utf8')
    c = locale.currency
%>

🏪*${shop}*
🍪*${title}*

*Цена раньше:* \
% if had_discount:
${c(price_before)} ~\(${c(price_old_before)}\)~
% else:
${c(price_before)}
% endif
\
*Цена сейчас:* \
% if discount:
${c(price_after)} ~\(${c(price_old_after)}\)~
% else:
${c(price_after)}
% endif
\
% if available:
*В наличии*
% else:
*Нет в наличии*
% endif

_Обновлено: ${timestamp} UTC_