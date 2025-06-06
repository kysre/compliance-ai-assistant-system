import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

import { Zap, Brain, Sparkles, Bot } from 'lucide-react';
import { useMode } from '@/contexts/mode-context';

const availableLightRagModes = [
    {
        text: 'Naive',
        value: 'lightrag/naive',
        icon: Brain,
    },
    {
        text: 'Local',
        value: 'lightrag/local',
        icon: Brain,
    },
    {
        text: 'Global',
        value: 'lightrag/global',
        icon: Brain,
    },
    {
        text: 'Hybrid',
        value: 'lightrag/hybrid',
        icon: Brain,
    },
];

// TODO: Fill this by api request to backend
const availableRagModes = [
    {
        text: 'GPT-4.1 Mini',
        value: 'rag/openai/gpt-4.1-mini',
        icon: Bot,
    },
    {
        text: 'GPT-4.1',
        value: 'rag/openai/gpt-4.1',
        icon: Bot,
    },
    {
        text: 'Gemini 2.5 Flash',
        value: 'rag/google/gemini-2.5-flash-preview-05-20',
        icon: Sparkles,
    },
    {
        text: 'Grok 3 Mini',
        value: 'rag/x-ai/grok-3-mini-beta',
        icon: Zap,
    },
];

export function ModeSelector() {
    const { mode, setMode } = useMode();

    return (
        <Select value={mode} onValueChange={setMode}>
            <SelectTrigger className="w-[200px]">
                <SelectValue />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel>LightRag</SelectLabel>
                    {availableLightRagModes.map((mode) => {
                        const IconComponent = mode.icon;
                        return (
                            <SelectItem key={mode.value} value={mode.value}>
                                <div className="flex items-center gap-2">
                                    <IconComponent className="h-4 w-4" />
                                    <span>{mode.text}</span>
                                </div>
                            </SelectItem>
                        );
                    })}
                </SelectGroup>
                <SelectGroup>
                    <SelectLabel>Rag</SelectLabel>
                    {availableRagModes.map((mode) => {
                        const IconComponent = mode.icon;
                        return (
                            <SelectItem key={mode.value} value={mode.value}>
                                <div className="flex items-center gap-2">
                                    <IconComponent className="h-4 w-4" />
                                    <span>{mode.text}</span>
                                </div>
                            </SelectItem>
                        );
                    })}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
}
