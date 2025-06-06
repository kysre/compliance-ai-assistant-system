'use client';

import { ChatUtils } from '@/api/chat-utils';
import { useMode } from '@/contexts/mode-context';
import { useThreadContext } from '@/contexts/thread-context';
import {
    AssistantRuntimeProvider,
    ExternalStoreThreadListAdapter,
    ThreadMessageLike,
    useExternalStoreRuntime,
    type AppendMessage,
    type ExternalStoreThreadData,
} from '@assistant-ui/react';
import { ReactNode, useState, useEffect } from 'react';

const getRunningMessage = (
    role: 'user' | 'assistant',
    threadId: string,
    content: any,
): ThreadMessageLike => {
    return {
        id: `msg-${role}-${Date.now()}`,
        status: {
            type: 'running',
        },
        metadata: {
            custom: {
                threadId: threadId,
            },
        },
        role: role,
        content: content,
    };
};

const getCompletedMessageFromRunningMessage = (
    runningMessage: ThreadMessageLike,
    content: any,
): ThreadMessageLike => {
    return {
        id: runningMessage.id,
        status: {
            type: 'complete',
            reason: 'stop',
        },
        metadata: runningMessage.metadata,
        role: runningMessage.role,
        content: content,
    };
};

export function ChatWithThreads({
    children,
}: Readonly<{
    children: ReactNode;
}>) {
    // Local state management (assistant-ui)
    const { currentThreadId, setCurrentThreadId, threads, setThreads } = useThreadContext();
    const [threadList, setThreadList] = useState<ExternalStoreThreadData<any>[]>([]);
    const setMessagesForThread = (threadId: string, messages: ThreadMessageLike[]) => {
        setThreads((prev) => new Map(prev).set(threadId, messages));
    };

    // Local state management (app)
    const { mode } = useMode();

    // Backend api calls
    const { createThread, getThreads, getMessages } = ChatUtils;

    // Initialize the thread lists (runs only once on mount)
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
                        messages = [
                            ...messages,
                            {
                                id: message.id,
                                status: 'complete',
                                role: message.role,
                                content: [{ type: 'text', text: message.content }],
                                metadata: {
                                    unstable_state: false,
                                },
                            },
                        ];
                    });
                    setMessagesForThread(thread.id, messages);
                });
                setThreadList(defaultThreadList);
            });
        });
    }, []);

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

    // Get messages for current thread
    const currentMessages = threads.get(currentThreadId) || [];
    // Set messages for current thread
    const setMessages = (messages: ThreadMessageLike[]) => {
        setThreads((prev) => new Map(prev).set(currentThreadId, messages));
    };

    // Functions to handle message interactions in a thread
    const onNew = async (message: AppendMessage): Promise<void> => {
        if (message.content.length !== 1 || message.content[0]?.type !== 'text')
            throw new Error('Only text content is supported');
        const runningUserMessage = getRunningMessage('user', currentThreadId, [
            { type: 'text', text: message.content[0].text },
        ]);
        const runningAssistantMessage = getRunningMessage('assistant', currentThreadId, []);
        setMessages([...currentMessages, runningUserMessage, runningAssistantMessage]);

        const ragType = mode.split('/')[0];
        const ragMode = mode.split('/')[1];
        const { sendMessage } = ChatUtils;
        var text: string = '';
        await sendMessage(currentThreadId, message.content[0].text, ragType, ragMode)
            .json((json) => {
                text = json.text;
            })
            .catch((error) => {
                text = 'Something went wrong. Try again.';
            });

        const completedUserMessage: ThreadMessageLike = getCompletedMessageFromRunningMessage(
            runningUserMessage,
            runningUserMessage.content,
        );
        const completedAssistantMessage: ThreadMessageLike = getCompletedMessageFromRunningMessage(
            runningAssistantMessage,
            [{ type: 'text', text: text }],
        );
        setMessages([...currentMessages, completedUserMessage, completedAssistantMessage]);
    };
    const onEdit = async (message: AppendMessage): Promise<void> => {
        onNew(message);
    };
    const onReload = async (parentId: string | null, config: any): Promise<void> => {
        const userMsgId = config.parentId;
        const userMsg = currentMessages.find((m) => m.id === userMsgId);
        if (userMsg) {
            onNew(userMsg);
        }
    };
    const onCancel = async (): Promise<void> => {
        // TODO: cancel the running message
        console.log('onCancel');
    };

    const runtime = useExternalStoreRuntime({
        messages: currentMessages,
        setMessages: setMessages,
        onNew: onNew,
        onEdit: onEdit,
        onReload: onReload,
        onCancel: onCancel,
        adapters: {
            threadList: threadListAdapter,
        },
    });

    return <AssistantRuntimeProvider runtime={runtime}>{children}</AssistantRuntimeProvider>;
}
