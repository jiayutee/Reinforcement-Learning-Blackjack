/* Presentation-only cue selection for accepted public-game state changes. */
(function (root) {
  function transitionCue(previous, current, command) {
    if (!previous || !current || !Number.isInteger(previous.revision) ||
        !Number.isInteger(current.revision) || current.revision !== previous.revision + 1) return null;
    const settled = current.phase === 'settled';
    function outcomeCue() {
      const profit = current.normalized_profit;
      if (!settled || !Number.isFinite(profit)) return null;
      return profit > 0 ? 'win' : profit < 0 ? 'loss' : 'push';
    }
    if (command === 'deal') return outcomeCue() || (settled ? null : 'deal');
    if (command === 'split') return outcomeCue() || (settled ? null : 'deal');
    if (command === 'hit' || command === 'double') return outcomeCue() || (settled ? null : 'hit');
    if (command === 'stand') return outcomeCue();
    return null;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {transitionCue};
  else root.PublicGameSoundEvents = {transitionCue};
})(typeof globalThis !== 'undefined' ? globalThis : this);
