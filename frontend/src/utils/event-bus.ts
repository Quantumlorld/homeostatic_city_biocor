// 🚀 LunaBeyond AI Event Bus
// Centralized event management system

type EventHandler = (data?: any) => void;
type EventMap = Map<string, Set<EventHandler>>;

export class EventBus {
    private events: EventMap;
    private onceEvents: Map<string, Set<EventHandler>>;

    constructor() {
        this.events = new Map();
        this.onceEvents = new Map();
    }

    public on(event: string, handler: EventHandler): void {
        if (!this.events.has(event)) {
            this.events.set(event, new Set());
        }
        this.events.get(event)!.add(handler);
    }

    public off(event: string, handler: EventHandler): void {
        const handlers = this.events.get(event);
        if (handlers) {
            handlers.delete(handler);
            if (handlers.size === 0) {
                this.events.delete(event);
            }
        }
    }

    public once(event: string, handler: EventHandler): void {
        if (!this.onceEvents.has(event)) {
            this.onceEvents.set(event, new Set());
        }
        this.onceEvents.get(event)!.add(handler);
    }

    public emit(event: string, data?: any): void {
        // Regular event handlers
        const handlers = this.events.get(event);
        if (handlers) {
            handlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`Error in event handler for '${event}':`, error);
                }
            });
        }

        // Once event handlers
        const onceHandlers = this.onceEvents.get(event);
        if (onceHandlers) {
            onceHandlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`Error in once event handler for '${event}':`, error);
                }
            });
            // Clear once handlers after execution
            this.onceEvents.delete(event);
        }
    }

    public removeAllListeners(event?: string): void {
        if (event) {
            this.events.delete(event);
            this.onceEvents.delete(event);
        } else {
            this.events.clear();
            this.onceEvents.clear();
        }
    }

    public getListenerCount(event: string): number {
        const handlers = this.events.get(event);
        const onceHandlers = this.onceEvents.get(event);
        
        let count = 0;
        if (handlers) count += handlers.size;
        if (onceHandlers) count += onceHandlers.size;
        
        return count;
    }

    public getEventNames(): string[] {
        const events = new Set<string>();
        
        this.events.forEach((_, event) => events.add(event));
        this.onceEvents.forEach((_, event) => events.add(event));
        
        return Array.from(events);
    }
}
