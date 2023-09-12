const fs = require("fs");

const { loadPyodide } = require("pyodide");

async function generateRepodata() {
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  return pyodide.runPythonAsync(`
  import micropip
  await micropip.install('webgui_jupyter_widgets')
  micropip.freeze()
`);
}

generateRepodata().then((result) => {
  fs.writeFileSync('pyodide/repodata.json', result);
});
