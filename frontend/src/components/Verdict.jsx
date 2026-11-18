export default function Verdict({ verdict, busy, error, onContinue }) {
  const qualified = verdict.actual_outcome === "qualified";

  return (
    <>
      <header className="topbar">
        <div>
          <p className="form-code light">Form MD-19 · Decision</p>
          <h1 className="brand">Bureaucrazy</h1>
        </div>
        <p className="tally single">Day {verdict.day_number} review</p>
      </header>
      <main className="desk-frame">
        <article className="sheet">
          <p className={`verdict-mark ${verdict.correct ? "ok" : "bad"}`}>
            {verdict.correct ? "Correct" : "Mistake"}
          </p>
          <p className="kicker">{verdict.applicant_name}</p>
          <p className="sentence small">{verdict.sentence}</p>
          <p>
            You {verdict.player_decision === "approve" ? "approved" : "denied"} this request. The
            applicant was {qualified ? "qualified" : "not qualified"}.
          </p>
          <h2>{qualified ? "Every posted rule was met." : "Where the file fell short"}</h2>
          {verdict.failed_requirements.length === 0 ? null : (
            <ul className="rules">
              {verdict.failed_requirements.map((rule) => (
                <li key={rule}>{rule}</li>
              ))}
            </ul>
          )}
          {verdict.day_complete && (
            <section className="day-close">
              <h2>Day {verdict.day_number} is closed</h2>
              <p>Mistakes on the log: {verdict.mistakes_on_day}.</p>
            </section>
          )}
          <div className="stamp-row">
            <button className="stamp approve" type="button" disabled={busy} onClick={onContinue}>
              {verdict.day_complete ? "Back to the lobby" : "Next request"}
            </button>
          </div>
          {error && <p className="error">{error}</p>}
        </article>
      </main>
    </>
  );
}
