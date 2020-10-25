import { LanguagesTable } from 'languages_table';

function setDifference(a, b) {
  let difference = new Set(a);
  for (let elem of b) {
    difference.delete(elem);
  }
  return Array.from(difference);
}

let langs;
let work = (function() {
  const languages = {
    "eng": "pbtdkɡmnŋfvθðszʃʒhɹlj"
  };

  function unique_chars(s) {
    let res = "";

    for (let i = 0; i < s.length; i++) {
      const c = s.charAt(i);
      if (res.indexOf(c) === -1) {
        res += c;
      }
    }

    return res;
  }

  let phonostring = "";
  window.phonostring = phonostring; // for inspectability

  function update_phonostring() {
    // update table
    $(".glyph").removeClass("selected");
    $(".glyph").filter(function(i, elem) {
      return phonostring.indexOf(elem.textContent) != -1;
    }).addClass("selected");

    // update input field
    $(".inventory_string").val(phonostring);

    renderTable(phonostring);
  }

  function set_phonostring(new_phonostring) {
    let chars = unique_chars(new_phonostring);
    phonostring = chars;
    update_phonostring();
  }

  $(".glyph").on("click", function() {
    console.log(this.textContent);
    $(this).toggleClass('selected');

    if ($(this).hasClass('selected')) {
      phonostring += this.textContent;
    } else {
      phonostring = phonostring.replace(this.textContent, '');
    }

    update_phonostring();
  })

  $(".inventory_string").on("input", function() {
    set_phonostring($(this).val());
  });

  const languages_table_container = document.querySelector("#languages_table_container");

  function renderTable(phonostring) {
    const languages_table = React.createElement(LanguagesTable, {phonostring: phonostring, set_phonostring:set_phonostring});
    window.languages_table = languages_table; // For debugging
    ReactDOM.render(languages_table, languages_table_container);
  }

  renderTable(phonostring);
});

console.log("importing langs");
$.getJSON("most_spoken.json", function(data) {
  langs = data;
  console.log(langs["ben"].name);
  work();
});
