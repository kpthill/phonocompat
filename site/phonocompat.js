function setDifference(a, b) {
  let difference = new Set(a);
  for (let elem of b) {
    difference.delete(elem);
  }
  return Array.from(difference);
}

class LanguagesTable extends React.Component {
  constructor(props) {
    super(props);
  }

  phonemesForLang(lang) {
    if (Object.keys(lang.phonemes).length === 0) return "---phoneme data not available---";
    if (!Object.keys(lang.phonemes)) return "no keys";
    return Object.keys(lang.phonemes).join("");
  }

  renderLang(lang) {
    const me = this;
    return (
      <tr key={lang.iso_code}>
        <td className="tg-0pky">{lang.rank}</td>
        <td className="tg-0pky">
          <a href="#" onClick={() => this.props.set_phonostring(Object.keys(lang.phonemes).join(""))}>
            {lang.name}
          </a>
        </td>
        <td className="tg-0pky">{lang.iso_code}</td>
        <td className="tg-0pky">{
          (lang.speakers / (1000*1000)).toLocaleString(undefined, {minimumFractionDigits: 1})
        }</td>
        <td className="tg-0pky">{me.phonemesForLang(lang)}</td>
        <td className="tg-0pky">{setDifference(this.props.phonostring, Object.keys(lang.phonemes)).join("")}</td>
        <td className="tg-0pky">{setDifference(Object.keys(lang.phonemes), this.props.phonostring).join("")}</td>
      </tr>
    );
  }

  render() {
    const me = this;
    return (
      <table >
        <tbody>
          <tr key="header">
            <th className="tg-0pky">Rank</th>
            <th className="tg-0pky">Language Name</th>
            <th className="tg-0pky">Language Code</th>
            <th className="tg-0pky">Speakers (MM)</th>
            <th className="tg-0pky">Consonants</th>
            <th className="tg-0pky">Missing Consonants</th>
            <th className="tg-0pky">Extra Consonants</th>
          </tr>
          {
            Object
              .values(langs)
              .sort((a, b) => { return a.rank - b.rank; })
              .map(me.renderLang.bind(me))
          }
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
