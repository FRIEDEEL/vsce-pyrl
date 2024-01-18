// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';


// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "pyrl" is now active!');
	let replaceLine = vscode.commands.registerCommand('pyrl.replaceLine',
	() => {
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const selection = editor.selection;
			const currentLine = editor.document.lineAt(selection.start.line);
			const lineContent=currentLine.text;

			// 调用 Python 脚本并传递当前行的内容
			const pythonScriptPath = path.join(context.extensionPath,'/src/python-script/supsubscript-replace.py');
			const pythonCommand = `python "${pythonScriptPath}" "${lineContent}"`;
			// const pythonCommand = `echo "${pythonScriptPath}$"`;
			cp.exec(pythonCommand, (error, stdout, stderr) => {
				if (error) {
					console.error(`Error: ${error.message}`);
					vscode.window.showErrorMessage(`Error: ${error.message}`);
				} else {
					// 将 Python 脚本的输出替换回当前行
					editor.edit((editBuilder) => {
						editBuilder.replace(currentLine.range, stdout.trim());
					});
				}
			});
		} else {
			vscode.window.showErrorMessage('No active text editor.');
		}
	});
	context.subscriptions.push(replaceLine);
}

// This method is called when your extension is deactivated
export function deactivate() {}
