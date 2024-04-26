const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var all_months = [];
var selectedId = -1;
var navBarLength = 7; // Number of months to display in the navigation bar, minimum 7 and increment by 2

function appendMonth(navElem, id) {
  display_month = month_names[all_months[id][1] - 1] + " " + all_months[id][0];
  if (id == selectedId) {
    return $(navElem).append("<li class=\"page-item active\"><span class=\"page-link\">" + display_month + "<span class=\"sr-only\">(current)</span></span></li>");
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
      $('#monthTitle').html(month_names[curmonth - 1] + " " + curyear);
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
