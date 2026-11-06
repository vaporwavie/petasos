# Chat Input

The chat composer keeps message entry and its supporting controls inside one accessible, visually unified surface.

## Attachment capacity

The composer counts only attachments successfully prepared for a message toward its per-message limit.

[[src/renderer/src/screens/Chat/attachmentUtils.ts#processFiles]] validates each candidate before it occupies a slot, allowing later valid files to use capacity left by rejected files.

### Rejected files do not consume slots

A rejected file followed by a valid file can still fill the final available attachment slot.

[[src/renderer/src/screens/Chat/attachmentUtils.test.ts]] covers an oversized text file followed by a valid text file when one slot remains.

## Submission acknowledgement

The composer clears only an accepted submission snapshot. Refused Send, Quick Ask and slash selections keep their draft and staged files and show the rejection for retry.

[[src/renderer/src/screens/Chat/ChatInput.tsx#ChatInput]] awaits the parent admission callback, suppresses duplicate pending payloads, and preserves later edits or added files when an earlier submission succeeds. Composer resets and run/profile scope changes fence obsolete acknowledgements. Validated Legacy dispatch acknowledges admission without waiting for its streamed reply; native transport retains its existing handled-result contract.

### Refusal preserves text and attachments

Actual composer Send and Quick Ask keep the exact draft and prepared attachment after a rejected callback, display its error, and allow retry without dispatching the same pending payload twice.

### Accepted snapshots preserve newer drafts

An accepted earlier submission removes only its staged files and leaves a newer draft or file intact. An imperative composer reset also excludes delayed acknowledgements.
