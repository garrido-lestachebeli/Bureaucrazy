import { useState } from "react";
import { decide, getCase, startGame } from "./api";
import Desk from "./components/Desk";
import TitleScreen from "./components/TitleScreen";
import Verdict from "./components/Verdict";

export default function App() {
  const [screen, setScreen] = useState("title");
  const [game, setGame] = useState(null);
  const [caseFile, setCaseFile] = useState(null);
  const [verdict, setVerdict] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function openDesk() {
    setBusy(true);
    setError("");
    try {
      const created = await startGame();
      const openCase = await getCase(created.game_id);
      setGame(created);
      setCaseFile(openCase);
      setVerdict(null);
      setScreen("desk");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function judge(decision) {
    setBusy(true);
    setError("");
    try {
      const result = await decide(game.game_id, decision);
      setGame(result.game);
      setVerdict(result);
      setScreen("verdict");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function continuePlay() {
    if (game.status !== "active") {
      setScreen("title");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const openCase = await getCase(game.game_id);
      setCaseFile(openCase);
      setScreen("desk");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  function leave() {
    setScreen("title");
    setError("");
  }

  return (
    <div className="office">
      {screen === "title" && <TitleScreen busy={busy} error={error} onStart={openDesk} />}
      {screen === "desk" && game && caseFile && (
        <Desk
          game={game}
          caseFile={caseFile}
          busy={busy}
          error={error}
          onDecide={judge}
          onLeave={leave}
        />
      )}
      {screen === "verdict" && verdict && (
        <Verdict verdict={verdict} busy={busy} error={error} onContinue={continuePlay} />
      )}
    </div>
  );
}
