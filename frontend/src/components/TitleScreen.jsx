export default function TitleScreen({ busy, error, onStart }) {
  return (
    <main className="desk-frame title-frame">
      <article className="sheet title-sheet">
        <p className="form-code">Form MD-19 · Rev. A</p>
        <h1>Bureaucrazy</h1>
        <p className="lede">Municipal Employment Desk</p>
        <p>
          A request arrives as one sentence. The rules are posted on the wall. The file is
          whatever the applicant brought. Approve the people who meet every rule. Deny the rest.
          A day has five requests.
        </p>
        <div className="stamp-row">
          <button className="stamp approve" type="button" onClick={onStart} disabled={busy}>
            Open the desk
          </button>
        </div>
        {error && <p className="error">{error}</p>}
      </article>
    </main>
  );
}
