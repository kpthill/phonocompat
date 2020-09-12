class LanguagesTable extends React.Component {
  constructor(props) {
    super(props);
  }

  phonemesForLang(lang) {
    if (!lang.phonemes) return "no phonemes";
    if (!Object.keys(lang.phonemes)) return "no keys";
    return Object.keys(lang.phonemes).join("");
  }

  renderLang(lang) {
    const me = this;
    return (
      <tr>
        <td className="tg-0pky">{lang.name}</td>
        <td className="tg-0pky">{lang.iso_code}</td>
        <td className="tg-0pky">TODO</td>
        <td className="tg-0pky">TODO</td>
        <td className="tg-0pky">{me.phonemesForLang(lang)}</td>
        <td className="tg-0pky">TODO</td>
        <td className="tg-0pky">TODO</td>
      </tr>
    );
  }

  render() {
    const me = this;
    return (
      <table >
        <tbody>
          <tr>
            <th className="tg-0pky">Language Name</th>
            <th className="tg-0pky">Language Code</th>
            <th className="tg-0pky">Speakers (MM)</th>
            <th className="tg-0pky">Rank</th>
            <th className="tg-0pky">Consonants</th>
            <th className="tg-0pky">Missing Consonants</th>
            <th className="tg-0pky">Extra Consonants</th>
          </tr>
          {Object.values(langs).map(me.renderLang.bind(me))}
        </tbody>
      </table>
    );
  }
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

  $("#english").on("click", function() {
    set_phonostring(languages["eng"]);
  });

  const languages_table_container = document.querySelector("#languages_table_container");
  ReactDOM.render(React.createElement(LanguagesTable), languages_table_container);
});

console.log("importing langs");
$.getJSON("most_spoken.json", function(data) {
  langs = data;
  console.log(langs["ben"].name);
  work();
});
