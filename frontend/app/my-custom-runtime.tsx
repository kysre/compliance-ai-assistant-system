'use client';

import { LocalRuntimeCore, Message, Thread } from '@assistant-ui/react';
import { ChatUtils } from '@/api/chat-utils';

export class MyCustomRuntime extends LocalRuntimeCore {
    async sendMessage(message: Message): Promise<void> {
        console.log(message);
        console.log(this);

        const { sendMessage } = ChatUtils;
        const threadId = '123';

        sendMessage(threadId, JSON.stringify(message)).json((json) => {
            const assistantMessage: Message = {
                id: json.id,
                role: 'assistant',
                content: json.content,
            };
            this.addMessage(assistantMessage);
        });
    }

    async getThreads(): Promise<Thread[]> {
        const { getThreads } = ChatUtils;
        const threads: Thread[] = [];
        getThreads().json((json) => {
            console.log(json);
            json.threads.forEach((thread: any) => {
                threads.push({
                    id: thread.id,
                    title: thread.title,
                    lastMessage: thread.lastMessage,
                    createdAt: new Date(thread.createdAt),
                });
            });
        });
        return threads;
    }

    async getMessages(threadId: string): Promise<Message[]> {
        const { getMessages } = ChatUtils;
        const messages: Message[] = [];
        getMessages(threadId).json((json) => {
            json.messages.forEach((message: any) => {
                messages.push({
                    id: message.id,
                    role: message.role,
                    content: message.content,
                    createdAt: new Date(message.createdAt),
                });
            });
        });
        return messages;
    }
}
