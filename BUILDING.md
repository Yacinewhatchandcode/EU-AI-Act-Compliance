# Building Apps with OpenClaw

## Rules
1. **Never invent build commands.** `build_game`, `make_app`, etc. do not exist.
2. **Write code manually.** Use the `write` tool to create `index.html`, `script.js`, `style.css`.
3. **Use standard tools.** `npm install`, `npm run build` are okay.
4. **Deploy correctly.** Use `python deploy_vercel.py <dir>` to put it online.

## Example: "Build a Game"
Do not run `build_game`.
Instead:
1. Create directory: `mkdir my-game`
2. Write `my-game/index.html`:
   ```html
   <html><body><canvas id="game"></canvas><script src="game.js"></script></body></html>
   ```
3. Write `my-game/game.js` with the game logic.
4. Deploy: `python deploy_vercel.py ./my-game`
5. Send the resulting URL to the user.

## Example: "Open App"
Do not run `open_app_name`.
Instead:
1. `python desktop_control.py open_app "notepad"`
2. `python desktop_control.py find_window "Antigravity"`
