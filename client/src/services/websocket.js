// src/services/websocket.js

/**
 * WebSocket connection manager:
 * - auto-reconnect (3s)
 * - subscribe/unsubscribe
 * - addListener/removeListener (pub-sub)
 *
 * Messages should include both reading and stats every 15s, e.g.:
 * { timestamp: "...", value: 28.35, stats: { "5min": {...}, "1hr": {...}, "6hr": {...}, "1day": {...} } }
 */

export function createSocket({ url, onOpen, onClose, onError, getPreference }) {
    let socket = null;
    let reconnectTimer = null;
    let manuallyClosed = false;
    const listeners = new Set();
    const RECONNECT_INTERVAL_MS = 3000;

    const connect = () => {
        socket = new WebSocket(url);

        socket.addEventListener('open', () => {
            onOpen && onOpen();
            const pref = getPreference && getPreference();
            if (pref.location && pref.type) {
                try {
                    socket.send(JSON.stringify({ action: 'subscribe', location: pref.location, type: pref.type }));
                } catch {}
            }
        });

        socket.addEventListener('message', (evt) => {
            let payload = null;
            try {
                payload = JSON.parse(evt.data);
            } catch {
                payload = evt.data;
            }
            listeners.forEach((fn) => {
                try { fn(payload); } catch {}
            });
        });

        socket.addEventListener('close', () => {
            onClose && onClose();
            if (!manuallyClosed) scheduleReconnect();
        });

        socket.addEventListener('error', (err) => {
            onError && onError(err);
        });
    };

    const scheduleReconnect = () => {
        if (reconnectTimer) return;
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            connect();
        }, RECONNECT_INTERVAL_MS);
    };

    const subscribe = ({ location, type }) => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ action: 'subscribe', location, type }));
        }
    };

    const unsubscribe = ({ location, type } = {}) => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ action: 'unsubscribe', location, type }));
        }
    };

    const addListener = (fn) => listeners.add(fn);
    const removeListener = (fn) => listeners.delete(fn);

    const close = () => {
        manuallyClosed = true;
        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
            reconnectTimer = null;
        }
        try { socket && socket.close(); } catch {}
    };

    connect();

    return {
        subscribe,
        unsubscribe,
        addListener,
        removeListener,
        close,
        get readyState() {
            return socket.readyState;
        },
    };
}