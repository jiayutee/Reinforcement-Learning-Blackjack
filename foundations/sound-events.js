/* Presentation events only: this module never changes rewards or game state. */
(function (root) {
  function transitionCue(previous, current) {
    if (!previous || !current || !Number.isInteger(previous.revision) ||
        !Number.isInteger(current.revision) || current.revision !== previous.revision + 1) return null;
    const hand = current.hand;
    if (!hand) return null;
    if (current.last_command === 'deal') return hand.done ? null : 'deal';
    if (!previous.hand || previous.hand.done ||
        !['hit', 'stand'].includes(current.last_command)) return null;
    if (hand.done) {
      if (current.reward === 1) return 'win';
      if (current.reward === -1) return 'loss';
      if (current.reward === 0) return 'push';
      return null;
    }
    return current.last_command === 'hit' ? 'hit' : null;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {transitionCue};
  else root.BlackjackSoundEvents = {transitionCue};
})(typeof globalThis !== 'undefined' ? globalThis : this);
