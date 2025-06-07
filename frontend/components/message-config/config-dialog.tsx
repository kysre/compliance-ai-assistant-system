'use client';

import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Settings } from 'lucide-react';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Textarea } from '@/components/ui/textarea';
import { useConfig } from '@/contexts/config-context';
import { useTranslations } from 'next-intl';

export function ConfigDialog() {
    const t = useTranslations('ConfigDialog');

    const { systemPromptType, customPrompt, setSystemPromptType, setCustomPrompt } = useConfig();

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline">
                    <Settings />
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>{t('title')}</DialogTitle>
                    <DialogDescription>{t('description')}</DialogDescription>
                </DialogHeader>

                <RadioGroup
                    value={systemPromptType}
                    onValueChange={(value) =>
                        setSystemPromptType(value as 'chat' | 'compliance' | 'custom')
                    }
                >
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="chat" id="r1" />
                        <div className="grid gap-2">
                            <Label htmlFor="r1">{t('chat')}</Label>
                            <p className="text-muted-foreground text-sm">{t('chatDescription')}</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="compliance" id="r2" />
                        <div className="grid gap-2">
                            <Label htmlFor="r2">{t('compliance')}</Label>
                            <p className="text-muted-foreground text-sm">
                                {t('complianceDescription')}
                            </p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3">
                        <RadioGroupItem value="custom" id="r3" />
                        <div className="grid gap-2">
                            <Label htmlFor="r3">{t('custom')}</Label>
                            <p className="text-muted-foreground text-sm">
                                {t('customDescription')}
                            </p>
                        </div>
                    </div>
                </RadioGroup>

                <Textarea
                    placeholder={t('customPromptPlaceholder')}
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    disabled={systemPromptType !== 'custom'}
                />
            </DialogContent>
        </Dialog>
    );
}
