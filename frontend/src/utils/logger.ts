// 📝 LunaBeyond AI Logger
// Centralized logging system

export enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3,
    FATAL = 4
}

export interface LogEntry {
    timestamp: string;
    level: LogLevel;
    message: string;
    data?: any;
    module: string;
}

export class Logger {
    private module: string;
    private debugMode: boolean;
    private logLevel: LogLevel;
    private logs: LogEntry[] = [];

    constructor(module: string, debugMode: boolean = false, logLevel: LogLevel = LogLevel.INFO) {
        this.module = module;
        this.debugMode = debugMode;
        this.logLevel = logLevel;
    }

    public debug(message: string, data?: any): void {
        this.log(LogLevel.DEBUG, message, data);
    }

    public info(message: string, data?: any): void {
        this.log(LogLevel.INFO, message, data);
    }

    public warn(message: string, data?: any): void {
        this.log(LogLevel.WARN, message, data);
    }

    public error(message: string, data?: any): void {
        this.log(LogLevel.ERROR, message, data);
    }

    public fatal(message: string, data?: any): void {
        this.log(LogLevel.FATAL, message, data);
    }

    private log(level: LogLevel, message: string, data?: any): void {
        if (level < this.logLevel) {
            return;
        }

        const logEntry: LogEntry = {
            timestamp: new Date().toISOString(),
            level,
            message,
            data,
            module: this.module
        };

        // Store log entry
        this.logs.push(logEntry);

        // Keep only last 1000 logs
        if (this.logs.length > 1000) {
            this.logs = this.logs.slice(-1000);
        }

        // Output to console
        this.outputToConsole(logEntry);
    }

    private outputToConsole(entry: LogEntry): void {
        const timestamp = entry.timestamp;
        const module = entry.module;
        const levelName = LogLevel[entry.level];
        const message = entry.message;

        const logMessage = `[${timestamp}] [${module}] [${levelName}] ${message}`;

        switch (entry.level) {
            case LogLevel.DEBUG:
                if (this.debugMode) {
                    console.debug(logMessage, entry.data || '');
                }
                break;
            case LogLevel.INFO:
                console.info(logMessage, entry.data || '');
                break;
            case LogLevel.WARN:
                console.warn(logMessage, entry.data || '');
                break;
            case LogLevel.ERROR:
                console.error(logMessage, entry.data || '');
                break;
            case LogLevel.FATAL:
                console.error(`🔴 ${logMessage}`, entry.data || '');
                break;
        }
    }

    public getLogs(level?: LogLevel): LogEntry[] {
        if (level !== undefined) {
            return this.logs.filter(log => log.level >= level);
        }
        return [...this.logs];
    }

    public clearLogs(): void {
        this.logs = [];
    }

    public setLogLevel(level: LogLevel): void {
        this.logLevel = level;
    }

    public setDebugMode(debugMode: boolean): void {
        this.debugMode = debugMode;
    }

    public exportLogs(): string {
        return JSON.stringify(this.logs, null, 2);
    }
}
