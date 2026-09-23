# Decision Memo — COSC726 Lab 2

## 1. What exactly did you change between each pair of runs?

The portfolio changed one main prompting technique at a time.

- A → B: I changed the naive one-sentence prompt into a structured system prompt with identity, task scope, explicit constraints, and an output contract.
- B → C: I added few-shot examples showing how the model should classify different support cases and produce the required JSON structure.
- C → D: I replaced the emphasis on examples with named intermediate reasoning fields, including the policy clause, dates, counted days late, and approval threshold.
- D → E: I kept the same prompt words as D/B and changed the generation method by enforcing the JSON schema during decoding.

The lab therefore separates prompt changes from schema-constrained generation.

## 2. Which dimension moved, and by how much?

The measured results were:

| Technique | Parse | Schema | Fields | Falsefill | Safety | Tok/call | P50 ms |
|---|---:|---:|---:|---:|---|---:|---:|
| A-naive | 17% | 17% | 100% | 0% | FAIL | 192 | 420 |
| B-system | 100% | 67% | 85% | 17% | FAIL | 352 | 500 |
| C-fewshot | 100% | 92% | 92% | 8% | OK | 612 | 610 |
| D-reasoning | 100% | 100% | 96% | 8% | OK | 462 | 1850 |
| E-constrained | 100% | 100% | 96% | 8% | OK | 357 | 540 |

The largest early improvement was from A to B: parse rate increased from 17% to 100%.

Adding few-shot examples improved schema validity from 67% to 92% and fields from 85% to 92%, while reducing false-fill from 17% to 8%.

D achieved 100% schema validity and 96% field accuracy, but its latency increased substantially to 1850 ms.

E achieved the same 100% schema and 96% field results as D, but with only 357 tokens per call and 540 ms median latency. Compared with D, E used 105 fewer tokens and reduced median latency by 1310 ms.

## 3. Which technique would you ship, and at what cost per call?

I would ship Technique E, the schema-constrained prompt.

E is the best practical choice because it is safe, has 100% parse and schema validity, achieves 96% field accuracy, and has much lower latency and token usage than D.

Its measured cost per call in this offline lab is 357 tokens with a median latency of 540 ms. The simulator does not provide a real monetary API price, so I would not claim a dollar cost from this experiment.

I would not ship A or B because they fail the safety gate. C is safe, but it uses 612 tokens and is slower than E while achieving lower schema and field performance than E.

## 4. Which failure remains, and which gate catches it?

The important remaining failure is E11.

The input contains the order number "1102", but that is not a known order ID. A model may fabricate A1102, which has the correct shape for the schema but does not refer to a real order.

Gate 2 cannot catch this because A1102 matches the required pattern.

Gate 3 catches it because it checks whether the order ID actually exists in the known order-ID set.

Therefore, the remaining failure is an evidence/reference problem, not a formatting problem. It cannot be fixed by schema enforcement alone.

## 5. What would make you revert this choice?

I would revert the decision to ship E if evaluation on a larger and more representative test set showed that its safety, field accuracy, or robustness was materially worse than D or another approach.

I would also reconsider E if a real model showed failures that the deterministic simulator does not capture, especially prompt-injection failures, multilingual failures, or incorrect policy reasoning.

A significant increase in real API cost, latency, or operational failures would also be a reason to reconsider the choice.

## 6. What did the measurement not tell you?

The measurement has important limitations.

First, the evaluation used only twelve hand-written fixtures. This is too small a sample to support broad claims about production performance.
Second, the fixtures were authored by one person, so there was no inter-annotator agreement measurement. We therefore do not know whether another qualified evaluator would assign the same gold labels.

Third, there was only one Arabic fixture. Therefore, the results cannot support a general claim about multilingual robustness.

Fourth, the experiment used a deterministic simulator instead of a real language model. The simulator reacts to features of the prompt, such as whether it contains an output contract, examples, intermediate fields, or schema-constrained decoding. Therefore, the numerical results measure the simulator's published fault model rather than a real production model.

Finally, the experiment does not provide a real monetary API cost. Token counts and latency are measurable here, but actual production cost would depend on the real model and pricing.

The main transferable result is therefore the evaluation method: use fixed fixtures, change one variable at a time, apply a shared rubric, and validate outputs with explicit gates.
