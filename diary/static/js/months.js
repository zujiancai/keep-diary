var all_months = [];
var selectedId = -1;
var navBarLength = 7; // Number of months to display in the navigation bar, minimum 7 and increment by 2

function prettyMonth(id, shorthand = false) {
  const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const full_month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  if (shorthand) 
    return month_names[all_months[id][1] - 1] + "." + all_months[id][0];
  else
    return full_month_names[all_months[id][1] - 1] + ' ' + all_months[id][0];
}

function appendMonth(navElem, id) {
  display_month = prettyMonth(id, true);
  if (id == selectedId) {
    return $(navElem).append("<li class=\"page-item active\"><span class=\"page-link\">" + display_month + "</span></li>");
  }
  else {
    return $(navElem).append("<li class=\"page-item\"><a class=\"page-link\" href=\"months?year=" + all_months[id][0] + "&month=" + all_months[id][1] + "\">" + display_month + "</a></li>");
  }
}

function appendDots(navElem, id) {
  return $(navElem).append("<li class=\"page-item\"><a class=\"page-link\" href=\"#\" onclick=\"renderNav(" + id + ")\">....</a></li>");
}

function updateSelectedId(curyear, curmonth) {
  for (let i = 0; i < all_months.length; i++) {
    if (all_months[i][0] == curyear && all_months[i][1] == curmonth) {
      selectedId = i;
      $('#monthTitle').html(prettyMonth(selectedId));
      $('#aboutText').html('This is a list of all diaries for ' + prettyMonth(selectedId) + '. There are totally ' + all_months.length + ' months from ' + prettyMonth(0) + ' to ' + prettyMonth(all_months.length - 1) + '.');
      break;
    }
  }
  return selectedId;
}

function renderNav(curid) {
  const max_id = all_months.length - 1;
  let $navElem = $('.pagination');
  $navElem.empty();
  if (max_id < navBarLength) {
    for (let i = 0; i <= max_id; i++) appendMonth($navElem, i);
  }
  else if (curid < navBarLength - 3) {
    for (let i = 0; i < navBarLength - 2; i++) appendMonth($navElem, i);
    appendDots($navElem, navBarLength - 1);
    appendMonth($navElem, max_id);
  }
  else if (curid > max_id - navBarLength + 3) {
    appendMonth($navElem, 0);
    appendDots($navElem, max_id - navBarLength + 1);
    for (let i = max_id - navBarLength + 3; i <= max_id; i++) appendMonth($navElem, i);
  }
  else {
    appendMonth($navElem, 0);
    appendDots($navElem, curid - navBarLength + 4);
    let curOffset = (navBarLength - 5) / 2;
    for (let i = curid - curOffset; i <= curid + curOffset; i++) appendMonth($navElem, i);
    appendDots($navElem, curid + navBarLength - 4);
    appendMonth($navElem, max_id);
  }
}

// Path: diary/static/js/months.js