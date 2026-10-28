# This file is NOT imported. build_react_notebook.py copies its text into the
# single question notebook (Cell 4), after the prompt and the Calculator
# backend. It mirrors the loop and the printed report of the Complex Numbers
# 1cau notebooks (so_phuc, Sinh_them_cau_hoi/KLTN_D55_ReAct_Calculator_1cau).
#
# =====================================================================
# THE REAL ReAct LOOP (Thought -> Action -> Observation -> new Thought)
# =====================================================================
# Standard ReAct mechanism (Yao et al. 2022), also what agent frameworks do
# internally: set stop=["Observation:"] so the model MUST stop there, then the
# harness runs the real tool and inserts the real result, then generates on.
# This way the model NEVER invents a tool result.
STOP_STR = 'Observation:'
MAX_TOOL_CALLS = 25          # safety limit against endless loops (this type needs about 13 calls)
ACTION_INPUT_RE = re.compile(r'Action Input:[ \t]*(.*)')


def chay_react(chat_prompt, token_budget):
    """Return (full_text, total_tokens, number_of_tool_calls, tool_log)."""
    calculator = Calculator(free_unknowns=AN_SO_TU_DO)
    # Forced prefix: the model must continue from "<think>\nThought:", it can
    # no longer start with free prose (its most likely default behavior).
    full_text, total_tokens, n_calls, tool_log = '<think>\nThought:', 0, 0, []

    while True:
        remaining = token_budget - total_tokens
        if remaining <= 0:
            break

        # Every round the input is the prompt plus the WHOLE history (including
        # the Observations inserted by the harness), so the context keeps
        # growing. Recompute the room that is really left, or the model would
        # overflow MAX_MODEL_LEN in the middle of a round.
        model_input = chat_prompt + full_text
        room = MAX_MODEL_LEN - len(tok(model_input).input_ids) - 8
        n_new = min(remaining, room)
        if n_new <= 0:
            full_text += '\n[SYSTEM: out of context room, stopping.]\n'
            break

        sp_gen = SamplingParams(temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K,
                                presence_penalty=PRESENCE_PENALTY,
                                max_tokens=n_new, seed=SEED,
                                stop=[STOP_STR])
        out = llm.generate([model_input], sp_gen)[0].outputs[0]
        full_text += out.text
        total_tokens += len(out.token_ids)

        if out.stop_reason != STOP_STR:
            break   # the model finished by itself (Final Answer / EOS) or ran out of budget

        n_calls += 1
        match = None
        for mm in ACTION_INPUT_RE.finditer(out.text):
            match = mm          # take the LAST Action Input of the text just generated
        expression = match.group(1).strip() if match else ''

        if not expression:
            observation = ('ERROR: no "Action Input:" line found. Write a Thought, '
                           'then "Action: Calculator", then "Action Input: <expression>".')
            tool_log.append(('(no Action Input)', observation))
        else:
            result, error = calculator.evaluate(expression)
            if error:
                observation = (f'ERROR: {error}. Fix the syntax and try again '
                               '(sqrt() for roots, ** for powers, log() for logarithms, '
                               'Eq(a, b) to compare).')
                tool_log.append((expression, f'ERROR: {error}'))
            else:
                observation = result
                tool_log.append((expression, result))

        full_text += f'{STOP_STR} {observation}\n'

        if n_calls >= MAX_TOOL_CALLS:
            full_text += ('\n[SYSTEM: tool-call limit reached, give your Final Answer '
                          'now, with no further Action.]\n')
            input_final = chat_prompt + full_text
            room_final = MAX_MODEL_LEN - len(tok(input_final).input_ids) - 8
            sp_final = SamplingParams(temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K,
                                      presence_penalty=PRESENCE_PENALTY,
                                      max_tokens=max(1, min(token_budget - total_tokens, room_final)),
                                      seed=SEED)
            out_final = llm.generate([input_final], sp_final)[0].outputs[0]
            full_text += out_final.text
            total_tokens += len(out_final.token_ids)
            break

    return full_text, total_tokens, n_calls, tool_log


# =====================================================================
# RUN
# =====================================================================
prompt_text = PROMPT_TEMPLATE.replace('{de_bai}', DE_BAI)
chat_prompt = tok.apply_chat_template(
    [{'role': 'user', 'content': prompt_text}],
    tokenize=False, add_generation_prompt=True, enable_thinking=True)

prompt_tokens = len(tok(chat_prompt).input_ids)
print(f'Prompt: {prompt_tokens} tokens | room left for generation: {MAX_MODEL_LEN - prompt_tokens} '
      f'(budget {MAX_NEW_TOKENS})')
assert prompt_tokens + MAX_NEW_TOKENS + 256 <= MAX_MODEL_LEN, (
    'MAX_MODEL_LEN in Cell 3 is too small for this prompt: raise it and run Cell 3 again.')

t0 = time.time()
full_text, tong_tok, n_calls, nhat_ky = chay_react(chat_prompt, MAX_NEW_TOKENS)
giay = time.time() - t0


def lay_dap_an(t):
    for pat in (r'Final\s+Answer[^A-D]{0,20}([A-D])\b',
                r'\\boxed\{\s*(?:\\text\{\s*)?([A-D])\b',
                r'[Đđ]áp\s*án[^A-D]{0,15}([A-D])\b'):
        m = re.findall(pat, t)
        if m:
            return m[-1]
    return ''


chon = lay_dap_an(full_text)
dung = (chon == DAP_AN_DUNG)
n_loi = sum(1 for _, obs in nhat_ky if str(obs).startswith('ERROR'))

print('=' * 72)
print(f'Dap an dung: {DAP_AN_DUNG}   |   Model chon: {chon or "(khong chot duoc)"}   |   '
      f'{"DUNG" if dung else "SAI"}')
print('=' * 72)
print(f'Thoi gian: {giay:.0f}s | Tong token: {tong_tok}/{MAX_NEW_TOKENS} | '
      f'So luot goi Calculator: {n_calls} | Loi cu phap phai tu sua: {n_loi}')
print()
print('--- NHAT KY GOI TOOL (Action Input  ->  Observation) ---')
if nhat_ky:
    for i, (bt, obs) in enumerate(nhat_ky, 1):
        print(f'  [{i:2d}] {bt}')
        print(f'       -> {obs}')
else:
    print('  (!!) MODEL KHONG GOI TOOL LAN NAO - kiem tra lai phan huong dan tool trong prompt.')
print()

with open('/kaggle/working/full_response.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)
print(f'[DA GHI FILE] full_text ({len(full_text)} ky tu) -> /kaggle/working/full_response.txt')
print()
print('--- TOAN BO LOI GIAI (da chen Observation that) ---')
print(full_text)
