'use client';

import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface ModeContextType {
    mode: string;
    setMode: (mode: string) => void;
}

const ModeContext = createContext<ModeContextType | undefined>(undefined);

export function ModeProvider({ children }: { children: ReactNode }) {
    const [mode, setMode] = useState('lightrag/naive');

    return <ModeContext.Provider value={{ mode, setMode }}>{children}</ModeContext.Provider>;
}

export function useMode() {
    const context = useContext(ModeContext);
    if (context === undefined) {
        throw new Error('useMode must be used within a ModeProvider');
    }
    return context;
}
