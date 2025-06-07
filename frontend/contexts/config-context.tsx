'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type SystemPromptType = 'chat' | 'compliance' | 'custom';

interface ConfigContextType {
    systemPromptType: SystemPromptType;
    customPrompt: string;
    setSystemPromptType: (type: SystemPromptType) => void;
    setCustomPrompt: (prompt: string) => void;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

interface ConfigProviderProps {
    children: ReactNode;
}

export function ConfigProvider({ children }: ConfigProviderProps) {
    const [systemPromptType, setSystemPromptType] = useState<SystemPromptType>('chat');
    const [customPrompt, setCustomPrompt] = useState('');

    return (
        <ConfigContext.Provider
            value={{
                systemPromptType,
                customPrompt,
                setSystemPromptType,
                setCustomPrompt,
            }}
        >
            {children}
        </ConfigContext.Provider>
    );
}

export function useConfig() {
    const context = useContext(ConfigContext);
    if (context === undefined) {
        throw new Error('useConfig must be used within a ConfigProvider');
    }
    return context;
}
