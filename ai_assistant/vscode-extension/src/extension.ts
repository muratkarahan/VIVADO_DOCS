/**
 * Vivado FPGA Expert - VS Code Extension
 * Chat participant for Xilinx Vivado Design Suite
 */

import * as vscode from 'vscode';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

let ragServerProcess: ChildProcess | null = null;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('Vivado FPGA Expert extension activating...');
    
    // Output channel
    outputChannel = vscode.window.createOutputChannel('Vivado Expert');
    outputChannel.appendLine('🚀 Vivado FPGA Expert başlatılıyor...');
    
    // Chat participant
    const chatParticipant = vscode.chat.createChatParticipant(
        'vivado-fpga-expert.chat',
        chatHandler
    );
    
    chatParticipant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'icon.png');
    
    context.subscriptions.push(chatParticipant);
    
    // Commands
    context.subscriptions.push(
        vscode.commands.registerCommand('vivadoExpert.startServer', startRAGServer),
        vscode.commands.registerCommand('vivadoExpert.stopServer', stopRAGServer),
        vscode.commands.registerCommand('vivadoExpert.restartServer', restartRAGServer)
    );
    
    // Auto-start server
    const config = vscode.workspace.getConfiguration('vivadoExpert');
    if (config.get<boolean>('autoStart', true)) {
        startRAGServer();
    }
    
    outputChannel.appendLine('✅ Vivado FPGA Expert hazır! Chat\'te @vivado yazarak kullanın.');
    console.log('Vivado FPGA Expert extension activated');
}

/**
 * Chat handler
 */
async function chatHandler(
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
): Promise<void> {
    try {
        // Get user message
        const userMessage = request.prompt.trim();
        
        if (!userMessage) {
            stream.markdown('Lütfen bir soru sorun. Örnek: `@vivado AXI4-Lite nedir?`');
            return;
        }
        
        // Check for commands
        const command = request.command;
        
        if (command === 'search') {
            stream.markdown(`🔍 **Arama yapılıyor:** "${userMessage}"\n\n`);
        } else if (command === 'code') {
            stream.markdown(`💻 **Kod örneği hazırlanıyor:** "${userMessage}"\n\n`);
        } else if (command === 'explain') {
            stream.markdown(`📚 **Açıklama hazırlanıyor:** "${userMessage}"\n\n`);
        } else {
            stream.markdown(`💬 **Soru:** "${userMessage}"\n\n`);
        }
        
        // Progress
        stream.progress('Vivado dökümanları aranıyor...');
        
        // Call RAG system (simplified - actual implementation would use Python backend)
        const response = await queryRAGSystem(userMessage, command);
        
        // Send response
        stream.markdown(response);
        
        // Add references
        stream.markdown('\n\n---\n');
        stream.markdown('💡 **İpucu:** `/search`, `/code`, `/explain` komutlarını kullanarak daha spesifik sonuçlar alabilirsiniz.');
        
    } catch (error) {
        stream.markdown(`❌ **Hata:** ${error}`);
        outputChannel.appendLine(`Error: ${error}`);
    }
}

/**
 * Query RAG system
 */
async function queryRAGSystem(query: string, command?: string): Promise<string> {
    try {
        // MCP server'a HTTP request gönder
        const axios = require('axios');
        const serverUrl = 'http://localhost:5000/query';
        
        const response = await axios.post(serverUrl, {
            query: query,
            command: command,
            n_results: 5
        }, {
            timeout: 30000 // 30 saniye timeout
        });
        
        if (response.data.success) {
            // Başarılı yanıt
            let result = `**Vivado Expert Yanıtı:**\n\n${response.data.answer}\n\n`;
            
            // Kaynakları ekle
            if (response.data.contexts && response.data.contexts.length > 0) {
                result += `---\n\n**📚 Kaynaklar:**\n`;
                response.data.contexts.slice(0, 3).forEach((ctx: any, i: number) => {
                    result += `${i + 1}. ${ctx.file} (uygunluk: ${(ctx.relevance * 100).toFixed(1)}%)\n`;
                });
            }
            
            // Token kullanımı
            if (response.data.tokens) {
                result += `\n*Token kullanımı: ${response.data.tokens}*`;
            }
            
            return result;
        } else {
            return `❌ **Hata:** ${response.data.error || 'Bilinmeyen hata'}`;
        }
        
    } catch (error: any) {
        // Server bağlantı hatası
        if (error.code === 'ECONNREFUSED') {
            return `❌ **MCP Server'a bağlanılamıyor!**\n\nLütfen server'ı başlatın:\n\n\`\`\`powershell\ncd ai_assistant\npython vivado_mcp_server.py\n\`\`\`\n\nServer çalışıyor mu kontrol edin: http://localhost:5000/health`;
        }
        
        return `❌ **Hata:** ${error.message}`;
    }
}

/**
 * Start RAG server
 */
function startRAGServer() {
    if (ragServerProcess) {
        outputChannel.appendLine('⚠️ RAG server zaten çalışıyor');
        return;
    }
    
    const config = vscode.workspace.getConfiguration('vivadoExpert');
    const pythonPath = config.get<string>('pythonPath', 'python');
    
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Workspace bulunamadı');
        return;
    }
    
    const scriptPath = path.join(workspaceFolder.uri.fsPath, 'ai_assistant', 'vivado_mcp_server.py');
    
    outputChannel.appendLine(`🔄 RAG server başlatılıyor: ${scriptPath}`);
    
    ragServerProcess = spawn(pythonPath, [scriptPath], {
        cwd: path.join(workspaceFolder.uri.fsPath, 'ai_assistant')
    });
    
    ragServerProcess.stdout?.on('data', (data) => {
        outputChannel.appendLine(`[Server] ${data}`);
    });
    
    ragServerProcess.stderr?.on('data', (data) => {
        outputChannel.appendLine(`[Error] ${data}`);
    });
    
    ragServerProcess.on('close', (code) => {
        outputChannel.appendLine(`RAG server kapandı (exit code: ${code})`);
        ragServerProcess = null;
    });
    
    vscode.window.showInformationMessage('Vivado RAG Server başlatıldı');
}

/**
 * Stop RAG server
 */
function stopRAGServer() {
    if (!ragServerProcess) {
        outputChannel.appendLine('⚠️ RAG server çalışmıyor');
        return;
    }
    
    outputChannel.appendLine('🛑 RAG server durduruluyor...');
    ragServerProcess.kill();
    ragServerProcess = null;
    
    vscode.window.showInformationMessage('Vivado RAG Server durduruldu');
}

/**
 * Restart RAG server
 */
function restartRAGServer() {
    stopRAGServer();
    setTimeout(() => startRAGServer(), 1000);
}

export function deactivate() {
    stopRAGServer();
}
