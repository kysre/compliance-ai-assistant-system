'use client';

import type { ReactNode } from 'react';
import {
    AssistantRuntimeProvider,
    useLocalRuntime,
    type ChatModelAdapter,
} from '@assistant-ui/react';
import { useMode } from '@/contexts/ModeContext';

export function MyRuntimeProvider({
    children,
}: Readonly<{
    children: ReactNode;
}>) {
    const { mode } = useMode();

    const MyModelAdapter: ChatModelAdapter = {
        async run({ messages, abortSignal }) {
            // TODO replace with your own API
            // console.log(messages)
            // lightrag or rag:
            const ragType = mode.split('/')[0];
            // naive or gpt-4.1
            const ragMode = mode.split('/')[1];

            const result = await fetch('http://127.0.0.1:8080/api/compliance/query/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // forward the messages in the chat to the API
                body: JSON.stringify({
                    query: messages[messages.length - 1].content[0].text,
                    mode: ragMode,
                }),
                // if the user hits the "cancel" button or escape keyboard key, cancel the request
                signal: abortSignal,
            });

            const data = await result.json();
            console.log(data);
            console.log('delta time: ' + data.time);
            return {
                content: [
                    {
                        type: 'text',
                        text: data.text,
                    },
                ],
            };
        },
    };

    const runtime = useLocalRuntime(MyModelAdapter);

    return <AssistantRuntimeProvider runtime={runtime}>{children}</AssistantRuntimeProvider>;
}
