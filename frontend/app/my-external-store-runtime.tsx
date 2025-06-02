'use client';

import { ChatUtils } from '@/api/chat-utils';
import { useMode } from '@/contexts/ModeContext';
import { useThreadContext } from '@/contexts/thread-context';
import {
    AssistantRuntimeProvider,
    type ExternalStoreThreadData,
    ExternalStoreThreadListAdapter,
    ThreadMessageLike,
    useExternalStoreRuntime,
} from '@assistant-ui/react';
import { ReactNode, useState, useEffect } from 'react';

export function ChatWithThreads({
    children,
}: Readonly<{
    children: ReactNode;
}>) {
    const { currentThreadId, setCurrentThreadId, threads, setThreads } = useThreadContext();
    const [threadList, setThreadList] = useState<ExternalStoreThreadData<any>[]>([]);
    const setMessagesForThread = (threadId: string, messages: ThreadMessageLike[]) => {
        setThreads((prev) => new Map(prev).set(threadId, messages));
    };

    const { createThread, getThreads, getMessages } = ChatUtils;

    useEffect(() => {
        createThread().json((json) => {
            setCurrentThreadId(json.thread.id);
        });
        getThreads().json((json) => {
            var defaultThreadList = [];
            json.threads.forEach((thread: any) => {
                defaultThreadList = [
                    ...defaultThreadList,
                    {
                        threadId: thread.id,
                        status: 'regular',
                        title: thread.title,
                    },
                ];
                var messages = [];
                getMessages(thread.id).json((json) => {
                    json.messages.forEach((message: any) => {
                        messages = [...messages, {
                            id: message.id,
                            status: 'complete',
                            role: message.role,
                            content: [{ type: 'text', text: message.content }],
                        }];
                    });
                    setMessagesForThread(thread.id, messages);
                });
                setThreadList(defaultThreadList);
            });
        });
    }, []); // Empty dependency array means it runs only once on mount

    // Get messages for current thread
    const currentMessages = threads.get(currentThreadId) || [];

    const threadListAdapter: ExternalStoreThreadListAdapter = {
        threadId: currentThreadId,
        threads: threadList.filter((t) => t.status === 'regular'),
        archivedThreads: threadList.filter((t) => t.status === 'archived'),

        onSwitchToNewThread: async () => {
            const { createThread } = ChatUtils;
            var newId: string = '';
            await createThread().json((json) => {
                newId = json.thread.id;
            });
            setThreadList((prev) => [
                ...prev,
                {
                    threadId: newId,
                    status: 'regular',
                    title: 'New Chat',
                },
            ]);
            setThreads((prev) => new Map(prev).set(newId, []));
            setCurrentThreadId(newId);
        },

        onSwitchToThread: (threadId) => {
            setCurrentThreadId(threadId);
        },

        onRename: (threadId, newTitle) => {
            // TODO: update the thread title in the database
            setThreadList((prev) =>
                prev.map((t) => (t.threadId === threadId ? { ...t, title: newTitle } : t)),
            );
        },

        onArchive: (threadId) => {
            // TODO: archive the thread in the database
            setThreadList((prev) =>
                prev.map((t) => (t.threadId === threadId ? { ...t, status: 'archived' } : t)),
            );
        },

        onDelete: (threadId) => {
            // TODO: delete the thread and its messages in the database
            setThreadList((prev) => prev.filter((t) => t.threadId !== threadId));
            setThreads((prev) => {
                const next = new Map(prev);
                next.delete(threadId);
                return next;
            });
            if (currentThreadId === threadId) {
                setCurrentThreadId('default');
            }
        },
    };

    const setMessages = (messages: ThreadMessageLike[]) => {
        setThreads((prev) => new Map(prev).set(currentThreadId, messages));
    };

    const { mode } = useMode();

    const onNew = async (message) => {
        if (message.content.length !== 1 || message.content[0]?.type !== 'text')
            throw new Error('Only text content is supported');

        console.log('currentMessages', currentMessages);

        const userMessage: ThreadMessageLike = {
            id: `message-${Date.now()}`,
            status: 'running',
            metadata: {
                custom: {
                    threadId: currentThreadId,
                },
            },
            role: 'user',
            content: [{ type: 'text', text: message.content[0].text }],
        };
        setMessages([...currentMessages, userMessage]);

        // Handle new message for current thread
        // Your implementation here
        const ragType = mode.split('/')[0];
        // naive or gpt-4.1
        const ragMode = mode.split('/')[1];

        console.log('mode', mode);
        console.log('ragType', ragType);
        console.log('ragMode', ragMode);

        const { query } = ChatUtils;

        var text: string = '';
        await query(ragMode, ragType, message.content[0].text).json((json) => {
            text = json.text;
        });

        console.log('assistant message', text);

        userMessage.status = 'complete';

        const assistantMessage: ThreadMessageLike = {
            id: `message-${Date.now()}`,
            status: 'complete',
            metadata: {
                custom: {
                    threadId: currentThreadId,
                },
            },
            role: 'assistant',
            content: [{ type: 'text', text: text }],
        };
        setMessages([...currentMessages, userMessage, assistantMessage]);
    }

    const runtime = useExternalStoreRuntime({
        messages: currentMessages,
        setMessages: setMessages,
        onNew: onNew,
        adapters: {
            threadList: threadListAdapter,
        },
    });

    return <AssistantRuntimeProvider runtime={runtime}>{children}</AssistantRuntimeProvider>;
}
