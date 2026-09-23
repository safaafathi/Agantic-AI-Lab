# COSC726 — Lab 3 Decision Memo

## 1. What did you build, and which control caught which failure?

I built a ReAct-style customer-support agent driven by the
Qwen/Qwen2.5-1.5B-Instruct model.

The agent uses structured Pydantic argument models, a Step contract,
four execution gates, a dispatcher, and a bounded controller loop.

The controls are:

- Gate 1 checks whether the requested tool is known.
- Gate 2 validates the shape and values of tool arguments.
- Gate 3 checks whether referenced orders actually exist.
- Gate 4 checks whether a consequential approval request is supported
  by the required evidence and satisfies the policy threshold.
- The controller loop adds turn limits, token-budget limits,
  no-progress detection, escalation handling, and malformed-output
  handling.
- The fifth gate added in the Stretch checks whether the final answer
  is supported by the recorded trace.

The controls therefore protect both tool execution and, with Gate 5,
the final answer.


## 2. Which failure did no control catch, and why not?

The injection exercise exposed the main limitation of the first four
gates.

The problem can occur in the final natural-language answer rather
than in a tool call. Gates 1–4 validate the selected tool, its
arguments, the referenced order, and the evidence required for
consequential actions. They do not by themselves guarantee that
every claim in the final answer is supported by the trace.

This is why the fifth gate is useful: it moves validation to the
output boundary and checks whether the final answer is supported by
what the agent actually observed and recorded.


## 3. What would you add first, and why that first?

I would add output validation as the first additional control.

The existing gates already provide important protection around tool
execution. However, a model can still produce an unsupported final
answer without making an invalid tool call.

Therefore, validating the final answer against the trace closes a
trust boundary that the first four gates do not cover.


## 4. How often could the model not follow the contract?

The model used for the experiment was:

Qwen/Qwen2.5-1.5B-Instruct

The recorded repair counters were:

- fence_or_prose: 23
- retries: 36
- gave_up: 12

These numbers show that the model frequently needed recovery before
it could produce the required structured output. In particular,
12 cases reached the gave_up counter, meaning the model could not
produce a valid step after the available repair attempts.

This suggests that a 1.5B model should not be trusted to follow the
agent contract by itself in a production system. Structural
validation, retries, bounded execution, and explicit failure
handling are necessary.


## 5. Where does your agent still trust something it should not?

The agent still relies on the language model to correctly interpret
the customer's natural-language request and to select an appropriate
next action.

It also relies on the model to produce a truthful and useful final
answer. Although Gate 5 improves protection against unsupported
claims, language understanding itself remains a point of trust.

The experiment therefore shows that validation around tool execution
does not eliminate all risks created by model interpretation.


## 6. What did this lab not tell you?

This lab did not provide a complete measure of production
reliability.

The experiment used the Qwen/Qwen2.5-1.5B-Instruct model, which has
a different failure profile from a frontier model. The runs used
greedy decoding, which makes runs comparable within the session but
is not a complete reproducibility plan.

Each exercise was run once, so the results do not provide a variance
estimate. In addition, the five customer emails form a smoke test
rather than a statistically representative evaluation set.

Therefore, the results demonstrate concrete failure modes and the
value of the controls, but they should not be interpreted as a
production reliability estimate.
