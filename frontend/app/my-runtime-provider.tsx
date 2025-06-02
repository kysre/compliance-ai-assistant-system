'use client';

import type { ReactNode } from 'react';
import { useMemo } from 'react';
import {
    AssistantRuntimeProvider,
    useLocalRuntime,
    type ChatModelAdapter,
    unstable_useRemoteThreadListRuntime,
    type RemoteThreadListAdapter,
    useThreadListItem,
    type ThreadHistoryAdapter,
    Message,
    Thread,
} from '@assistant-ui/react';
import { RuntimeAdapterProvider } from '@/app/runtime-adapter-provider';
import { useMode } from '@/contexts/ModeContext';
import { ChatUtils } from '@/api/chat-utils';

// Implement your custom adapter with proper message persistence
const myRemoteThreadListAdapter: RemoteThreadListAdapter = {
    async list() {
        const { getThreads } = ChatUtils;
        var threads: Thread[] = [];
        await getThreads().json((json) => {
            json.threads.forEach((thread: any) => {
                threads = [
                    ...threads,
                    {
                        // TODO: get the status from backend
                        // status: thread.archived ? "archived" : "regular",
                        status: 'regular',
                        remoteId: thread.id,
                        title: thread.title,
                    },
                ];
            });
        });
        return { threads: threads };
    },

    async initialize(threadId: string) {
        // TODO: create the thread in the database
        const { createThread } = ChatUtils;
        var newThreadId: string = '';
        await createThread().json((json) => {
            newThreadId = json.thread.id;
        });
        console.log(threadId, newThreadId);
        return { remoteId: newThreadId };
    },

    async rename(remoteId: string, newTitle: string) {
        // TODO: update the thread title in the database
        console.log(remoteId, newTitle);
    },

    async archive(remoteId: string) {
        // TODO: archive the thread in the database
        console.log(remoteId);
    },

    async unarchive(remoteId: string) {
        // TODO: unarchive the thread in the database
        console.log(remoteId);
    },

    async delete(remoteId: string) {
        // TODO: delete the thread and its messages in the database
        console.log(remoteId);
    },

    async generateTitle(remoteId: string, unstable_messages: any[]) {
        // TODO: generate title from messages using your AI
        console.log(remoteId, unstable_messages);
        // const title = await generateTitle(messages);
        // await db.threads.update(remoteId, { title });
        const title = 'test thread title';

        return new ReadableStream({
            start(controller) {
                controller.enqueue(new TextEncoder().encode(title));
                controller.close();
            },
        });
    },
};

// Complete implementation with message persistence using Provider pattern
export function MyRuntimeProvider({
    children,
}: Readonly<{
    children: ReactNode;
}>) {
    const { mode } = useMode();

    const MyChatModelAdapter: ChatModelAdapter = {
        async run({ messages, abortSignal }) {
            // console.log(messages)
            // lightrag or rag:
            console.log('messages', messages);
            const ragType = mode.split('/')[0];
            // naive or gpt-4.1
            const ragMode = mode.split('/')[1];

            console.log('mode', mode);
            console.log('ragType', ragType);
            console.log('ragMode', ragMode);

            const { query } = ChatUtils;

            var text: string = '';
            await query(ragMode, ragType, messages[messages.length - 1].content[0].text).json(
                (json) => {
                    text = json.text;
                },
            );
            return {
                content: [
                    {
                        type: 'text',
                        text: text,
                    },
                ],
            };
        },
    };

    const runtime = unstable_useRemoteThreadListRuntime({
        runtimeHook: () => {
            // Create a basic LocalRuntime - persistence will be added via Provider
            return useLocalRuntime(MyChatModelAdapter);
        },
        adapter: {
            ...myRemoteThreadListAdapter,
            // The Provider component adds thread-specific adapters
            unstable_Provider: ({ children }) => {
                // This runs in the context of each thread
                const threadListItem = useThreadListItem();
                const remoteId = threadListItem.remoteId;

                // Create thread-specific history adapter
                const history = useMemo<ThreadHistoryAdapter>(
                    () => ({
                        async load() {
                            const { getMessages } = ChatUtils;
                            var messages: Message[] = [];
                            console.log('messages', messages);
                            if (!remoteId) return { messages: [] };
                            await getMessages(remoteId).json((json) => {
                                json.messages.forEach((message: any) => {
                                    messages = [
                                        ...messages,
                                        {
                                            role: message.role,
                                            content: message.content,
                                            id: message.id,
                                            createdAt: new Date(message.createdAt),
                                        },
                                    ];
                                });
                            });
                            console.log('messages', messages);
                            return { messages: messages };
                        },

                        async append(message) {
                            console.log(message);
                            if (!remoteId) {
                                console.error('Cannot save message - thread not initialized');
                                return;
                            }
                            // TODO: save the message to the database
                            console.log(message);
                        },
                    }),
                    [remoteId],
                );

                const adapters = useMemo(() => ({ history }), [history]);

                return (
                    <RuntimeAdapterProvider adapters={adapters}>{children}</RuntimeAdapterProvider>
                );
            },
        },
    });

    // const runtime2 = useLocalRuntime(MyChatModelAdapter);
    return <AssistantRuntimeProvider runtime={runtime}>{children}</AssistantRuntimeProvider>;
}
