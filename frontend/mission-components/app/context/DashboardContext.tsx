'use client';

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { TelemetryState, WSMessage } from '../types/websocket';
import { useDashboardWebSocket } from '../hooks/useDashboardWebSocket';

export interface Annotation {
    id: string;
    targetId: string; // ID of anomaly or metric
    text: string;
    author: string;
    timestamp: string;
}

export interface Operator {
    id: string;
    name: string;
    avatar: string;
    activePanel: string;
}

interface ContextValue {
    state: TelemetryState;
    isConnected: boolean;
    send: (msg: WSMessage) => void;
    dispatch: any;
    isReplayMode: boolean;
    toggleReplayMode: () => void;
    replayProgress: number;
    setReplayProgress: (p: any) => void;
    isPlaying: boolean;
    togglePlay: () => void;
    isBattleMode: boolean;
    setBattleMode: (active: boolean) => void;
    // Collaboration
    annotations: Annotation[];
    addAnnotation: (note: Omit<Annotation, 'id' | 'timestamp'>) => void;
    removeAnnotation: (id: string) => void;
    presence: Operator[];
}

const DashboardContext = createContext<ContextValue | undefined>(undefined);

export const DashboardProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const ws = useDashboardWebSocket();
    const [isBattleMode, setBattleMode] = useState(false);
    const [annotations, setAnnotations] = useState<Annotation[]>([]);
    const [presence] = useState<Operator[]>([
        { id: '1', name: 'SIGMA', avatar: 'Σ', activePanel: 'Mission Control' },
        { id: '2', name: 'ALPHA', avatar: 'A', activePanel: 'Systems' },
        { id: '3', name: 'KAPPA', avatar: 'K', activePanel: 'Chaos Engine' },
    ]);

    // Add Annotation
    const addAnnotation = (note: Omit<Annotation, 'id' | 'timestamp'>) => {
        const newNote: Annotation = {
            ...note,
            id: Math.random().toString(36).substr(2, 9),
            timestamp: new Date().toLocaleTimeString(),
        };
        setAnnotations(prev => [newNote, ...prev]);
    };

    // Remove Annotation
    const removeAnnotation = (id: string) => {
        setAnnotations(prev => prev.filter(a => a.id !== id));
    };

    // Auto-trigger Battle Mode on Critical Anomalies
    useEffect(() => {
        if (ws.state.mission?.anomalies) {
            const hasCritical = ws.state.mission.anomalies.some((a: any) => a.severity === 'Critical');
            if (hasCritical && !isBattleMode) {
                setBattleMode(true);
            }
        }
    }, [ws.state.mission?.anomalies, isBattleMode]);

    const value = {
        ...ws,
        isBattleMode,
        setBattleMode,
        annotations,
        addAnnotation,
        removeAnnotation,
        presence
    };

    return (
        <DashboardContext.Provider value={value}>
            {children}
        </DashboardContext.Provider>
    );
};

export const useDashboard = () => {
    const context = useContext(DashboardContext);
    if (!context) throw new Error('useDashboard must be used within DashboardProvider');
    return context;
};
