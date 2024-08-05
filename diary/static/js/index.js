const HISTORY_MAX_SIZE = 12;
let search_history = [];
let historyRaw = localStorage.getItem(SEARCH_HISTORY_NAME);
if (historyRaw && historyRaw.length > 0) {
  search_history = JSON.parse(historyRaw);
}

// Handle search request
function searchDiaries(inputKey) {
  /*
  $('.loading-shield').show();
  $.ajax({
    url: 'search-diaries?keyword=' + encodeURIComponent(inputKey),
    type: 'GET',
    success: function(data){ 
      $('.loading-shield').hide();
      $('#cardlist').html(data);
      populateSearchDropdown(inputKey);
    },
    error: function(data) {
      $('.loading-shield').hide();
      alert("Status: " + data.status + "\nError: " + data.statusText);
    }
  });*/

  search_history.unshift(inputKey);
  if (search_history.length > HISTORY_MAX_SIZE) {
    search_history.pop();
  }
  localStorage.setItem(SEARCH_HISTORY_NAME, JSON.stringify(search_history));
  updateSearchHistoryMenu();
}

// Populate search dropdown menu
function updateSearchHistoryMenu() {
  if (search_history && search_history.length > 0) {
    let historyElement = $('#searchHistoryMenu');
    historyElement.empty();
    search_history.forEach(h => {
      historyElement.append('<li><a class="dropdown-item" href="#" onclick="searchDiaries(\'' + h  + '\');">' + h + '</a></li>');
    });
  }
}

// Path: diary/static/js/index.js