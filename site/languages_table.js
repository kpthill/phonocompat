export class LanguagesTable extends React.Component {
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
