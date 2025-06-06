'use client'

import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Settings } from "lucide-react"
import {
    RadioGroup,
    RadioGroupItem,
} from "@/components/ui/radio-group"
import { Textarea } from "@/components/ui/textarea"
import { useConfig } from "@/contexts/config-context"

export function ConfigDialog() {
    const {
        systemPromptType,
        customPrompt,
        setSystemPromptType,
        setCustomPrompt
    } = useConfig()

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline">
                    <Settings />
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Assistant Settings</DialogTitle>
                    <DialogDescription>
                        Choose an assistant to use for your messages.
                    </DialogDescription>
                </DialogHeader>

                <RadioGroup
                    value={systemPromptType}
                    onValueChange={(value) => setSystemPromptType(value as 'chat' | 'compliance' | 'custom')}
                >
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="chat" id="r1" />
                        <div className="grid gap-2">
                            <Label htmlFor="r1">Chat</Label>
                            <p className="text-muted-foreground text-sm">
                                Chat with an intelligent assistant.
                            </p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="compliance" id="r2" />
                        <div className="grid gap-2">
                            <Label htmlFor="r2">Compliance</Label>
                            <p className="text-muted-foreground text-sm">
                                Check compliance with regulations.
                            </p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="custom" id="r3" />
                        <div className="grid gap-2">
                            <Label htmlFor="r3">Custom</Label>
                            <p className="text-muted-foreground text-sm">
                                Test your custom system prompt.
                            </p>
                        </div>
                    </div>
                </RadioGroup>

                <Textarea
                    placeholder="Your custom system prompt."
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    disabled={systemPromptType !== 'custom'}
                />
            </DialogContent>
        </Dialog>
    )
}
