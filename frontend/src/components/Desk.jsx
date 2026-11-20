function RuleList({ title, sheets }) {
  return (
    <section>
      <h3>{title}</h3>
      <ul className="rules">
        {sheets.map((sheet) => (
          <li key={sheet.name}>
            <strong>{sheet.name}:</strong>{" "}
            {sheet.rules.length === 0 ? "No requirement posted." : sheet.rules.join("; ")}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function Desk({ game, caseFile, busy, error, onDecide, onLeave }) {
  const requestNumber = Math.min(game.cases_judged_today + 1, game.cases_per_day);
  const folder = caseFile.rule_folder;

  return (
    <>
      <header className="topbar">
        <div>
          <p className="form-code light">Form MD-19 · Day file</p>
          <h1 className="brand">Bureaucrazy</h1>
        </div>
        <ul className="tally">
          <li>Day {game.current_day}</li>
          <li>
            Request {requestNumber} of {game.cases_per_day}
          </li>
          <li>
            Mistakes {game.mistakes_today} of {game.mistakes_allowed}
          </li>
        </ul>
      </header>
      <main className="desk-frame">
        <article className="sheet request-sheet">
          <p className="kicker">Request</p>
          <p className="sentence">{caseFile.sentence}</p>
        </article>
        <div className="columns">
          <article className="sheet">
            <p className="kicker">Posted rules</p>
            <RuleList title="Agencies" sheets={folder.organizations} />
            <RuleList title="Positions" sheets={folder.roles} />
          </article>
          <article className="sheet">
            <p className="kicker">Applicant file {caseFile.applicant.file_number}</p>
            <h2>{caseFile.applicant.full_name}</h2>
            <p>Age {caseFile.applicant.age}</p>
            <h3>Licenses</h3>
            {caseFile.applicant.certifications.length === 0 ? (
              <p className="empty">No licenses on file.</p>
            ) : (
              <ul>
                {caseFile.applicant.certifications.map((name) => (
                  <li key={name}>{name}</li>
                ))}
              </ul>
            )}
            <h3>Assets</h3>
            {caseFile.applicant.assets.length === 0 ? (
              <p className="empty">No assets declared.</p>
            ) : (
              <ul>
                {caseFile.applicant.assets.map((asset) => (
                  <li key={asset.name}>
                    {asset.name} × {asset.quantity}
                  </li>
                ))}
              </ul>
            )}
            <h3>Employment</h3>
            {caseFile.applicant.jobs.length === 0 ? (
              <p className="empty">No employment on record.</p>
            ) : (
              <ul>
                {caseFile.applicant.jobs.map((job) => (
                  <li key={`${job.organization}-${job.span}`}>
                    {job.organization}, {job.title} ({job.span})
                  </li>
                ))}
              </ul>
            )}
          </article>
        </div>
        <div className="stamp-row">
          <button
            className="stamp approve"
            type="button"
            disabled={busy}
            onClick={() => onDecide("approve")}
          >
            Approve
          </button>
          <button
            className="stamp deny"
            type="button"
            disabled={busy}
            onClick={() => onDecide("deny")}
          >
            Deny
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        <button className="text-button" type="button" onClick={onLeave}>
          Return to the lobby
        </button>
      </main>
    </>
  );
}
